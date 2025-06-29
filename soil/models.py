from django.db import models

# Create your models here.
class soil(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/soil/')
    description = models.TextField()
    plants = models.ManyToManyField('plant', related_name='soils', blank=True)

    def __str__(self):
        return self.name

class plant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'image/plant/')
    description = models.TextField()

    def __str__(self):
        return self.name