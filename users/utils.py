from django.core.exceptions import PermissionDenied


class UserRequiredMixin:
    """ Миксин для определения принадлежности объекта пользователю"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise PermissionDenied
        return self.object
