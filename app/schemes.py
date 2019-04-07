def make_error(*args: str, origin: str, sep: str = "") -> dict:
    return {"error": sep.join(map(str, args)), "origin": origin}


invalid_request: dict = make_error("invalid request", origin="user")
profile_already_exists: dict = make_error("profile already exists for this user", origin="user")
invalid_user_uuid: dict = make_error("invalid user_uuid", origin="user")
success: dict = {"success": True}
