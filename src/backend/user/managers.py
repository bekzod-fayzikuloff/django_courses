from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if email is None:
            raise ValueError(_("Email is required"))
        if password is None:
            raise ValueError(_("Password is required"))

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise ValueError(_("Password is required"))
        user = self.create_user(email, password, username=username)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
