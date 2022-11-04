from django.http import Http404


class AuthenticatedUserPermissionsMixin:

    def has_permissions(self):
        if self.request.user.is_superuser:
            return True
        return self.request.user.username == self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class UserPermissionsMixin:

    def has_permissions(self):
        if self.request.user.is_superuser:
            return True
        return self.get_object().username == self.request.user.username

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

