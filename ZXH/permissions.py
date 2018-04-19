from rest_framework import permissions
from ZXH.models import Log
from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('user_id') is not None

    def has_object_permission(self, request, view, Log):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return Log.owner.id == request.session.get('user_id')
class IsLogsUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.session.get('user_id') is not None
    # def has_permission(self, request, view):
    #     return request.session.get('user_id')
    def has_object_permission(self, request, view, Log):
        return Log.owner == request.session.get('user_id')

