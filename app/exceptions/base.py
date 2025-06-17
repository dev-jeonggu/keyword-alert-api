
DEFAULT_MESSAGE = "예상치 못한 오류가 발생했습니다."

class AppException(Exception):
    def __init__(self, detail: str = DEFAULT_MESSAGE, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)