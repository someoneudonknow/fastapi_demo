from fastapi import Depends

from app.cores.error_response import ForbiddenException
from app.dependencies.auth_dependency import get_current_user


def require_role(*allowed_roles: str):
    async def role_checker(current_user=Depends(get_current_user)):
        user_role = current_user["user"].get("role")

        if not user_role:
            raise ForbiddenException("Role not found")

        if user_role not in allowed_roles:
            raise ForbiddenException(
                "You do not have permission to access this resource"
            )

        return current_user

    return role_checker
