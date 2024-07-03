from django.contrib.auth.models import BaseUserManager
from .choices import USER_ROLE_ADMIN


class UserManager(BaseUserManager):
    def create_user(self, phone, role):
        if not phone:
            raise ValueError("کاربران باید یک شماره موبایل داشته باشند")

        user = self.model(
            phone=phone,
            role=role
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone=phone,
            role=USER_ROLE_ADMIN
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
