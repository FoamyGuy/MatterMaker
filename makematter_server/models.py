import os
from django.db import models
from uuid import uuid4
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models import ForeignKey
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver




class MatterObject(models.Model):
    uuid = models.CharField("uuid", max_length=50, primary_key=True, default=uuid4, unique=True)
    scad_file = models.FileField("Openscad File", upload_to='out', blank=True)
    stl_file = models.FileField("STL File", upload_to='out', blank=True)

    def __str__(self):
        return self.uuid


class MatterTemplate(models.Model):
    uuid = models.CharField("uuid", max_length=50, primary_key=True, default=uuid4, unique=True)
    template_str = models.TextField("Template String", max_length=10000, blank=True, default="")
    name = models.CharField("Name", max_length="30", blank=True, default="")

    def __str__(self):
        return self.name



class MatterTemplateVar(models.Model):
    template = ForeignKey(MatterTemplate)
    name = models.CharField("Name", max_length="30", blank=True, default="")
    type = models.CharField("Type", max_length="20", blank=True, default="int")

    def __str__(self):
        return "%s - %s" % (self.template.name ,self.name)




@receiver(post_delete, sender=MatterObject)
def object_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.stl_file:
        if os.path.isfile(instance.stl_file.path):
            os.remove(instance.stl_file.path)
            instance.stl_file.delete(False)

    instance.scad_file.delete(False)
