from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import formulas
from .forms import UploadFileForm
from .models import RegAccesos

import datetime
import os
import zipfile


def ceci_view(request):
    return redirect("http://ceciliaprados.com.ar/")


@login_required
def siradig_view(request):
    listado = {}
    dire = ""
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            listado = lista_zip(request.FILES['file'])
            dire = lista_zip_ex(request.FILES['file'])

            # Grabo el registro
            reg1 = RegAccesos(fecha=datetime.datetime.now(), carpeta=dire, autenticado=False)
            reg1.save()

        else:
            # TODO: log errores
            print(form.errors)
    else:
        form = UploadFileForm()

    my_context = {
        'form': form,
        'listado': listado,
        'dire': dire,
    }

    return render(request, 'reader/siradig.html', my_context)


@login_required
def archivo_solo_view(request, slug):
    # print(slug)

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

    # Por ahora no grabo en la BD
    # MatToBD(todotodo, str(get_ult_reg().id))
    opath = formulas.MatToExc(todotodo)
    # opath2 = opath
    # AbrirExcel(opath)

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

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dirx = os.path.join(os.path.join(BASE_DIR, "temp"), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    zf.extractall(path=dirx)

    return dirx
