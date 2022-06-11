import os
import xlsxwriter
import datetime
import xml.etree.ElementTree as ET
import subprocess
import sys

from .models import Registros, RegAccesos


def LeeCarpetaXML(full_folder):
    rescarp = []

    for filename in os.listdir(full_folder):

        if filename.endswith(".xml"):
            ffile = os.path.join(full_folder, filename)
            todo = LeeXML(ffile)

            for x in range(len(todo)):
                rescarp.append(todo[x])

    return rescarp


def ArchenCarp(carpeta):
    # return [os.path.abspath(arch.path) for arch in os.scandir(carpeta) if arch.is_file()]
    return [arch.name for arch in os.scandir(carpeta) if arch.is_file()]


def MatToExc(matriztodo):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directorio = os.path.join(BASE_DIR, "temp")

    ahora = datetime.datetime.now()
    # ya = str(ahora.year)+'{:02d}'.format(ahora.month)+'{:02d}'.format(ahora.day)+'{:02d}'.format(ahora.hour)
    ya = '{}{:02d}{:02d}{:02d}{:02d}'.format(ahora.year, ahora.month, ahora.day, ahora.hour, ahora.minute)

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    opath = os.path.join(directorio, 'resultados_' + ya + '.xlsx')
    # opath = os.link(directorio, 'resultados_' + ya + '.xlsx')

    workbook = xlsxwriter.Workbook(opath)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    money = workbook.add_format({'num_format': '$#,##0'})

    # Start from the first cell row 0 and column 0
    row = 1
    # col = 0
    worksheet.write(0, 0, "CUIT", bold)
    worksheet.write(0, 1, "Deducción", bold)
    worksheet.write(0, 2, "Tipo", bold)
    worksheet.write(0, 3, "Dato1", bold)
    worksheet.write(0, 4, "Dato2", bold)
    worksheet.write(0, 5, "Porc", bold)

    # Iterate through the array you have and unpack the tuple at each index
    for elm1, elm2, elm3, elm4, elm5, elm6 in matriztodo:
        worksheet.write(row, 0, elm1)
        worksheet.write(row, 1, elm2)
        worksheet.write(row, 2, elm3)
        worksheet.write(row, 3, elm4)
        worksheet.write(row, 4, elm5.replace(".", ","), money)
        worksheet.write(row, 5, elm6)
        row += 1

    workbook.close()

    opath2 = '/' + os.path.join("temp", 'resultados_' + ya + '.xlsx')

    return opath2


def MatToBD(matriztodo, id_regi):

    for elm1, elm2, elm3, elm4, elm5, elm6 in matriztodo:
        reg2 = Registros(
            id_reg=id_regi,
            cuil=elm1,
            tipo=elm2,
            tipo2=elm3,
            cantidad=elm4,
            importe=elm5,
            par2=elm6
        )

        reg2.save()


def AbrirExcel(archi):

    if sys.platform == "win32":
        os.startfile(archi)

    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, archi])


def get_ult_reg():
    # resp = RegAccesos.objects.latest('id')
    resp = RegAccesos.objects.last()

    return resp


def LeeXML(full_file):
    tree = ET.parse(full_file)
    root = tree.getroot()

    # shape = (0, 5)
    resultado = []

    dato1 = ""
    dato2 = ""
    dato3 = ""
    dato4 = ""
    dato5 = ""
    cuit = ""

    for child in root:

        for ch2 in child:
            if child.tag == "empleado" and ch2.tag == 'cuit':
                cuit = ch2.text

            else:
                tmp = False

                for ch3 in ch2:
                    if child.tag == "cargasFamilia":

                        if ch3.tag == 'mesDesde':
                            dato3 = ch3.text

                        elif ch3.tag == 'mesHasta':
                            dato4 = ch3.text

                        elif ch3.tag == 'porcentajeDeduccion':
                            dato5 = str(ch3.text)

                        elif ch3.tag == 'parentesco':
                            dato2 = ch3.text
                            dato1 = ch2.tag

                    if dato2 != "" and dato3 != "" and dato4 != "" and dato5 != "":
                        tmp = True

                    elif child.tag == "deducciones" and ch3.tag == "montoTotal":
                        tmp = True
                        dato1 = ch2.tag
                        dato2 = ch2.attrib['tipo']
                        dato4 = ch3.text

                        if ch2.attrib['tipo'] == '99':
                            tmp = False

                    elif child.tag == "deducciones" and ch2.attrib['tipo'] == '99':

                        for ch4 in ch3:
                            if ch4.attrib['nombre'] == 'motivo':
                                dato3 = ch4.attrib['valor']
                                tmp = True

                    elif child.tag == "retPerPagos" and ch3.tag == "montoTotal":
                        tmp = True
                        dato1 = str(ch2.tag)
                        dato2 = str(ch2.attrib['tipo'])
                        dato4 = str(ch3.text)

                    if (dato1 + str(dato2) + str(dato4) != "") and tmp:

                        resultado.append([cuit, dato1, dato2, dato3, dato4, dato5])

                        dato1 = ""
                        dato2 = ""
                        dato3 = ""
                        dato4 = ""
                        dato5 = ""

                    elif child.tag == "ganLiqOtrosEmpEnt":
                        for ch4 in ch3:
                            dato1 = ""

                            for ch5 in ch4:
                                if ch5.text != "0":

                                    resultado.append([cuit, child.tag.upper(), ch5.tag, "", ch5.text, ""])

    return resultado
