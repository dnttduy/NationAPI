from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Nation(models.Model):
  nationId = models.CharField(max_length=100)
  lonlats = ArrayField(
      ArrayField(
          models.FloatField(),
          size=2,
      ),
  )

  def __str__(self):
      return self.nationId
