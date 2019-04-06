from app import m
from models.profile import Profile
from schemes import *


@m.user_endpoint(path=["create"])
def create(data: dict, user: str) -> dict:
    if "name" not in data or "country" not in data:
        return invalid_request
    name: str = data["name"]
    country: str = data["country"]
    try:
        Profile.create(user, name, country)
    except AssertionError:
        return profile_already_exists
    return success


@m.user_endpoint(path=["get"])
def get(data: dict, user: str) -> dict:
    try:
        return Profile.get(user)
    except AssertionError:
        return invalid_useruuid


@m.user_endpoint(path=["description"])
def description(data: dict, user: str) -> dict:
    if "description" not in data:
        return invalid_request
    description: str = data["description"]
    try:
        Profile.change_description(user, description)
    except AssertionError:
        return invalid_useruuid
    return success


@m.user_endpoint(path=["hacks"])
def hacks(data: dict, user: str) -> dict:
    if "hacks" not in data or data["hacks"] < 0:
        return invalid_request
    hacks: int = data["hacks"]
    try:
        Profile.update_hacks(user, hacks)
    except AssertionError:
        return invalid_useruuid
    return success


@m.user_endpoint(path=["cluster"])
def cluster(data: dict, user: str) -> dict:
    if "cluster" not in data:
        return invalid_request
    cluster: int = data["cluster"]
    try:
        Profile.change_cluster(user, cluster)
    except AssertionError:
        return invalid_useruuid
    return success
