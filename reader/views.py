from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pathlib import Path
import shutil

from . import formulas
from .models import RegAcceso, Registro

import datetime
import os
import zipfile


def get_carpeta():
    archivo_path = os.path.join(settings.TEMP_ROOT, 'ultima_carpeta.txt')
    with open(archivo_path, "r") as f:
        carpeta = f.readlines()

    return Path(carpeta[0])


@login_required
def siradig_view(request):
    listado = {}
    query_historia = RegAcceso.objects.filter(reg_user=request.user)

    if request.method == 'POST' and request.FILES.get('upload'):
        # TODO: Validar form
        listado = lista_zip(request.FILES['upload'])
        dire = lista_zip_ex(request.FILES['upload'])
        archivo_path = os.path.join(settings.TEMP_ROOT, 'ultima_carpeta.txt')
        with open(archivo_path, 'w') as f:
            f.write(dire)

    else:
        # Borro los archivos en carpeta temporal
        clean_folder(settings.TEMP_ROOT)

    my_context = {
        'listado': listado,
        'query_historia': query_historia,
    }

    return render(request, 'reader/home.html', my_context)


@login_required
def archivo_solo_view(request, slug):
    # TODO: Agregar validaciones de archivos
    dd = os.path.join(get_carpeta(), slug)
    matsolo = formulas.LeeXML(dd)

    context = {
        'titulo': slug[:11],
        'matsolo': matsolo
    }

    return render(request, 'reader/soloxml.html', context)


@login_required
def procesa_view(request, *args, **kwargs):

    todotodo = formulas.LeeCarpetaXML(get_carpeta())

    file_name = formulas.MatToExc(todotodo)
    url_to_file = os.path.join(settings.TEMP_URL, file_name)

    my_context = {
        'archproc': len(todotodo),
        'url_to_file': url_to_file
    }

    # Registro en BD
    # Grabo el registro único si no existe
    registro = RegAcceso(reg_user=request.user)
    registro.save()

    # Grabo cada uno de los registro
    for informacion in todotodo:
        this_registro = Registro(id_reg=registro,
                                 cuil=informacion[0],
                                 deduccion=informacion[1],
                                 tipo=informacion[2],
                                 dato1=informacion[3],
                                 dato2=informacion[4],
                                 porc=informacion[5])
        this_registro.save()

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


def clean_folder(path_to_folder):
    for path in Path(path_to_folder).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
