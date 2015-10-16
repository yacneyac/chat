#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: 
Author: 'yac'
Date: 
"""
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render

from chat.socket_chat import *

def chat(request):
    """ Namespace for websocket """
    return render_to_response('chat.html', context_instance=RequestContext(request))

def logout_user(request):
    """ Logout user and redirect to main page """
    logout(request)
    return redirect('/')

def auth_and_login(request):
    """ Authenticating user and login """
    post = request.POST
    if post:

        if not post['username'] or not post['password']:
            return json_response({'success': False, 'errorMessage': 'empty login/password'})

        user = authenticate(username=post['username'], password=post['password'])
        if user is None:
            return json_response({'success': False, 'errorMessage': 'incorrect login/password'})

        # auth user
        login(request, user)
        return json_response({'success': True})

    return redirect('/')

def create_user(username, password):
    """ Create user """
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    """ Check if user exist in DB """
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def sign_up_in(request):
    """ Sign up user """
    post = request.POST

    context = RequestContext(request)

    if post:
        if user_exists(post['username']):
            return json_response({'success': False, 'errorMessage': 'username exist'})

        create_user(username=post['username'], password=post['password'])
        return json_response({'success': True})

    else:
        return render_to_response('login.html', context_instance=context)

def json_response(data):
    """ Response json format """
    return HttpResponse(json.dumps(data), content_type="application/json")

def error404(request):
    """ Handler for 404 """
    return render(request,'404.html', status=404)

def error500(request):
    """ Handler for 500 """
    return render(request,'500.html', status=500)