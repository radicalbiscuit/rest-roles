from __future__ import absolute_import

from .base import RoleBasedPermission
from .roles import Role

__version__ = '0.1.0'

ALL_VIEWS = 'ALL_VIEWS'
ALL_ACTIONS = 'ALL_ACTIONS'
ALL_FIELDS = 'ALL_FIELDS'


class RoleConfigurationError(Exception):
    """Error relating to the definition of a Role subclass."""
