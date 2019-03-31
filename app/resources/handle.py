from models.profile import Profile


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'create', 'get', 'description', 'hacks'
    :param data: 'user_uuid', 'name', 'country', 'description', 'hacks'
    :return: user response for actions
    """

    if endpoint[0] == "create":
        if "user_uuid" not in data:
            return {"user_response": {"error": "Key 'user_uuid' has to be set for endpoint create."}}
        if type(data["user_uuid"]) is not str:
            return {"user_response": {"error": "Key 'user_uuid' has to be string for endpoint create."}}
        if "name" not in data:
            return {"user_response": {"error": "Key 'name' has to be set for endpoint create."}}
        if type(data["name"]) is not str:
            return {"user_response": {"error": "Key 'name' has to be string for endpoint create."}}
        if "country" not in data:
            return {"user_response": {"error": "Key 'country' has to be set for endpoint create."}}
        if type(data["country"]) is not str:
            return {"user_response": {"error": "Key 'country' has to be string for endpoint create."}}
        user_uuid: str = data["user_uuid"]
        name: str = data["name"]
        country: str = data["country"]
        return {"user_response": Profile.create(user_uuid, name, country)}
    if endpoint[0] == "get":
        if "user_uuid" not in data:
            return {"user_response": {"error": "Key 'user_uuid' has to be set for endpoint get."}}
        if type(data["user_uuid"]) is not str:
            return {"user_response": {"error": "Key 'user_uuid' has to be string for endpoint get."}}
        user_uuid: str = data["user_uuid"]
        return {"user_response": Profile.get(user_uuid)}
    if endpoint[0] == "description":
        if "user_uuid" not in data:
            return {"user_response": {"error": "Key 'user_uuid' has to be set for endpoint description."}}
        if type(data["user_uuid"]) is not str:
            return {"user_response": {"error": "Key 'user_uuid' has to be string for endpoint description."}}
        if "description" not in data:
            return {"user_response": {"error": "Key 'description' has to be set for endpoint description."}}
        if type(data["description"]) is not str:
            return {"user_response": {"error": "Key 'description' has to be string for endpoint description."}}
        user_uuid: str = data["user_uuid"]
        description: str = data["description"]
        return {"user_response": Profile.change_description(user_uuid, description)}
    if endpoint[0] == "hacks":
        if "user_uuid" not in data:
            return {"user_response": {"error": "Key 'user_uuid' has to be set for endpoint hacks."}}
        if type(data["user_uuid"]) is not str:
            return {"user_response": {"error": "Key 'user_uuid' has to be string for endpoint hacks."}}
        if "hacks" not in data:
            return {"user_response": {"error": "Key 'hacks' has to be set for endpoint hacks."}}
        if type(data["hacks"]) is not int:
            return {"user_response": {"error": "Key 'hacks' has to be integer for endpoint hacks."}}
        user_uuid: str = data["user_uuid"]
        hacks: int = data["hacks"]
        if hacks < 0:
            return {"user_response": {"error": "Key 'hacks' can not be negative."}}
        return Profile.update_hacks(user_uuid, hacks)
    return {"user_response": {"error": "Endpoint is not supported."}}


def handle_ms(data: dict) -> dict:
    return data
