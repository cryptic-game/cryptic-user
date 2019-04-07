from typing import Optional

from app import m
from models.profile import Profile
from schemes import *


@m.user_endpoint(path=["create"])
def endpoint_create(data: dict, user: str) -> dict:
    if "name" not in data or "country" not in data:
        return invalid_request

    name: str = data["name"]
    country: str = data["country"]

    if Profile.exists(user):
        return profile_already_exists

    Profile.create(user, name, country)

    return success


@m.user_endpoint(path=["get"])
def endpoint_get(data: dict, user: str) -> dict:
    profile: Profile = Profile.get(user)

    if profile is None:
        return invalid_user_uuid

    return profile.serialize


@m.user_endpoint(path=["description"])
def endpoint_description(data: dict, user: str) -> dict:
    if "description" not in data:
        return invalid_request

    description: str = data["description"]

    profile: Optional[Profile] = Profile.get(user)

    if profile is None:
        return invalid_user_uuid

    profile.change_description(description)

    return success


@m.user_endpoint(path=["hacks"])
def endpoint_hacks(data: dict, user: str) -> dict:
    if "hacks" not in data:
        return invalid_request

    hacks: int = data["hacks"]

    if not isinstance(hacks, int) or hacks < 0:
        return invalid_request

    profile: Optional[Profile] = Profile.get(user)

    if profile is None:
        return invalid_user_uuid

    profile.update_hacks(hacks)

    return success


@m.user_endpoint(path=["cluster"])
def endpoint_cluster(data: dict, user: str) -> dict:
    if "cluster" not in data:
        return invalid_request

    cluster: int = data["cluster"]

    if not isinstance(cluster, int) or cluster < 0:
        return invalid_request

    profile: Optional[Profile] = Profile.get(user)

    if profile is None:
        return invalid_user_uuid

    profile.change_cluster(cluster)

    return success
