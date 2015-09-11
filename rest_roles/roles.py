from __future__ import relative_imports

from . import ALL_ACTIONS, ALL_VIEWS, RoleConfigurationError


class RoleMeta(object):
    """Metaclass to register role classes."""
    registry = []

    def __new__(cls, name, bases, dct):
        """Register all roles created in the system."""
        role_cls = super(RoleMeta, cls).__new__(cls, name, bases, dct)
        if role_cls != Role:
            cls.registry.append(role_cls)


class Role(object):
    """Base class for constructing role-based permissions."""

    __metaclass__ = RoleMeta

    def __init__(self, request, view):
        """Init receives request and view as arguments."""
        super(Role, self).__init__()

    def is_active(self, request, view):
        """
        Whether this role is active for the given request.

        Subclasses should implement custom logic that returns a truthy value if
        the role should be activated.
        """
        raise NotImplementedError('Roles must define is_active')

    def get_permissions(self, request, view):
        """
        Retrieve the permissions assigned to this role for this request.

        Subclasses should return a dict object, which map views or viewsets to
        an inner dict. These inner dicts map actions (roughly, HTTP verbs) to
        one last dict. This dict contains two keys, one to define the fields to
        be made accessible, the other to define any restrictions on the items
        to serialize and return. This is best described with an example:

        {
            CatViewSet: {
                'create': {
                    'fields': ['age', 'color', 'grumpiness'],
                    'restrictions': None,
                },
                ...
            },
            ...
        }
        """
        raise NotImplementedError('Roles must define get_permissions')

    def _has_permission(self, request, view):
        """Enforce all permissions on this request."""
        # Get the full set of permissions
        permissions = self.get_permissions(request, view)

        # Retrieve the permissions specific to the current view
        view_cls = view.cls
        if ALL_VIEWS in permissions:
            if len(permissions) > 1:
                raise RoleConfigurationError(
                    'When using ALL_VIEWS, other views may not be defined in '
                    'your permissions')
            view_permissions = permissions[ALL_VIEWS]
        elif view_cls in permissions:
            view_permissions = permissions[view_cls]
        else:
            return False

        # Retrieve the fields and restrictions for the current action
        action = self._get_action(request, view)
        if ALL_ACTIONS in view_permissions:
            if len(permissions) > 1:
                raise RoleConfigurationError(
                    'When using ALL_ACTIONS, other actions may not be defined '
                    'in your permissions for the view')
            action_permissions = view_permissions[ALL_ACTIONS]
        elif action in view_permissions:
            action_permissions = view_permissions[action]
        else:
            return False

        # Enforce the field-level and row-level permissions
        self._enforce_fields(
            request, view, action_permissions['fields'])
        self._enforce_restrictions(
            request, view, action_permissions['restrictions'])

        # At this point, you have permission, congratulations!
        return True

    def _get_action(self, request, view):
        """Retrieve the action being attempted in this request."""
        pass

    def _enforce_fields(self, request, view, fields):
        """Dynamically restrict the fields in the serializer."""
        # See here for potential code to steal or repurpose:
        # https://gist.github.com/jeffschenck/ca7218cac2191b392043
        pass

    def _enforce_restrictions(self, request, view, restrictions):
        """Ensure only valid objects are created or modified."""
        # For creates, this will require validating that the object about to be
        # created *would* match the queries being described by the Q object
        # (or compound Q object) passed in as restrictions here. I imagine a
        # fully implemented version of this is massive and kind of gross, since
        # we'd need to implement Python-side calculations to mirror all Q
        # functionality:
        # - & and | and ~ operations between Q nodes
        # - __ foreign key traversal syntax
        # - all the field lookup types (__gte, __in, etc.)

        # For other operations, this should be a bit simpler but still a bit
        # gross. We'll be hooking into the DRF cycle to automatically filter
        # down the queryset immediately after the view's get_queryset is
        # completed.
        pass
