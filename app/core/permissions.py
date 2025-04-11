def has_access(user_id, doc, action):
    acl = doc.get("access", {})
    for role, users in acl.items():
        if user_id in users and action in ["read", "edit", "delete"]:
            return True
    return False
