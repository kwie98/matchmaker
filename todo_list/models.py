from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class Item(models.Model):
    class Status(models.TextChoices):
        PENDING = "P", gettext_lazy("Pending")
        DONE = "D", gettext_lazy("Done")
        CANCELLED = "C", gettext_lazy("Cancelled")

    text = models.TextField()
    status = models.CharField(max_length=1, choices=Status)


    def __str__(self):
        return f"[{self.status}] {self.text}"
