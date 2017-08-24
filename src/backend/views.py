# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import CreateAppForm, EditAppForm, ReleaseForm, \
        InstallationForm, MaintenanceForm, EditDetailsForm, \
        DownloadForm, DevelopmentForm
from django.apps import apps
from util.img_util import scale_img
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse

@login_required
def createApp(request):
    if request.user.is_staff:
        if request.method == 'GET':
            form = CreateAppForm()
        elif request.method == 'POST':
            form = CreateAppForm(request.POST)
            if form.is_valid():
                new_app = form.save()
                new_app.save()
                context = {
                    'message':"New App Page created Successfully!",
                    'go_back_to_url':"/app/"+new_app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/",
            'go_back_to_title':"Home Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'create.html', {'form':form})

@login_required
def editApp(request, num):
    App = apps.get_model('apps', 'App')
    try:
        edit_app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+edi_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    editors = edit_app.editors.all()
    if request.user in editors or request.user.is_staff:
        if request.method == 'GET':
            form = EditAppForm(instance=edit_app)
        elif request.method == 'POST':
            form = EditAppForm(request.POST, request.FILES, instance=edit_app)
            if form.is_valid():
                edited_app = form.save(commit=False)
                if 'icon' in request.FILES:
                    icon_file = request.FILES['icon']
                    edited_app.icon = scale_img(icon_file, icon_file.name, 128, 'both')
                edited_app.save()
                context = {
                    'message':"App Page edited Successfully!",
                    'go_back_to_url':"/app/"+edit_app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+edit_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'edit.html', {'form':form})

@login_required
def createRelease(request, num):
    App = apps.get_model('apps', 'App')
    try:
        release_app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+release_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    editors = release_app.editors.all()
    if request.user in editors or request.user.is_staff:
        if request.method == 'GET':
            form = ReleaseForm()
        elif request.method == 'POST':
            form = ReleaseForm(request.POST)
            if form.is_valid():
                new_release = form.save(commit=False)
                new_release.app = release_app
                new_release.save()
                context = {
                    'message':"Release added Successfully!",
                    'go_back_to_url':"/app/"+release_app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+release_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'create_release.html', {'form':form})

@login_required
def editRelease(request, num):
    Release = apps.get_model('apps', 'Release')
    App = apps.get_model('apps', 'App')
    try:
        edit_release = Release.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+edit_release.app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    editors = edit_release.app.editors.all()
    if request.user in editors or request.user.is_staff:
        if request.method == 'GET':
            form = ReleaseForm(instance=edit_release)
        elif request.method == 'POST':
            form = ReleaseForm(request.POST, instance=edit_release)
            if form.is_valid():
                edited_release = form.save()
                edited_release.save()
                context = {
                    'message':"Release edited Successfully!",
                    'go_back_to_url':"/app/"+edit_release.app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+edit_release.app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'edit_release.html', {'form':form})

@login_required
def modifyInstallation(request, num):
    existing = False
    App = apps.get_model('apps', 'App')
    Installation = apps.get_model('apps', 'Installation')
    try:
        app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    if Installation.objects.filter(app=app).exists():
        existing = True
        edit_installation = Installation.objects.get(app=app)
    if request.user.is_staff or request.user in app.editors.all():
        if request.method == 'GET':
            if existing:
                form = InstallationForm(instance=edit_installation)
            else:
                form = InstallationForm()
        elif request.method == 'POST':
            if existing:
                form = InstallationForm(request.POST, instance=edit_installation)
            else:
                form = InstallationForm(request.POST)
            if form.is_valid():
                if existing:
                    edited_installation = form.save()
                    edited_installation.save()
                else:
                    installation = form.save(commit=False)
                    installation.app = app
                    installation.save()
                context = {
                    'message':"Installation modified Successfully!",
                    'go_back_to_url':"/app/"+app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'installation.html', {'form':form})

@login_required
def modifyMaintenance(request, num):
    existing = False
    App = apps.get_model('apps', 'App')
    Maintenance = apps.get_model('apps', 'Maintenance')
    try:
        app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    if Maintenance.objects.filter(app=app).exists():
        existing = True
        edit_maintenance = Maintenance.objects.get(app=app)
    if request.user.is_staff or request.user in app.editors.all():
        if request.method == 'GET':
            if existing:
                form = MaintenanceForm(instance=edit_maintenance)
            else:
                form = MaintenanceForm()
        elif request.method == 'POST':
            if existing:
                form = MaintenanceForm(request.POST, instance=edit_maintenance)
            else:
                form = MaintenanceForm(request.POST)
            if form.is_valid():
                if existing:
                    edited_maintenance = form.save()
                    edited_maintenance.save()
                else:
                    maintenance = form.save(commit=False)
                    maintenance.app = app
                    maintenance.save()
                context = {
                    'message':"Maintenance notes modified Successfully!",
                    'go_back_to_url':"/app/"+app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'maintenance.html', {'form':form})

@login_required
def editDetails(request, num):
    App = apps.get_model('apps', 'App')
    try:
        edit_app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+edit_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    editors = edit_app.editors.all()
    if request.user in editors or request.user.is_staff:
        if request.method == 'GET':
            form = EditDetailsForm(instance=edit_app)
        elif request.method == 'POST':
            form = EditDetailsForm(request.POST, instance=edit_app)
            if form.is_valid():
                edited_app = form.save()
                edited_app.save()
                context = {
                    'message':"Edited Details Successfully!",
                    'go_back_to_url':"/app/"+edit_app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+edit_app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'edit_details.html', {'form':form})

@login_required
def modifyDownload(request, num):
    existing = False
    App = apps.get_model('apps', 'App')
    Download = apps.get_model('apps', 'Download')
    Release = apps.get_model('apps', 'Release')
    try:
        app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    if Download.objects.filter(app=app).exists():
        existing = True
        edit_download = Download.objects.get(app=app)
    if request.user.is_staff or request.user in app.editors.all():
        if request.method == 'GET':
            if existing:
                form = DownloadForm(instance=edit_download)
            else:
                form = DownloadForm()
        elif request.method == 'POST':
            if existing:
                form = DownloadForm(request.POST, instance=edit_download)
            else:
                form = DownloadForm(request.POST)
            if form.is_valid():
                if existing:
                    instance = form.save()
                    release = None
                    releases = Release.objects.filter(app=instance.app)
                    if releases:
                        release = releases.latest('date')
                    choice = instance.download_option
                    link = "https://ns-apps.washington.edu/"+instance.app.name+"/#cy-app-instructions-tab"
                    if choice == 'I':
                        instance.download_link = link
                    elif choice == 'D':
                        instance.download_link = release.url
                        if not release:
                            instance.download_link = link
                    elif choice == 'U':
                        instance.download_link = instance.external_url
                        if not instance.external_url:
                            instance.download_link = link
                    if not instance.default_release:
                        instance.default_release = release
                    print instance.download_link
                    instance.save()
                else:
                    download = form.save(commit=False)
                    download.app = app
                    download.save()
                context = {
                    'message':"Download Details modified Successfully!",
                    'go_back_to_url':"/app/"+app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'download.html', {'form':form})

@login_required
def modifyDevelopment(request, num):
    existing = False
    App = apps.get_model('apps', 'App')
    Development = apps.get_model('apps', 'Development')
    try:
        app = App.objects.get(id=num)
    except:
        context = {
            'message':"Requested App does not Exist!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    if Development.objects.filter(app=app).exists():
        existing = True
        edit_development = Development.objects.get(app=app)
    if request.user.is_staff or request.user in app.editors.all():
        if request.method == 'GET':
            if existing:
                form = DevelopmentForm(instance=edit_development)
            else:
                form = DevelopmentForm()
        elif request.method == 'POST':
            if existing:
                form = DevelopmentForm(request.POST, instance=edit_development)
            else:
                form = DevelopmentForm(request.POST)
            if form.is_valid():
                if existing:
                    edited_development = form.save()
                    edited_development.save()
                else:
                    development = form.save(commit=False)
                    development.app = app
                    development.save()
                context = {
                    'message':"Development Version modified Successfully!",
                    'go_back_to_url':"/app/"+app.name,
                    'go_back_to_title':"App Page",
                }
                return render(request, 'message.html', context)
    else:
        context = {
            'message':"You are not authorized to view this page!",
            'go_back_to_url':"/app/"+app.name,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)
    return render(request, 'development.html', {'form':form})

def deleteReleasePrompt(request, num):
    Release = apps.get_model('apps', 'Release')
    release = Release.objects.get(id=num)
    app = release.app
    go_back_to_url = "/app/"+app.name
    print app
    if request.user.is_staff or request.user in app.editors.all():
        context = {
            'release_id':num,
            'name':app.name,
            'go_back_to_url':go_back_to_url,
            'go_back_to_title':"App Page",
        }
        return render(request, 'prompt.html', context)
    else:
        message = "You are not authorized to view this page!"
        context = {
            'message':message,
            'go_back_to_url':go_back_to_url,
            'go_back_to_title':"App Page",
        }
        return render(request, 'message.html', context)

def deleteRelease(request, num):
    Release = apps.get_model('apps', 'Release')
    release = Release.objects.get(id=num)
    app = release.app
    if request.user.is_staff or request.user in app.editors.all():
        release.delete()
        message = "Release Deleted Successfully!"
    else:
        message = "You are not authorized to view this page!"
    go_back_to_url = "/app/"+app.name
    context = {
        'message':message,
        'go_back_to_url':go_back_to_url,
        'go_back_to_title':"App Page",
    }
    return render(request, 'message.html', context)
