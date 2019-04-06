import datetime
from typing import Union, NoReturn

from sqlalchemy import Column, Integer, String, DateTime

import objects as db
from schemes import *


class Profile(db.Base):
    __tablename__: str = "profile"

    user_uuid: Union[Column, str] = Column(String(36), primary_key=True, unique=True)
    name: Union[Column, str] = Column(String(32))
    registered: Union[Column, datetime.datetime] = Column(DateTime, nullable=False)
    cluster_id: Union[Column, int] = Column(Integer)
    description: Union[Column, str] = Column(String(256), default='')
    country: Union[Column, str] = Column(String(32))
    num_hacks: Union[Column, int] = Column(Integer, default=0)

    @property
    def serialize(self) -> dict:
        _ = self.user_uuid
        result: dict = {**self.__dict__}
        if "_sa_instance_state" in result:
            del result["_sa_instance_state"]
        registered: datetime.datetime = result["registered"]
        result["registered"] = int(registered.timestamp() * 1000)
        return result

    @staticmethod
    def create(user_uuid: str, name: str, country: str) -> NoReturn:
        """
        Creates a new profile
        :param user_uuid: The UUID of the user
        :param name: The username
        :param country: The country of the user
        :return: Dict with status
        """

        assert not Profile.exists(user_uuid), profile_already_exists

        profile: Profile = Profile(
            user_uuid=user_uuid,
            name=name,
            registered=datetime.datetime.now(),
            country=country
        )

        db.session.add(profile)
        db.session.commit()

    @staticmethod
    def exists(user_uuid: str) -> bool:
        profile: Profile = db.session.query(Profile).get(user_uuid)
        return profile is not None

    @staticmethod
    def get(user_uuid: str) -> dict:
        profile: Profile = db.session.query(Profile).get(user_uuid)
        assert profile is not None, invalid_useruuid
        return profile.serialize

    @staticmethod
    def change_description(user_uuid: str, description: str) -> NoReturn:
        assert Profile.exists(user_uuid), profile_already_exists
        db.session.query(Profile).filter(Profile.user_uuid == user_uuid). \
            update({"description": description})
        db.session.commit()

    @staticmethod
    def update_hacks(user_uuid: str, hacks: int) -> NoReturn:
        assert Profile.exists(user_uuid), profile_already_exists
        db.session.query(Profile).filter(Profile.user_uuid == user_uuid). \
            update({"num_hacks": hacks})
        db.session.commit()

    @staticmethod
    def change_cluster(user_uuid: str, cluster: int) -> NoReturn:
        assert Profile.exists(user_uuid), profile_already_exists
        db.session.query(Profile).filter(Profile.user_uuid == user_uuid). \
            update({"cluster_id": cluster})
        db.session.commit()
