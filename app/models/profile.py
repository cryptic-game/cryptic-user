import datetime
from typing import Union, NoReturn, Optional

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import exists

import objects as db


class Profile(db.Base):
    __tablename__: str = "profile"

    user_uuid: Union[Column, str] = Column(String(36), primary_key=True, unique=True)
    name: Union[Column, str] = Column(String(32))
    registered: Union[Column, datetime.datetime] = Column(DateTime, nullable=False)
    cluster_id: Union[Column, int] = Column(Integer)
    description: Union[Column, str] = Column(String(256), default='')
    country: Union[Column, str] = Column(String(32))
    num_hacks: Union[Column, int] = Column(Integer, default=0)

    def change_description(self, description: str) -> NoReturn:
        self.description = description
        db.session.commit()

    def update_hacks(self, hacks: int) -> NoReturn:
        self.num_hacks = hacks
        db.session.commit()

    def change_cluster(self, cluster: int) -> NoReturn:
        self.cluster_id = cluster
        db.session.commit()

    @property
    def serialize(self) -> dict:
        _ = self.user_uuid
        result: dict = {**self.__dict__}
        if "_sa_instance_state" in result:
            del result["_sa_instance_state"]
        registered: datetime.datetime = result["registered"]
        result["registered"]: int = int(registered.timestamp() * 1000)
        return result

    @staticmethod
    def exists(user_uuid: str) -> bool:
        return db.session.query(exists().where(Profile.user_uuid == user_uuid)).scalar() == 1

    @staticmethod
    def get(user_uuid: str) -> Optional['Profile']:
        return db.session.query(Profile).get(user_uuid)

    @staticmethod
    def create(user_uuid: str, name: str, country: str) -> bool:
        """
        Creates a new profile
        :param user_uuid: The UUID of the user
        :param name: The username
        :param country: The country of the user
        :return: Dict with status
        """

        profile: Profile = Profile(
            user_uuid=user_uuid,
            name=name,
            registered=datetime.datetime.now(),
            country=country
        )

        db.session.add(profile)
        db.session.commit()

        return True
