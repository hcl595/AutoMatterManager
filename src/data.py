# models.py
import datetime
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
    name = Column(String(32), index=True, nullable=False, comment="姓名")
    key = Column(String(32), nullable=False, comment="密码")
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
    day = Column(String(32), nullable=False, comment="日期")
    start_time = Column(String(32), nullable=False, comment="开始时间")
    finish_time = Column(String(32), nullable=False, comment="结束时间")
    event = Column(String(32), nullable=False, comment="事件名称")
    level = Column(Integer, nullable=False, comment="等级")
    acc = Column(String(32), index=True, nullable=False, comment="姓名")
    __table__args__ = (
        UniqueConstraint("id", "acc"),  # 联合唯一约束
        Index("acc", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.acc}>"


class share(Base):
    __tablename__ = "share"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    share_user = Column(String(32), nullable=False, comment="分享者")
    acc_user = Column(String(32), nullable=False, comment="接受者")
    eventID = Column(Integer, nullable=False, comment="事件主键")
    eventInfo = Column(String(32), nullable=False, comment="事件名称")
    __table__args__ = (
        UniqueConstraint("id", "share_user"),  # 联合唯一约束
        Index("share_user", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.acc}>"


class type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    type = Column(String(32), nullable=False, comment="类名称")
    level = Column(Integer, nullable=False, comment="等级")
    acc = Column(String(32), nullable=False, comment="姓名")
    __table__args__ = (
        UniqueConstraint("id", "acc"),  # 联合唯一约束
        Index("acc", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.acc}>"


def setup():
    if not database_exists(engine.url):
        create_database(engine.url)
        # 删除表
        Base.metadata.drop_all(engine)
        # 创建表
        Base.metadata.create_all(engine)
    user_instance = userInfo(
    name="admin",
    key="admin",
    )
    session.add(user_instance)


if __name__ == "__main__":
    setup()
    result = session.query(userInfo.id,userInfo.name,).all()
    print("already")
    print(result)
    print("complete!")
    result = session.query(matter.id,matter.acc,).all()
    print(result)
    print("complete!")