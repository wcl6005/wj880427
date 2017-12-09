# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from monthdelta import monthdelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Company, Material, Order
from django.contrib.auth.models import User, Group
import datetime
import os
import re
import tempfile
import uuid
import xlsxwriter
import json
def readJson(filepath):
    try:
        with open(filepath) as fp:        
            return json.load(fp)
    except Exception as ex:
        return str(ex)
    
def _getOperators():
    operators = Group.objects.get(name='Operator').user_set.all()
    return [user for user in User.objects.all() if user.is_superuser or user in operators]

