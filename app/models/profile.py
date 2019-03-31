import datetime

from sqlalchemy import Column, Integer, String, DateTime

import objects_db as db


class Profile(db.base):
    __tablename__: str = "profile"

    user_uuid: Column = Column(String(36), primary_key=True, unique=True)
    name: Column = Column(String(32))
    registered: Column = Column(DateTime, nullable=False)
    cluster_id: Column = Column(Integer)
    description: Column = Column(String(256), default='')
    country: Column = Column(String(32))
    num_hacks: Column = Column(Integer, default=0)

    @property
    def serialize(self) -> dict:
        _ = self.user_uuid
        return {**self.__dict__}

    @staticmethod
    def create(user_uuid: str, name: str, country: str) -> dict:
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

        return {"success": "Profile has been created.", "user_uuid": user_uuid, "name": name}

    @staticmethod
    def get(user_uuid: str) -> dict:
        profile: Profile = db.session.query(Profile).get(user_uuid)
        if profile is None:
            return {"error": "Invalid user_uuid."}
        return {"success": profile.serialize}

    @staticmethod
    def change_description(user_uuid, description):
        if "error" in Profile.get(user_uuid):
            return {"error": "Invalid user_uuid."}
        db.session.query(Profile).filter(Profile.user_uuid == user_uuid). \
            update({"description": description})
        return {"success": "Description has been updated.", "user_uuid": user_uuid}
