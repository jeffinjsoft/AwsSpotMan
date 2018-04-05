from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

from django.core.management import call_command

import json
import datetime

from dashboard.models import Schedule


def cron_to_time(c):
    """
    take cron exp as string and output the date time format

    return {'minute':'','hour':'','day':'','week':'','month':''}
    """
    spl = c.split(" ")
    day = // need to find if its * or not
    out = {
        'minute':int(spl[0]),
        'hour':int(spl[1]),
        'day':int(spl[2]),
        'month':int(spl[3]),
        'week':int(spl[4]),
    }


def cur_time():
    """
    return the current time in format

    return {'minute':'','hour':'','day':'','week':'','month':'','year'}
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    n = datetime.datetime.today().weekday()
    spl = now.split("-")
    out = {
        'minute':spl[4],
        'hour':spl[3],
        'day':spl[2],
        'week':n,
        'month':spl[1],
    }

    return out


def check_times(now,cron):
    """
    Check the both times in dict and return true if time matches cron
    """
    pass

def do_action(action,stack):
    """
    Do the action which scheduled for that stack
    """
    out = {
        'status':'',
        'message:''
    }

    if action == 'start':
        """
        refer view start
        """
        pass

        # return out
    elif action == 'stop':
        """
        refer
         stop
        """
        pass

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
        print cu_out

        sc = Schedule.objects.all()
        for i in sc:
            c_out = cron_to_time(i.cron)
            if check_times(cu_out,c_out):
                action = do_action(i.action,i.stack)
                if action['status'] == 'success':
                    print i.stack.id
                else:
                    print action['message']


        result = {'message': "Successfully completd cron"}
        return json.dumps(result)
