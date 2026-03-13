from django.conf import settings
from django.db import models
from .current_user import get_current_user


class AuditModel(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True,null=True,blank=True,editable=False)
    updated_dt = models.DateTimeField(auto_now=True,null=True,blank=True,editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()

        if user and not user.is_anonymous:
            if not self.pk and not self.created_by:
                self.created_by = user

            self.updated_by = user

        super().save(*args, **kwargs)