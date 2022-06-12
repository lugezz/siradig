from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import formulas
from .models import RegAcceso

import datetime
import os
import zipfile


@login_required
def siradig_view(request):
    listado = {}
    dire = ""
    if request.method == 'POST' and request.FILES.get('upload'):
        # TODO: Validar form
        listado = lista_zip(request.FILES['upload'])
        dire = lista_zip_ex(request.FILES['upload'])

        # Grabo el registro
        reg1 = RegAcceso(fecha=datetime.datetime.now(), carpeta=dire, autenticado=False)
        reg1.save()

    my_context = {
        'listado': listado,
        # 'dire': dire,
    }

    return render(request, 'reader/home.html', my_context)


@login_required
def archivo_solo_view(request, slug):
    dd = os.path.join(str(formulas.get_ult_reg().carpeta), slug)
    matsolo = formulas.LeeXML(dd)
    
    context = {
        'titulo': slug[:11],
        'matsolo': matsolo
    }

    return render(request, 'reader/soloxml.html', context)


@login_required
def procesa_view(request, *args, **kwargs):

    todotodo = formulas.LeeCarpetaXML(formulas.get_ult_reg().carpeta)
    archproc = (len(todotodo))

    # TODO: Registrar en BD
    opath = formulas.MatToExc(todotodo)
    if settings.DEBUG:
        opath = f'file:///{opath}'

    my_context = {
        'archproc': archproc,
        'opath': opath
    }

    return render(request, 'reader/procesa.html', my_context)


def lista_zip(arch):
    zf = zipfile.ZipFile(arch, "r")
    listz = zf.namelist

    return listz


def lista_zip_ex(arch):
    zf = zipfile.ZipFile(arch, "r")

    dirx = os.path.join(settings.TEMP_ROOT, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    zf.extractall(path=dirx)

    return dirx
