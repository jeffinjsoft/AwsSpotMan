import string
import random
import base64

from .forms import StackForm
from . import models

import boto3
from botocore.exceptions import ClientError


def get_stack_choices():
    form = StackForm()
    list = []
    vpcs = models.Vpc.objects.all()
    vpc_list = [v.fullname for v in vpcs]
    regions = models.Region.objects.all()
    region_list = [r.name for r in regions]
    sgs = models.Sgroup.objects.all()
    sgs_list = [r.fullname for r in sgs]
    keys = models.Keypair.objects.all()
    keys_list = [r.name for r in keys]
    amis = models.Ami.objects.all()
    ami_list = [r.fullname for r in amis]
    inst = models.InstanceType.objects.all()
    inst_list = [r.name for r in inst]
    inst_p = models.InstanceProfile.objects.all()
    inst_p_list = [r.name for r in inst_p]

    eip = models.Eip.objects.all()
    eips = [r.ip for r in eip]
    v = models.Volume.objects.all()
    volumes = [r.vid for r in v]

    choice = {}
    choice['form'] = form
    choice['region'] = region_list
    choice['sg_groups'] = sgs_list
    choice['vpcs'] = vpc_list
    choice['keypairs'] = keys_list
    choice['amis'] = ami_list
    choice['instance_type'] = inst_list
    choice['instance_profile'] = inst_p_list
    choice['eips'] = eips
    choice['volumes'] = volumes
    return choice



def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_avz():
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_availability_zones()
    except ClientError as e:
        print e
    return response['AvailabilityZones'][0]['ZoneName']

def get_spot_price(ty,az='eu-west-1a'):

    try:
        client=boto3.client('ec2')
        prices=client.describe_spot_price_history(InstanceTypes=[ty],MaxResults=1,ProductDescriptions=['Linux/UNIX (Amazon VPC)'],AvailabilityZone=az)
    except ClientError as e:
        print e

    if len(prices['SpotPriceHistory']) == 0:
        p = {'status':'error','message':'no proce history'}
        return p

    p = {'price':prices['SpotPriceHistory'][0]['SpotPrice'],'status':'success'}
    return p

def get_spot_id_status(r_id):
    out = {}
    try:
        client=boto3.client('ec2')
        response = client.describe_spot_instance_requests(SpotInstanceRequestIds=[str(r_id)])
        out['status'] = 'success'
        out['message'] = response['SpotInstanceRequests'][0]['Status']['Code']
        out['code'] = response['SpotInstanceRequests'][0]['Status']['Code']
        if 'InstanceId' in response['SpotInstanceRequests'][0].keys():
            out['i_id'] = response['SpotInstanceRequests'][0]['InstanceId']
        else:
            out['i_id'] = 'null'
    except ClientError as e:
        out['status'] = 'error'
        out['message'] = e
    return out


def cancel_spot_request(spot_re_id):
    out = {}
    try:
        client=boto3.client('ec2')
        response = client.cancel_spot_instance_requests(SpotInstanceRequestIds=[spot_re_id])

        if response['CancelledSpotInstanceRequests'][0]['State'] == 'cancelled':
            out['status'] = 'success'
        else:
            out['status'] = 'fail'
            out['message'] = response['CancelledSpotInstanceRequests'][0]['State']
    except ClientError as e:
        out['status'] = 'fail'
        out['message'] = e
        print e
    return out

def terminate_instance(in_id):
    out = {}
    if in_id == 'null':
        out['status'] = 'error'
        out['message'] = 'instance id null'
    try:
        client=boto3.client('ec2')
        response = client.terminate_instances(InstanceIds=[in_id])
        out['status'] = 'success'

    except ClientError as e:
        print e
        out['status'] = 'fail'
        out['message'] = e
    return out

def spot_request(arg):

    spot_out = {}
    """
    Need to add BlockDurationMinutes
    EIP with network interface id NetworkInterfaceId
    'PrivateIpAddresses'

    """
    #
    # spot_out['status'] = 'error'
    # spot_out['out'] = 'access error'
    # return spot_out

    ## pre checks before request
    required_keys = ['sg_group','instanceprofile','ami','instancetype','keypair','spotprice']
    for r in required_keys:
        if r not in arg.keys():
            spot_out['status'] = 'error'
            spot_out['out'] = 'required_keys not found -->'+r
            return spot_out

    vpc = arg['vpc'].split('|')[0].strip()

    sg_id = str(arg['sg_group'].split('|')[0].strip())
    s_ids = [sg_id]
    ami = str(arg['ami'].split('|')[0].strip())
    b_encoded = base64.b64encode(arg['userdata'])

    c_s = models.Sgroup.objects.get(sg_id=sg_id)

    client=boto3.client('ec2')
    response = client.describe_subnets(Filters=[{'Name':'vpc-id','Values':[vpc]}])
    sub_id = response['Subnets'][0]['SubnetId']

    if c_s.vpc != vpc:
        spot_out['status'] = 'error'
        spot_out['out'] = 'security group is not in same vpc'
        return spot_out


    #checking the latest spot sprice
    az = get_avz()
    spot_price = get_spot_price(arg['instancetype'],az)

    if spot_price['status'] == 'success' and float(spot_price['price']) <= float(arg['spotprice']):

        client = boto3.client('ec2')
        l_s = {
            'NetworkInterfaces':[{'SubnetId':sub_id,'DeviceIndex':0,'Groups':s_ids}],
            'IamInstanceProfile': {
                'Name': arg['instanceprofile']
            },
            'ImageId': ami,
            'InstanceType':arg['instancetype'],
            'KeyName': arg['keypair'],
            'UserData': b_encoded
        }



        if arg['publicip'] == 'yes' or arg['publicip'] == 'no':
            if arg['publicip'] == 'yes':
                l_s['NetworkInterfaces'][0]['AssociatePublicIpAddress'] = True
            else:
                l_s['NetworkInterfaces'][0]['AssociatePublicIpAddress'] = False
        if arg['eip'] != '':
            """
            need to assosiate EIP after instance request
            """
            pass

        if arg['volume'] != '':
            print 'vol man'


        try:
            response = client.request_spot_instances(
                ClientToken=id_generator(),
                DryRun=False,
                InstanceCount=1,
                LaunchSpecification=l_s,
                SpotPrice=spot_price['price'],
            )
            print 'Requested'
            print response


        except ClientError as e:
            print 'in except'
            spot_out['status'] = 'error'
            spot_out['out'] = 'sport request exception :- %s' %e
            print "Unexpected error: %s" % e
            return spot_out

        spot_out['status'] = 'success'
        spot_out['out'] = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
        spot_out['message'] = response['SpotInstanceRequests'][0]['Status']['Message']
        spot_out['code'] = response['SpotInstanceRequests'][0]['Status']['Code']

        return spot_out
    else:
        if spot_price['status'] == 'error':
            spot_out['status'] = 'error'
            spot_out['out'] = spot_price['message']
            return spot_out

        spot_out['status'] = 'error'
        spot_out['out'] = 'spot price is grater for ' + arg['spotprice']
        return spot_out
