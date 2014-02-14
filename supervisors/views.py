# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.template import RequestContext, loader
from models import Server

from supervisor.states import ProcessStates


def index(request):
    statuses = list()
    servers = Server.objects.all()
    for srv in servers:
        get_status = srv.get_status()
        if not get_status:
            continue
        for status in get_status:
            print status
            statuses.append( {'inst': srv.id,'state': status['statename'] } )

    template = loader.get_template('supervisors/index.html')
    context = RequestContext(request, {
        'statuses': statuses,
    })
    return HttpResponse(template.render(context))

def inst(request, server_id):
    server = Server.objects.filter(id=server_id)[0]
    status = server.get_status()
    print status
    ordered_status = list()
    template = loader.get_template('supervisors/inst.html')
    context = RequestContext(request, {
        'inst': server,
        'status': status,
    })
    return HttpResponse(template.render(context))

def action(request, server_id, action_name, process_name):
    server = Server.objects.filter(id=server_id)[0]
    server.perform_action(process_name,action_name)
    return HttpResponseRedirect('/supervisors/inst/%s/' % server_id)

