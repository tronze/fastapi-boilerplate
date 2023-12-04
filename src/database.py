from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"sqlite:///db.sqlite3"

# connect args의 check same thread 옵션은 sqlite 데이터 베이스를 사용할 때 필요
# Sqlite는 동시에 하나의 thread만 허용하는데 FastAPI 특성상 이를 비활성화 해줄 필요가 있음.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


Base = declarative_base(cls=BaseModel)


def get_db():
    """데이터베이스 세션 생성 함수 입니다.

    Returns:
         void
    """
    db = db_session()  # 세션
    try:
        yield db  # 세션 Generator 반환
    finally:
        db.close()  # 사용 완료 후 세션 회수
