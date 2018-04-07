from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

from django.core.management import call_command

import json
import datetime

from dashboard.models import Schedule,Stacks
from dashboard.helper import spot_request,cancel_spot_request,terminate_instance


def cron_to_time(c):
    """
    take cron exp as string and output the date time format

    return {'minute':'','hour':'','day':'','week':'','month':''}
    """
    spl = c.split(" ")

    if spl[0] == '*':
        mi = range(1,61)
    else:
        mi = [spl[0]]

    if spl[1] == '*':
        hour = range(1,25)
    else:
        hour = [spl[1]]

    if spl[2] == '*':
        day = range(1,32)
    else:
        day = [spl[0]]

    if spl[3] == '*':
        month = range(1,13)
    else:
        month = [spl[3]]

    if spl[4] == '*':
        week = range(1,13)
    else:
        week = [spl[4]]

    out = {
        'minute':mi,
        'hour':hour,
        'day':day,
        'month':month,
        'week':week,
    }

    return out


def cur_time():
    """
    return the current time in format

    return {'minute':'','hour':'','day':'','week':'','month':'','year'}
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    n = datetime.datetime.today().weekday()
    spl = now.split("-")
    out = {
        'minute':int(spl[4]),
        'hour':int(spl[3]),
        'day':int(spl[2]),
        'week':n+1,
        'month':int(spl[1]),
    }

    return out


def check_times(now,cron):
    """
    Check the both times in dict and return true if time matches cron
    """
    # print now,cron

    if now['minute'] in cron['minute'] and now['hour'] in cron['hour'] and now['day'] in cron['day'] and now['month'] in cron['month'] and now['week'] in cron['week']:
        print 'Cron matched'
        return True
    else:
        return False

def do_action(action,stack):
    """
    Do the action which scheduled for that stack
    """
    out = {
        'status':'',
        'message':''
    }

    if action == 'start':
        """
        refer view start
        """

        ##  start stack

        s = Stacks.objects.get(id=stack.id)
        s.instance_id = 'null'
        arg = {'ami':s.ami,
                 'instanceprofile': s.instance_profile,
                 'instancetype': s.instancetype,
                 'keypair': s.keypair,
                 'public_ip': s.public_ip,
                 'region': s.region,
                 'sg_group': s.securitygroup,
                 'spotprice': s.max_spot,
                 'userdata': s.userdata,
                 'vpc': s.vpc}

        # print arg

        response = spot_request(arg)


        if response['status'] != 'success':

            s.request_id=response['out']
            s.status_code=response['code']
            s.deleted = 'no'
            s.save()

            out = {
                'status':'success',
                'message':'started'
            }

            return out
        else:
            out = {
                'status':'error',
                'message':response['out']
            }

            return out



        # return out
    elif action == 'stop':
        """
        refer
         stop
        """
        ##  stop stack

        s = Stacks.objects.get(id=stack.id)
        s_o = cancel_spot_request(s.request_id)
        if s_o['status'] == 'success':
            t_out = terminate_instance(s.instance_id)
            if t_out['status'] == 'fail':
                out = {
                    'status':'fail',
                    'message':t_out['message']
                }

                return out
            else:
                s.deleted = 'yes'
                s.status = 'Terminated'
                s.save()

                out = {
                    'status':'success',
                    'message':'stopped'
                }

                return out
        else:
            out = {
                'status':'error',
                'message':s_o['message']
            }

            return out


        # return out
    else:
        out['status'] = 'error'
        out['message'] = 'Action is not valid, delete this schedule'

        return out




class Command(BaseCommand):


    help = 'Check for cron and start/stop stacks'



    def handle(self, *args, **options):
        # Your Code

        cu_out = cur_time()
        # print cu_out

        sc = Schedule.objects.all()
        for i in sc:
            c_out = cron_to_time(i.cron)
            # print c_out
            if check_times(cu_out,c_out):
                action = do_action(i.action,i.stack)
                if action['status'] == 'success':
                    print "completd %s --> %s"%(i.action,i.stack.name)
                else:
                    print action['message']
            else:
                print 'No cron matched now'
