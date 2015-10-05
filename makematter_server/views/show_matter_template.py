from django.shortcuts import render_to_response
from makematter_server.models import MatterTemplate, MatterTemplateVar


def show_matter_template(request, uuid):
    template = MatterTemplate.objects.get(uuid=uuid)

    template_vars = MatterTemplateVar.objects.filter(template=template)

    for var in template_vars:
        print("%s - %s" % (var.name, var.type))

    return render_to_response("matter_template_viewer.html",
                              {'matter_template_vars': template_vars,
                               'matter_template': template})
