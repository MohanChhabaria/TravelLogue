from django.db import models
from users.models import UserProfile
import random
from django.utils.deconstruct import deconstructible
from django.db.models.signals import pre_save
from .utils import get_extension

class Iternary(models.Model):
    travellor = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    no_of_days = models.IntegerField()
    expenditure = models.IntegerField()
    registration_timestamp = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Media(models.Model):
    title = models.CharField(max_length=50, null=True)
    iternary = models.ForeignKey(Iternary, on_delete=models.CASCADE)
    media = models.ImageField(upload_to="iternary_images")
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{}  image  - {}".format(self.iternary.title, self.uploaded_at)


@deconstructible
class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    starting_day = models.IntegerField()
    iternary = models.ForeignKey(Iternary, on_delete=models.CASCADE)

    class Meta:
        ordering = ["starting_day"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name
    

@deconstructible
class Accomodation(models.Model):
    property_name = models.CharField(max_length=200,null=False)
    location = models.URLField()
    price = models.IntegerField()
    review = models.TextField(max_length=2000)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    class Meta:
        ordering = ["destination__starting_day"]
        verbose_name = "Accomodation"
        verbose_name_plural = "Accomodations"

    def __str__(self):
        return self.property_name



def event_pre_save_media(sender, instance, *args, **kwargs):
    ext = get_extension(instance.media.name)
    instance.media.name = instance.iternary.travellor.user.get_full_name()  + "_"  \
        + instance.iternary.title  +"_" + str(random.randint(1,10000))  + ext


def event_pre_save_iternary(sender, instance, *args, **kwargs):
    instance.title = (instance.title).lower()


pre_save.connect(event_pre_save_media, sender=Media)
pre_save.connect(event_pre_save_iternary, sender=Iternary)



