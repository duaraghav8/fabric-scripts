def get_role(hostname):
    """Return the role assigned to the specified host
    This function assumes that each host in the infrastructure is assigned exactly 1 role.
    If the given host doesn't exist in any of the roles' host list, None is returned.
    """
    for role in roledefs:
        if hostname in roledefs[role]["hosts"]:
            return role


def exists(hostname):
    """Returns True if the given host exists in any role's host list."""
    if not get_role(hostname):
        return False
    return True


roledefs = {}
