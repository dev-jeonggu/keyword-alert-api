from fastapi import FastAPI, Depends
from app.exceptions import register_exception_handlers
from app.exceptions.base import AppException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import app.models.models as models
import app.schemas.schemas as schemas  # 이렇게 하나만 import
import app.auth.auth as auth
from typing import cast
from app.db.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

register_exception_handlers(app)

# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 유저 인증
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    from app.auth.auth import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise AppException("유효하지 않은 토큰입니다", 401)
    except JWTError:
        raise AppException("유효하지 않은 토큰입니다", 401)
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise AppException(f"해당 사용자를 찾을 수 없습니다: {email}", 404)
    return user

# 회원가입
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 중복 사용자 확인
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise AppException("이미 존재하는 사용자입니다", 409)
    
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created"}

# 로그인
@app.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise AppException("잘못된 인증 정보입니다", 401)
    
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# 키워드 등록
@app.post("/subscribe-keyword")
def subscribe_keyword(keyword: schemas.KeywordCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 중복 키워드 확인
    existing_keyword = db.query(models.Keyword).filter(
        models.Keyword.word == keyword.word,
        models.Keyword.owner_id == current_user.id
    ).first()
    if existing_keyword:
        raise AppException(f"이미 등록된 키워드입니다: {keyword.word}", 409)
    
    k = models.Keyword(word=keyword.word, owner_id=current_user.id)
    db.add(k)
    db.commit()
    return {"message": "Keyword subscribed"}

# 외부 알림 전송 (내부 호출용)
@app.post("/notify")
def notify(payload: dict, db: Session = Depends(get_db)):
    message = str(payload.get("message", ""))
    if not message:
        raise AppException("메시지가 비어있습니다", 400)
    
    # 이미 동일한 메시지가 있는지 확인
    existing_alert = db.query(models.Alert).filter(models.Alert.message == message).first()
    if existing_alert:
        raise AppException("이미 동일한 알림 메시지가 존재합니다", 409)
    
    all_keywords = db.query(models.Keyword).all()
    matched_users = set()  # 중복 방지를 위해 set 사용
    
    for k in all_keywords:
        keyword_str = cast(str, k.word)
        if keyword_str in message:
            matched_users.add(k.owner.email)
            
    # 매칭된 사용자들에게 알림 생성
    for user_email in matched_users:
        alert = models.Alert(message=message, user_email=user_email)
        db.add(alert)
    db.commit()
    return {"message": "Notification processed", "notified_users": len(matched_users)}

# 내 알림 조회
@app.get("/alerts", response_model=list[schemas.AlertOut])
def get_alerts(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.user_email == current_user.email).all()