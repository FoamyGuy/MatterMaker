from django.http import HttpResponse
import time
from makematter_server.models import MatterTemplate

import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.http import HttpResponse
from django.template import Template, Context

from django.template.loader import render_to_string
from makematter_server.models import MatterObject, MatterTemplate, MatterTemplateVar
from makematter_server.settings import MEDIA_ROOT, WORKING_DIR


def render_matter_template(request, uuid):
    template = MatterTemplate.objects.get(uuid=uuid)


    key = request.GET.get('key')
    print(key)
    try:
        obj = MatterObject.objects.get(uuid=key)

    except ObjectDoesNotExist:
        obj = MatterObject()

    if request.GET.get("text"):
        text = request.GET.get("text")
    else:
        text = ""

    box_template_code = template.template_str

    template_vars = MatterTemplateVar.objects.filter(template=template)

    # build context:
    ctx_dict = {}
    for var in template_vars:
        if var.type == "str" or var.type == "int":
            ctx_dict[var.name] = request.GET.get(var.name)
        elif var.type == "bool":
            ctx_dict[var.name] = request.GET.get(var.name) == "true"

    print ctx_dict

    box_template = Template(box_template_code)

    ctx = Context(ctx_dict)

    scad_str = box_template.render(ctx)


    f = open(os.path.join(WORKING_DIR, '%s.scad' % obj.uuid), 'w+')
    f.write(scad_str)
    f.close()
    f = open(os.path.join(WORKING_DIR, '%s.scad' % obj.uuid), 'rb')

    if obj.scad_file.name:
        print("scad file already exists")
        obj.scad_file.file.open()
        obj.scad_file.close()
        obj.scad_file.open(mode="w")
        scad_str_in = f.read()
        obj.scad_file.write(scad_str_in)
    else:
        print("making scad file")
        obj.scad_file = File(f)
        print("created scad file name: %s" % obj.scad_file.name)

    obj.save()
    f.close()
    obj.scad_file.close()

    os_cmd_str = "openscad -o %s %s" % (os.path.join(WORKING_DIR, '%s.stl' % obj.uuid), os.path.join(WORKING_DIR, '%s.scad' % obj.uuid))

    os.system(os_cmd_str)
    file_is_ready = False
    while not file_is_ready:
        try:
            tmp_f = open(os.path.join(WORKING_DIR, '%s.stl' % obj.uuid), 'rb')
            tmp_f.close()
            file_is_ready = True
        except IOError:
            # Not Ready yet, try again in a sec
            time.sleep(.1)
            pass

    f = open(os.path.join(WORKING_DIR, '%s.stl' % obj.uuid), 'rb')

    if obj.stl_file.name:
        obj.stl_file.open()
        obj.stl_file.close()
        obj.stl_file.open(mode="w")
        stl_str_in = f.read()
        obj.stl_file.write(stl_str_in)
    else:
        obj.stl_file = File(f)

    obj.save()
    f.close()
    obj.stl_file.close()

    stl_url = obj.stl_file.url
    time.sleep(.5)

    os.remove(os.path.join(WORKING_DIR, '%s.scad' % obj.uuid))
    os.remove(os.path.join(WORKING_DIR, '%s.stl' % obj.uuid))
    print stl_url
    return HttpResponse(stl_url)

