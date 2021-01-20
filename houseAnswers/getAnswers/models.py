from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Provider(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200, unique=True)
    priority = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(9),MinValueValidator(1)]
    )
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Fields(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    key_phrase = models.CharField(max_length=200)

    def __str__(self):
        return self.name
