def make_error(*args: str, sep: str = "") -> dict:
    return {"error": sep.join(map(str, args))}


invalid_request = make_error("Invalid request.")
profile_already_exists = make_error("Profile already exists for this user.")
invalid_useruuid = make_error("Invalid user_uuid.")
success = {"success": True}
