# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Stacks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    region = models.CharField(max_length=20)
    vpc = models.CharField(max_length=50)
    keypair = models.CharField(max_length=50)
    securitygroup = models.CharField(max_length=50)
    ami = models.CharField(max_length=50)
    userdata = models.CharField(max_length=500,default='',blank=True)
    instancetype = models.CharField(max_length=20)
    instance_profile = models.CharField(max_length=50)
    public_ip = models.CharField(max_length=20,default='no',blank=True)
    max_spot = models.CharField(max_length=20)
    request_id = models.CharField(max_length=20,default="null")
    instance_id = models.CharField(max_length=20,default="null")
    status = models.CharField(max_length=20,default='pending')
    status_code = models.CharField(max_length=20,default="null")
    deleted = models.CharField(max_length=20,default='no')
    ip = models.CharField(max_length=20,default="")
    eip = models.CharField(max_length=20,default="")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.name


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)

    stack = models.ForeignKey(Stacks, on_delete=models.CASCADE)
    cron = models.CharField(max_length=20)
    action = models.CharField(max_length=20)

    def __unicode__(self):
       return self.stack.name + "  " +self.action


class Vpc(models.Model):
    vpc_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)


    def __unicode__(self):
       return self.vpc_id

    def fullname(self):
        return str(self.vpc_id)+' | '+str(self.name)[:10]

class Sgroup(models.Model):
    sg_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    vpc = models.CharField(max_length=50)


    def __unicode__(self):
       return self.sg_id

    def fullname(self):
        return str(self.sg_id)+' | '+str(self.name)[:10]


class Ami(models.Model):
    ami_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __unicode__(self):
       return self.ami_id

    def fullname(self):
        return str(self.ami_id)+' | '+str(self.name)[:10]


class Volume(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='null')
    vid = models.CharField(max_length=50)
    instance_id = models.CharField(max_length=50,default='null')
    a_zone = models.CharField(max_length=50,default='null')
    snap_id = models.CharField(max_length=50,default='null')
    state = models.CharField(max_length=50,default='available')





    def __unicode__(self):
       return self.vid

    def fullname(self):
        return str(self.vid)+' | '+str(self.name)[:10]



class Eip(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    inter_id = models.CharField(max_length=50)


    def __unicode__(self):
       return self.ip


class InstanceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


    def __unicode__(self):
       return self.name

class InstanceProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    arn = models.CharField(max_length=50)


    def __unicode__(self):
       return self.name

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


    def __unicode__(self):
       return self.name

class Keypair(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


    def __unicode__(self):
       return self.name
