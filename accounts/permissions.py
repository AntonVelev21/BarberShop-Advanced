from rest_framework.permissions import BasePermission


class HasFullAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('accounts.have_full_access'):
            return True
        else:
            return False