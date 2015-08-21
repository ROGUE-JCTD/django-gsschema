# -*- coding: utf-8 -*-
import httplib
import time
import base64
import json
import os

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils._os import safe_join
from django.views.static import serve
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from lxml import etree

@login_required
def index(request):
    # Render list page with the documents and the form
    return render_to_response(
        'gsschema/index.html',
        context_instance=RequestContext(request)
    )


@login_required
def download(request, layer):
    if layer:
        workspace, datastore = get_layer_info(request, layer)
        filename = '{}/workspaces/{}/{}/{}/schema.xsd'.format(get_gsschema_dir(), workspace, datastore, layer)
        filename = os.path.abspath(filename)
        if os.path.isfile(filename):
            response = serve(request, os.path.basename(filename), os.path.dirname(filename))
            response['Content-Disposition'] = 'attachment; filename="{}.xsd"'.format(layer)
            return response
        response = HttpResponse('Error - no schema file previously uploaded for layer: {}'.format(layer))
    elif layer is None:
        response = HttpResponse('Error - layer parameter not provided')
    else:
        response = HttpResponse('Error - layer name referred to by typeName parameter not found: {}'.format(layer))
    return response


@login_required
def describe(request, layer):
    if layer:
        print '----[ describe'
        res = describe_layer(request, layer)
        response = HttpResponse(res, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="{}_describe.xsd"'.format(layer)
    elif layer is None:
        response = HttpResponse('typeName parameter not provided')
    else:
        response = HttpResponse('layer name referred to by typeName parameter not found: {}'.format(layer))
    return response

@login_required
def remove(request, layer):
    if layer:
        workspace, datastore = get_layer_info(request, layer)
        filename = '{}/workspaces/{}/{}/{}/schema.xsd'.format(get_gsschema_dir(), workspace, datastore, layer)
        filename = os.path.abspath(filename)
        if os.path.exists(filename):
            try:
                os.remove(filename)
                response = HttpResponse('Successful removal of {}!'.format(layer))
            except OSError as e:
                response = HttpResponse('Error - {}'.format(e.message))
                pass
        else:
            response = HttpResponse('Error - File {}/schema.xsd does not exist'.format(layer))
    else:
        response = HttpResponse('Error - Layer returned null: {}'.format(layer))
    return response

@login_required
def upload(request, layer):
    # Handle file upload
    response = HttpResponse('Error - Upload request not POST')
    if request.method == 'POST':
        workspace, datastore = get_layer_info(request, layer)

        if workspace and datastore:
            filename = 'workspaces/{}/{}/{}/schema.xsd'.format(workspace, datastore, layer)
            filename_absolute = safe_join(get_gsschema_dir(), filename)
            print filename_absolute
            # if there is already and xsd file there, back it up first.
            backup_millis = int(round(time.time() * 1000))
            try:
                os.rename(filename_absolute, '{}_{}'.format(filename_absolute, backup_millis))
            except OSError:
                pass

            file_storage = FileSystemStorage(location=get_gsschema_dir())
            file_storage.file_permissions_mode = 0644
            uploaded_file = request.FILES['file']
            try:
                etree.parse(uploaded_file)
            except etree.XMLSyntaxError as error:
                response = HttpResponse('Error - XML not valid: {}'.format(error.message))
            else:
                file_storage.save(filename, uploaded_file)
                response = HttpResponse('upload completed for layer: {}'.format(layer))

    return response


def get_layers_as_admin(request):
    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(request)
    conn.request("GET", "/geoserver/rest/layers.json", None, headers)
    conn.set_debuglevel(1)
    r1 = conn.getresponse()
    print r1.status, r1.reason

    layers = []
    resp_obj = json.loads(r1.read())
    if resp_obj and resp_obj.get('layers', None):
        for layer in resp_obj['layers'].get('layer', None):
            print layer.get('name', '{ No Name }')
            layers.append(layer.get('name', '{ No Name }'))
    return layers


def get_layer_info(request, layer):
    workspace = None
    datastore = None

    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(request)
    conn.request("GET", "/geoserver/rest/layers/{}.json".format(layer), None, headers)
    r1 = conn.getresponse()
    print r1.status, r1.reason

    resp_obj = json.loads(r1.read())
    href_path = 'layer.resource.href'
    href = reduce(dict.get, href_path.split('.'), resp_obj)
    if href:
        tokes = href.split('/')
        if len(tokes) == 11:
            workspace = tokes[6]
            datastore = tokes[8]

    return workspace, datastore


def describe_layer(request, layer):
    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(request)
    conn.request("GET", "/geoserver/wfs?version=1.1.0&request=DescribeFeatureType&typeName={}".format(layer), None, headers)
    return conn.getresponse().read()


def get_connection(request):
    url_tokens = request.META['HTTP_REFERER'].split('/')
    protocol = url_tokens[0]
    if protocol.lower() == 'https:':
        conn = httplib.HTTPSConnection(url_tokens[2])
    else:
        conn = httplib.HTTPConnection(url_tokens[2])
    return conn

"""
example settings file
GSSCHEMA_CONFIG = {
    'gsschema_dir': '/var/lib/geoserver_data'
}
"""
def get_gsschema_dir():
    conf = getattr(settings, 'GSSCHEMA_CONFIG', {})
    return conf.get('gsschema_dir', './')