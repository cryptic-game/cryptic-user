from cryptic import MicroService

from models.profile import Profile

m: MicroService = MicroService(name="user")


@m.user_endpoint(path=["create"])
def create(data: dict, user: str) -> dict:
    if "name" not in data:
        return {"user_response": {"error": "Key 'name' has to be set for endpoint create."}}
    if type(data["name"]) is not str:
        return {"user_response": {"error": "Key 'name' has to be string for endpoint create."}}
    if "country" not in data:
        return {"user_response": {"error": "Key 'country' has to be set for endpoint create."}}
    if type(data["country"]) is not str:
        return {"user_response": {"error": "Key 'country' has to be string for endpoint create."}}
    name: str = data["name"]
    country: str = data["country"]
    return {"user_response": Profile.create(user, name, country)}


@m.user_endpoint(path=["get"])
def get(data: dict, user: str) -> dict:
    return {"user_response": Profile.get(user)}


@m.user_endpoint(path=["description"])
def description(data: dict, user: str) -> dict:
    if "description" not in data:
        return {"user_response": {"error": "Key 'description' has to be set for endpoint description."}}
    if type(data["description"]) is not str:
        return {"user_response": {"error": "Key 'description' has to be string for endpoint description."}}
    description: str = data["description"]
    return {"user_response": Profile.change_description(user, description)}


@m.user_endpoint(path=["hacks"])
def hacks(data: dict, user: str) -> dict:
    if "hacks" not in data:
        return {"user_response": {"error": "Key 'hacks' has to be set for endpoint hacks."}}
    if type(data["hacks"]) is not int:
        return {"user_response": {"error": "Key 'hacks' has to be integer for endpoint hacks."}}
    hacks: int = data["hacks"]
    if hacks < 0:
        return {"user_response": {"error": "Key 'hacks' can not be negative."}}
    return Profile.update_hacks(user, hacks)


@m.user_endpoint(path=["cluster"])
def cluster(data: dict, user: str) -> dict:
    if "cluster" not in data:
        return {"user_response": {"error": "Key 'cluster' has to be set for endpoint cluster."}}
    if type(data["cluster"]) is not int and data["cluster"] is not None:
        return {"user_response": {"error": "Key 'cluster' has to be integer or null for endpoint cluster."}}
    cluster: int = data["cluster"]
    return Profile.change_cluster(user, cluster)
