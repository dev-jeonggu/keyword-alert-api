# Keyword Alert API
FastAPI 기반의 키워드 기반 알림 시스템 API입니다.  
사용자는 관심 키워드를 등록하고, 외부에서 전달된 메시지에 키워드가 포함되면 알림을 받을 수 있습니다.

## 👩🏻‍💻 Developer
| jeonggu.kim<br />(김정현) |
|:---:|
| <a href="https://github.com/dev-jeonggu"> <img src="https://avatars.githubusercontent.com/dev-jeonggu" width=100px alt="_"/> </a> |
| <a href="https://github.com/dev-jeonggu">@dev-jeonggu</a> |

## 📌 Key Features
- 사용자 회원가입 / 로그인 (JWT 인증)
- 관심 키워드 등록
- 외부 알림 메시지 수신 (Webhook처럼 사용 가능)
- 키워드 매칭 시 알림 저장
- 본인의 알림 조회 API 제공
- Swagger 자동 문서화

## 🛠 Tech Stack
| 항목       | 내용                        |
|------------|-----------------------------|
| Framework  | FastAPI                     |
| Database   | SQLite + SQLAlchemy         |
| Auth       | OAuth2 + JWT (python-jose)  |
| Hashing    | passlib[bcrypt]             |
| Docs       | Swagger (자동 생성)         |


## ⚙️ Installation & Run

### 1. 클론 및 진입

```bash
git clone https://github.com/dev-jeonggu/keyword-alert-api.git
cd keyword-alert-api
```
### 2. 가상환경 생성 및 패키지 설치
```
pip3 install fastapi uvicorn "python-jose[cryptography]" sqlalchemy bcrypt
pip3 install "passlib[bcrypt]"
pip3 install python-multipart
```
### 3. 서버 실행
```
uvicorn app.main:app --reload
```
- 접속: http://localhost:8000
- 문서: http://localhost:8000/docs

## 📁 Project Structure
```
keyword-alert-api/
├── main.py          # FastAPI 엔트리포인트
├── auth.py          # 인증(JWT, 해싱)
├── models.py        # SQLAlchemy 모델
├── schemas.py       # Pydantic 스키마
├── database.py      # DB 세션/엔진 관리
└── requirements.txt # 패키지 목록
```

## 🧪 API Test Scenarios
### 1. 회원가입
```
POST /signup
{
  "email": "test@example.com",
  "password": "1234"
}
```

### 2. 로그인 (JWT 발급)
```
POST /login (x-www-form-urlencoded)
username=test@example.com
password=1234
```

### 3. 키워드 등록
```
POST /subscribe-keyword
Authorization: Bearer <token>
{
  "word": "딥러닝"
}
```

### 4. 알림 수신
```
POST /notify
{
  "message": "다음 주에 딥러닝 세미나가 열립니다."
}
```

### 5. 알림 조회
```
GET /alerts
Authorization: Bearer <token>
```

## 📌 Notes
- 단일 사용자용 SQLite 기반 프로젝트
- Webhook 또는 크롤링 시스템과 연계하면 알림 자동화 가능
