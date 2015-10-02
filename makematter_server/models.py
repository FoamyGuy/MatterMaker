import os
from django.db import models
from uuid import uuid4
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from makematter_server.settings import MEDIA_OUT


class Object(models.Model):
    uuid = models.CharField("uuid", max_length=50, primary_key=True, default=uuid4, unique=True)
    scad_file = models.FileField("Openscad File", upload_to='out', blank=True)
    stl_file = models.FileField("STL File", upload_to='out', blank=True)

    def __str__(self):
        return self.uuid


@receiver(post_delete, sender=Object)
def object_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.stl_file:
        if os.path.isfile(instance.stl_file.path):
            os.remove(instance.stl_file.path)
            instance.stl_file.delete(False)

    instance.scad_file.delete(False)
