# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import StackForm
from .helper import get_stack_choices,spot_request,get_spot_id_status,cancel_spot_request,terminate_instance

from . import models

# Create your views here.

def home(request):
    return render(request, "dashboard/home.html", {})


@login_required(login_url='/login/')
def index(request):

    s = models.Stacks.objects.filter(deleted='no')
    no = s.count()
    return render(request, "dashboard/index.html", {'server':no})


@login_required(login_url='/login/')
def schedule_view(request):

    s = models.Schedule.objects.all()
    return render(request, "dashboard/schedule_view.html", {'schedules':s})


@login_required(login_url='/login/')
def schedule_add_new(request):
    if request.method == "POST":
        print request.POST['stack']
        s = models.Stacks.objects.get(id=request.POST['stack'])
        sc = models.Schedule(
            action=request.POST['action'],
            cron=request.POST['cron'],
            stack=s)
        sc.save()
        return HttpResponseRedirect("/dashboard/schedule/")


@login_required(login_url='/login/')
def schedule_add(request):

    s = models.Stacks.objects.all()

    return render(request, "dashboard/schedule_add.html", {'stacks':s})

@login_required(login_url='/login/')
def stacks(request):
    s = models.Stacks.objects.all()
    return render(request, "dashboard/stacks.html", {'stacks':s})

@login_required(login_url='/login/')
def stack_view(request,s_id):
    s = models.Stacks.objects.filter(id=s_id)
    return render(request, "dashboard/stack_view.html", {'stack':s})

@login_required(login_url='/login/')
def refresh_status(request,s_id):
    s = models.Stacks.objects.get(id=s_id)
    spot_status = get_spot_id_status(s.request_id)
    if spot_status['status'] == 'success':
        s.status = spot_status['message']
        s.instance_id = spot_status['i_id']
        s.status_code = spot_status['code']
        s.save()
        messages.success(request, 'Successfully Refreshed %s' %str(s_id))
    else:
        messages.warning(request, 'Error refresong %s -->%s' %(str(s_id),spot_status['message']))
    return HttpResponseRedirect("/dashboard/stacks/")

@login_required(login_url='/login/')
def stack_start(request,s_id):

    s = models.Stacks.objects.get(id=s_id)
    s.instance_id = 'null'
    arg = {'ami':s.ami,
             'instanceprofile': s.instance_profile,
             'instancetype': s.instancetype,
             'keypair': s.keypair,
             'publicip': s.public_ip,
             'region': s.region,
             'sg_group': s.securitygroup,
             'spotprice': s.max_spot,
             'userdata': s.userdata,
             'vpc': s.vpc,
             'eip': s.eip}

    # print arg

    response = spot_request(arg)


    if response['status'] != 'success':
        print response['out']
        msg = 'unable to add -->'+response['out']
        messages.warning(request, msg)
        return HttpResponseRedirect("/dashboard/stacks/")
    s.request_id=response['out']
    s.status_code=response['code']
    s.deleted = 'no'
    s.save()
    messages.success(request, 'Successfully Started')
    return HttpResponseRedirect("/dashboard/stacks/")

@login_required(login_url='/login/')
def stack_view_del(request,s_id):

    ## cancel spot request id and delete from DB
    try:
        s = models.Stacks.objects.get(id=s_id)
        s_o = cancel_spot_request(s.request_id)
        if s_o['status'] == 'success':
            t_out = terminate_instance(s.instance_id)
            if t_out['status'] == 'fail':
                messages.warning(request, t_o['message'])
            else:
                s.deleted = 'yes'
                s.status = 'Terminated'
                s.save()
                messages.success(request, 'Successfully terminated')
        else:
            messages.warning(request, s_o['message'])
    except:
        messages.warning(request, 'Error deleting stack')
    return HttpResponseRedirect("/dashboard/stacks/")

@login_required(login_url='/login/')
def stacks_add(request):
    if request.method == "POST":
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = StackForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                # arg = {}
                arg = form.cleaned_data
                # print arg
                # return HttpResponseRedirect("/dashboard/stacks/")
                arg['owner'] = request.user

                response = spot_request(arg)


                if response['status'] != 'success':
                    print response['out']
                    msg = 'unable to add -->'+response['out']
                    messages.warning(request, msg)
                    return HttpResponseRedirect("/dashboard/stacks/")


                try:
                    ## adding details to DB

                    s = models.Stacks(name=arg['name'],owner=arg['owner'],region=arg['region'],vpc=arg['vpc'],
                        keypair=arg['keypair'],securitygroup=arg['sg_group'],ami=arg['ami'],userdata=arg['userdata'],
                        instancetype=arg['instancetype'],instance_profile=arg['instanceprofile'],max_spot=arg['spotprice'],
                        public_ip=arg['publicip'],request_id=response['out'],status_code=response['code'])
                    s.save()
                    messages.success(request, response['message'])
                except:
                    # print 'db error'
                    messages.warning(request, 'Spot requested but unable to add due to DB')

                return HttpResponseRedirect("/dashboard/stacks/")
            else:

                CHOICES = get_stack_choices()
                form = StackForm(request.POST)
                form.is_valid()
                CHOICES['form'] = form
                return render(request, "dashboard/stacks_add.html", CHOICES)
    else:
        CHOICES = get_stack_choices()
        return render(request, "dashboard/stacks_add.html", CHOICES)
