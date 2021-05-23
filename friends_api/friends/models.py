from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_sent'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_received'
    )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return "%s" % self.from_user_id
