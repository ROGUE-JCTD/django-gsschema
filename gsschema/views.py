# -*- coding: utf-8 -*-
import httplib
import time
import base64
import json
import os

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils._os import safe_join
from django.core.files.storage import default_storage
from django.views.static import serve
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from gsschema.forms import DocumentForm

@login_required
def index(request):
    # An empty, unbound form
    file_upload_form = DocumentForm()

    # Render list page with the documents and the form
    return render_to_response(
        'gsschema/index.html',
        {
            'layers': get_layers()
        },
        context_instance=RequestContext(request)
    )


@login_required
def download(request, layer):
    if layer:
        workspace, datastore = get_layer_info(layer)
        filename = '{}/workspaces/{}/{}/{}/schema.xsd'.format(settings.MEDIA_ROOT, workspace, datastore, layer)
        filename = os.path.abspath(filename)
        if os.path.isfile(filename):
            response = serve(request, os.path.basename(filename), os.path.dirname(filename))
            response['Content-Disposition'] = 'attachment; filename="{}.xsd"'.format(layer)
            return response
        response = HttpResponse('no schema file previously uploaded for layer: {}'.format(layer))
    elif layer is None:
        response = HttpResponse('typeName parameter not provided')
    else:
        response = HttpResponse('layer name refered to by typeName parameter not found: {}'.format(layer))
    return response


@login_required
def describe(request, layer):
    if layer:
        print '----[ describe'
        res = describe_layer(layer)
        response = HttpResponse(res, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="{}_describe.xsd"'.format(layer)
    elif layer is None:
        response = HttpResponse('typeName parameter not provided')
    else:
        response = HttpResponse('layer name refered to by typeName parameter not found: {}'.format(layer))
    return response


@login_required
def upload(request, layer):
    # Handle file upload
    if request.method == 'POST':
        workspace, datastore = get_layer_info(layer)

        if workspace and datastore:
            filename = 'workspaces/{}/{}/{}/schema.xsd'.format(workspace, datastore, layer)
            filename_absolute = safe_join(settings.MEDIA_ROOT, filename)
            # if there is already and xsd file there, back it up first.
            backup_millis = int(round(time.time() * 1000))
            try:
                os.rename(filename_absolute, '{}_{}'.format(filename_absolute, backup_millis))
            except OSError:
                pass
            default_storage.save(filename, request.FILES['file'])

        response = HttpResponse('upload completed for layer: {}'.format(layer))
    return response


def get_layers():
    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(settings.SITEURL)
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


def get_layer_info(layer):
    workspace = None
    datastore = None

    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(settings.SITEURL)
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


def describe_layer(layer):
    username = settings.OGC_SERVER['default']['USER']
    password = settings.OGC_SERVER['default']['PASSWORD']
    auth = base64.encodestring('{}:{}'.format(username, password)).replace('\n', '')
    headers = {"Authorization": "Basic {}".format(auth)}
    conn = get_connection(settings.SITEURL)
    conn.request("GET", "/geoserver/wfs?version=1.1.0&request=DescribeFeatureType&typeName={}".format(layer), None, headers)
    r1 = conn.getresponse()
    print r1.status, r1.reason
    return r1.read()


def get_connection(site_url):
    urls_tokens = site_url.split('/')
    protocol = urls_tokens[0]
    conn = None
    if protocol.lower() == 'http:':
        conn = httplib.HTTPConnection(urls_tokens[2])
    elif protocol.lower() == 'https:':
        conn = httplib.HTTPSConnection(urls_tokens[2])
    return conn