from typing import Optional

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.orm import Session

from ..base import QFEntity, open_session
from loguru import logger


class QFUser(QFEntity):
    """
    qfusion user 表
    """
    __tablename__ = "user"
    uuid = Column(String(length=32), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False, unique=True, default="")
    password = Column(String(length=255), nullable=False)
    description = Column(String(length=255), default="")
    email = Column(String(255))
    phonenumber = Column(String(255))
    aliasname = Column(String(50), default="", nullable=False)
    department = Column(String(50), default="", nullable=False)
    usertype = Column(String(20), default="", nullable=False)
    parentid = Column(String(32), default="", nullable=True)
    backupstorageinterfaceid = Column(String(32), default="", nullable=True)
    createdate = Column(TIMESTAMP, nullable=False)
    lastopdate = Column(TIMESTAMP, nullable=False)
    lastchecktime = Column(TIMESTAMP, nullable=True)

    @classmethod
    def get_auth_user(cls, session: Session, name: str, password: str) -> Optional["QFUser"]:
        """
        验证用户名、密码是否对应
        :param session: 会话对象
        :param name: 用户名
        :param password: 密码
        :return: 成功返回用户对象，失败返回空
        """
        try:
            if user := session.query(cls).filter_by(name=name).first():
                if user.password == password:
                    return user
            return None
        except Exception as e:
            logger.error(f"auth {name} password {password} error -> {e}")
            return None

    @classmethod
    def get_user_by_uuid(cls,session:Session, uuid: str) -> Optional["QFUser"]:
        """
        根据uuid获取当前用户
        :param uuid: 用户的uuid
        :return: 成功返回用户对象，失败返回空
        """
        try:
            user = session.query(cls).filter_by(uuid=uuid).first()
            return user
        except Exception as e:
            logger.error(f"the user does not exist : {uuid}.\nerr info -> {e}")
            return None

    @classmethod
    def get_department_by_uuid(cls, uuid: str) -> Optional["QFUser"]:
        """
        通过用户的uuid获取用户的部门
        :param uuid: 用户的uuid
        :return: 成功返回用户对象，失败返回空
        """
        user: Optional["QFUser"] = cls.get_user_by_uuid(uuid=uuid)

        if not user:
            return None

        if user.usertype == "admin":
            return user
        else:
            department = cls.get_user_by_uuid(uuid=user.parentid)
            return department
