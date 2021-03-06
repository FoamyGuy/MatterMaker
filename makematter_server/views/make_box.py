import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.http import HttpResponse
from django.template import Template, Context

from django.template.loader import render_to_string
from makematter_server.models import MatterObject, MatterTemplate, MatterTemplateVar
from makematter_server.app_settings import MEDIA_ROOT, WORKING_DIR




def make_box(request):
    """
    l = request.GET.get('l')
    w = request.GET.get('w')
    t = request.GET.get('t')

    lid = request.GET.get('lid') == "true"
    box = request.GET.get('box') == "true"
    """

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

    #print(obj.uuid)

    template = MatterTemplate.objects.get(name="Basic Box")

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

    """
    scad_str = render_to_string(box_template,
                               {'length':l,
                                'width':w,
                                'thickness':t,
                                'text':text,
                                'box': box,
                                'lid': lid})

    """

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
    os.remove(os.path.join(WORKING_DIR, '%s.stl' % obj.uuid))
    os.remove(os.path.join(WORKING_DIR, '%s.scad' % obj.uuid))
    print stl_url
    return HttpResponse(stl_url)
