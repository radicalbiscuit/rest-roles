from rest_framework import permissions

from .roles import RoleMeta


class RoleBasedPermission(permissions.BasePermission):
    """
    Base role-based permission class.

    This is intended to be included in DEFAULT_PERMISSION_CLASSES in your
    REST_FRAMEWORK settings. It automatically encapsulates all the logic
    defined in your various roles.
    """

    def has_permission(self, request, view):
        """Run through all roles and return True if any grant permission."""
        for role_cls in RoleMeta.registry:
            role = role_cls(request, view)
            if role.is_active(request, view):
                if role._has_permission(request, view):
                    return True
        return False
