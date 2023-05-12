# models.py
from sqlalchemy import create_engine,Column,Integer,String,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy_utils import database_exists,create_database
from sqlalchemy.ext.declarative import declarative_base

# 基础类
Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/FlaskProgram")
Session = sessionmaker(bind=engine)
session = scoped_session(Session)


class userInfo(Base):
    # 数据库中存储的表名
    __tablename__ = "userInfo"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    account = Column(String(32), index=True, nullable=False, comment="姓名")
    password = Column(String(32), nullable=False, comment="密码")
    mail = Column(String(32), index=True, nullable=True, comment="邮箱")
    __table__args__ = (
        UniqueConstraint("id", "name"),  # 联合唯一约束
        Index("name", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.name} key:{self.key}>"


class matter(Base):
    __tablename__ = "matter"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    date = Column(String(32), nullable=False, comment="日期")
    start_time = Column(String(32), nullable=False, comment="开始时间")
    finish_time = Column(String(32), nullable=False, comment="结束时间")
    matterInfo = Column(String(32), nullable=False, comment="事件名称")
    level = Column(Integer, nullable=False, comment="等级")
    account = Column(String(32), index=True, nullable=False, comment="姓名")
    comment = Column(String(255), nullable=False, comment="事件备注")
    __table__args__ = (
        UniqueConstraint("id", "account"),  # 联合唯一约束
        Index("account", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} account:{self.account}>"


class share(Base):
    __tablename__ = "share"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    share_user = Column(String(32), nullable=False, comment="分享者")
    accept_user = Column(String(32), nullable=False, comment="接受者")
    matterID = Column(Integer, nullable=False, comment="事件主键")
    matterInfo = Column(String(32), nullable=False, comment="事件名称")
    __table__args__ = (
        UniqueConstraint("id", "share_user"),  # 联合唯一约束
        Index("share_user", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} share_user:{self.share_user}>"


class type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    type = Column(String(32), nullable=False, comment="类名称")
    level = Column(Integer, nullable=False, comment="等级")
    type_matter = Column(String(255), nullable=True, comment="类库")
    account = Column(String(32), nullable=False, comment="姓名")
    __table__args__ = (
        UniqueConstraint("id", "account"),  # 联合唯一约束
        Index("account", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} account:{self.account}>"


def setup():
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        user_instance = userInfo(
        account="admin",
        password="admin1234",
        )
        session.add(user_instance)
        session.commit()
        session.remove()
        print("database setup completely!")
    else:
        pass

if __name__ == "__main__":
    setup()