from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class Item(models.Model):
    text = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=(
            ("P", gettext_lazy("Pending")),
            ("D", gettext_lazy("Done")),
            ("C", gettext_lazy("Cancelled")),
        ),
    )

    def __str__(self):
        return f"[{self.status}] {self.text}"
