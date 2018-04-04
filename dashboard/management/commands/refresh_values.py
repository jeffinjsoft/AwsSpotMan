from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

from django.core.management import call_command

import json

from boto3_helper import check_amis,check_profiles,check_types,check_keys,check_regions,check_sgs,check_vpcs

all_options = ['amis','profiles','types','keys','regions','sgs','vpcs']

def check_v(options):
    o_l = []
    if options['check'] == 'all':
        print 'Checking all choices'
        o_l = all_options
    else:
        o_l = options['check'].split(',')
        for i in o_l:
            if i not in all_options:
                raise CommandError('option -->'+i+' <--not found in options')

    # print o_l

    if 'amis' in o_l:
        if options['accnt_id'] == "Null":
            raise CommandError('Please provide account id for this')
        else:
            check_amis(options['accnt_id'])
    if 'profiles' in o_l:
        check_profiles()

    if 'types' in o_l:
        check_types()
    if 'keys' in o_l:
        check_keys()
    if 'regions' in o_l:
        check_regions()
    if 'sgs' in o_l:
        check_sgs()
    if 'vpcs' in o_l:
        check_vpcs()

class Command(BaseCommand):


    help = 'recheck for all db values(boto3)'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
        '-c', '--check',
        dest="check",
        default='all',
        help="use to find all choice"
    )

        parser.add_argument(
        '-a', '--accnt',
        dest="accnt_id",
        default='Null',
        help="please use this for amis"
    )

    def handle(self, *args, **options):
        # Your Code

        try:
            check_v(options)
            print 'Command Completed'
        except Exception as e:
            print e

        # result = {'message': "Successfully Loading initial data"}
        # return json.dumps(result)
