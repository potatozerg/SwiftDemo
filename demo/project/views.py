from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .adapter import *

def index(request):
    if request.method == "GET":
        return render(request, 'project/index.html')
    elif request.method == "POST":
        project_name = request.POST['project_name']
        user_name = request.POST['user_name']
        password = request.POST['password']
        token = login(user_name, password, project_name)
        request.session["token"] = token
        if token:
            return HttpResponseRedirect(reverse('project:container'))
        else:
            error_msg = "Wrong Combination of username and password"
            messages.error(request, error_msg)
            return HttpResponseRedirect(reverse('project:index'))


def logout(request):
    if request.method == "POST":
        request.session['token'] = None
        return HttpResponseRedirect(reverse('project:index'))


def container_list(request):
    if request.method == "GET" and request.session["token"]:
        # 账号密码验证
        containers_list = get_containers_list(request.session["token"])
        context = {"container_list": containers_list}
        return render(request, 'project/container_list.html', context)


def add_container(request):
    if request.session["token"]:
        if request.method == "GET" and request.session["token"]:
            return render(request, 'project/add_container.html')
        elif request.method == "POST" and request.session["token"]:
            create_container(request.session['token'], request.POST["container_name"])
            return HttpResponseRedirect(reverse('project:container'))
    else:
        error_msg = "Wrong Combination of username and password"
        messages.error(request, error_msg)
        return HttpResponseRedirect(reverse('project:index'))


def remove_container(request):
    if request.method == "POST" and request.session["token"]:
        token = request.session['token']
        container_name = request.POST["container"]
        if get_container_details(token, container_name) == []:
            delete_container(token, container_name)
            return HttpResponseRedirect(reverse('project:container'))
        else:
            return render(request, 'project/remove_container.html')


def container_detail(request, container_name):
    if request.method == "GET" and request.session["token"]:
        content_list = get_container_details(request.session["token"], container_name)
        context = {"container_name": container_name,
                   "content_list": content_list}
        return render(request, 'project/container_detail.html', context)


def add_container_content(request, container_name):
    if request.method == "GET" and request.session["token"]:
        return render(request, 'project/add_container_content.html')
    elif request.method == "POST" and request.session["token"]:
        if 'file' in request.FILES and request.FILES['file']:
            token = request.session["token"]
            file = request.FILES['file']
            create_object(token, container_name, file._name, file)
            return HttpResponseRedirect(reverse('project:container_detail', args=(container_name,)))
        else:
            messages.error(request, "Please select a file")
            return render(request, 'project/add_container_content.html')


def remove_container_content(request):
    if request.method == "POST" and request.session["token"]:
        token = request.session['token']
        container_name = request.POST["container"]
        content_name = request.POST["content"]

        delete_object(token, container_name, content_name)
        return HttpResponseRedirect(reverse('project:container_detail', args=(container_name,)))


def get_content_temp_url(request, container_name, file_name):
    if request.method == "GET" and request.session["token"]:
        token = request.session["token"]
        url = get_object_content_temp(token, container_name, file_name)
        context = {"url": url}
        return render(request, 'project/container_content_temp_url.html', context)
