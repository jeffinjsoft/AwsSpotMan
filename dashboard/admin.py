# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from . import models
admin.site.register(models.Stacks)
admin.site.register(models.Vpc)
admin.site.register(models.Sgroup)
admin.site.register(models.InstanceType)
admin.site.register(models.Ami)
admin.site.register(models.InstanceProfile)
admin.site.register(models.Keypair)
admin.site.register(models.Region)
admin.site.register(models.Schedule)
