from datetime import datetime
import os
import subprocess
import sys
import xmltodict

from django.conf import settings
import xlsxwriter
import xml.etree.ElementTree as ET

from .models import Registro
from .deducciones import get_deduccion


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
    ahora = datetime.now()
    ya = '{}{:02d}{:02d}{:02d}{:02d}'.format(ahora.year, ahora.month, ahora.day, ahora.hour, ahora.minute)

    directorio = settings.TEMP_ROOT
    file_name = f'resultados_{ya}.xlsx'
    opath = os.path.join(directorio, file_name)

    workbook = xlsxwriter.Workbook(opath)
    worksheet = workbook.add_worksheet()

    money = workbook.add_format({'num_format': '$#,##0.00'})
    header_format = workbook.add_format({'bold': True,
                                         'align': 'center',
                                         'valign': 'vcenter',
                                         'fg_color': '#D7E4BC',
                                         'border': 1})
    center_format = workbook.add_format({'align': 'center'})
    no_format = workbook.add_format()

    center_format.set_font_name('Arial')
    center_format.set_font_size(8)
    header_format.set_font_name('Arial')
    header_format.set_font_size(8)
    money.set_font_name('Arial')
    money.set_font_size(8)
    no_format.set_font_name('Arial')
    no_format.set_font_size(8)

    # Empiezo por el encabezado
    row = 1
    # col = 0
    worksheet.write(0, 0, "CUIL", header_format)
    worksheet.write(0, 1, "Deducción", header_format)
    worksheet.write(0, 2, "Tipo", header_format)
    worksheet.write(0, 3, "Dato1", header_format)
    worksheet.write(0, 4, "Dato2", header_format)
    worksheet.write(0, 5, "Porc", header_format)
    worksheet.write(0, 6, "Descripción", header_format)

    # Algo de formato
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('G:G', 60)
    worksheet.freeze_panes(1, 1)

    # Itero por cada item de MatrizTodo
    for elements in matriztodo:
        for idx, item in enumerate(elements):
            # Proceso los 6 items en cada fila de MatrizTodo
            item_format = money if (idx == 4 and elements[1] != 'cargaFamilia') else center_format

            if idx == 1 or idx == 6:
                worksheet.write(row, idx, item, no_format)
            else:
                if elements[1] == 'GANLIQOTROSEMPENT' and idx == 2:
                    worksheet.write(row, idx, item, no_format)
                else:
                    val_item = 0 if not item else float(item)
                    worksheet.write_number(row, idx, val_item, item_format)
        row += 1

    workbook.close()

    return file_name


def QueryToExc(id, query):
    opath = os.path.join(settings.TEMP_ROOT, f"Presentacion_{id}.xlsx")

    workbook = xlsxwriter.Workbook(opath)
    worksheet = workbook.add_worksheet()

    money = workbook.add_format({'num_format': '$#,##0.00'})
    header_format = workbook.add_format({'bold': True,
                                         'align': 'center',
                                         'valign': 'vcenter',
                                         'fg_color': '#D7E4BC',
                                         'border': 1})
    center_format = workbook.add_format({'align': 'center'})
    no_format = workbook.add_format()

    center_format.set_font_name('Arial')
    center_format.set_font_size(8)
    header_format.set_font_name('Arial')
    header_format.set_font_size(8)
    money.set_font_name('Arial')
    money.set_font_size(8)
    no_format.set_font_name('Arial')
    no_format.set_font_size(8)

    # Empiezo por el encabezado
    row = 1
    worksheet.write(0, 0, "CUIL", header_format)
    worksheet.write(0, 1, "Deducción", header_format)
    worksheet.write(0, 2, "Tipo", header_format)
    worksheet.write(0, 3, "Dato1", header_format)
    worksheet.write(0, 4, "Dato2", header_format)
    worksheet.write(0, 5, "Porc", header_format)
    worksheet.write(0, 6, "Descripción", header_format)

    # Algo de formato
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('G:G', 60)
    worksheet.freeze_panes(1, 1)

    # Itero por cada item de MatrizTodo
    for item in query:
        worksheet.write_number(row, 0, item.cuil, center_format)
        worksheet.write(row, 1, item.deduccion, no_format)

        if item.deduccion == 'GANLIQOTROSEMPENT':
            worksheet.write(row, 2, item.tipo, no_format)
        else:
            val_item = 0 if not item.tipo else float(item.tipo)
            worksheet.write_number(row, 2, val_item, center_format)

        val_item = 0 if not item.dato1 else int(item.dato1)
        worksheet.write_number(row, 3, int(val_item), center_format)

        if item.deduccion == 'cargaFamilia':
            worksheet.write_number(row, 4, int(item.dato2), center_format)
        else:
            worksheet.write_number(row, 4, float(item.dato2), money)

        val_item = 0 if not item.porc else float(item.porc)
        worksheet.write_number(row, 5, val_item, center_format)

        worksheet.write(row, 6, get_deduccion(item.deduccion, item.tipo), no_format)
        row += 1
    workbook.close()


def MatToBD(matriztodo, id_regi):

    for elm1, elm2, elm3, elm4, elm5, elm6 in matriztodo:
        reg2 = Registro(
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
    descripcion = ""
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
                            descripcion = get_deduccion(dato1, dato2)

                    if dato2 != "" and dato3 != "" and dato4 != "" and dato5 != "":
                        tmp = True

                    elif child.tag == "deducciones" and ch3.tag == "montoTotal":
                        tmp = True
                        dato1 = ch2.tag
                        dato2 = ch2.attrib['tipo']
                        dato4 = ch3.text
                        descripcion = get_deduccion(dato1, dato2)

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
                        descripcion = get_deduccion(dato1, dato2)

                    if (dato1 + str(dato2) + str(dato4) != "") and tmp:

                        resultado.append([cuit, dato1, dato2, dato3, dato4, dato5, descripcion])

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


# -----------------------------------------------------------------------
class EmpleadoSiradig:
    def __init__(self, cuit, nro_presentacion, fecha, deducciones=[],
                 cargasFamilia=[], ganLiqOtrosEmpEnt=[], retPerPagos=[]):
        self.cuit = cuit
        self.nro_presentacion = nro_presentacion
        self.fecha = fecha
        self.deducciones = deducciones
        self.cargasFamilia = cargasFamilia
        self.ganLiqOtrosEmpEnt = ganLiqOtrosEmpEnt
        self.retPerPagos = retPerPagos

    def get_cuit(self):
        return self.cuit

    def get_dict_all(self):
        diccionario = {
            'cuit': self.cuit,
            'deducciones': self.deducciones,
            'cargasFamilia': self.cargasFamilia,
            'ganLiqOtrosEmpEnt': self.ganLiqOtrosEmpEnt,
            'retPerPagos': self.retPerPagos,
        }

        return diccionario

    def get_total_deducciones(self):
        resp = 0
        for deduccion in self.deducciones:
            resp += deduccion['importe']


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def leeXML3(xml_file):
    """
    Lee XML
    ------
    Devuelve un objeto Empleado con la información
    de la presentación y todo lo declarado
    """

    tree = ET.parse(xml_file)
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

    diccionario_base = xmltodict.parse(xmlstr)
    cuit = diccionario_base['presentacion']['empleado']['cuit']
    nro_presentacion = diccionario_base['presentacion']['nroPresentacion']
    fecha = diccionario_base['presentacion']['fechaPresentacion']
    fecha = datetime.strptime(fecha, '%Y-%m-%d')
    deducciones = []
    cargasFamilia = []
    ganLiqOtrosEmpEnt = []
    retPerPagos = []

    # Tomo Deducciones -----------------------------------
    if diccionario_base['presentacion'].get('deducciones'):
        lista_deducciones = diccionario_base['presentacion']['deducciones']['deduccion']
        if type(lista_deducciones) != list:
            # Para que el bucle no tome los campos
            lista_deducciones = [lista_deducciones]

        for deduccion in lista_deducciones:
            subtipo = 0
            if 'detalles' in deduccion:
                subtipo = deduccion['detalles']['detalle']['@motivo']

            deducciones.append(
                {'nombre': 'deduccion',
                 'tipo': deduccion['@tipo'],
                 'subtipo': subtipo,
                 'importe': deduccion['montoTotal'],
                 'descripcion': get_deduccion('deduccion', deduccion['@tipo'])
                 }
            )

    # Tomo Cargas de Familia -----------------------------------
    if diccionario_base['presentacion'].get('cargasFamilia'):
        lista_familiares = diccionario_base['presentacion']['cargasFamilia']['cargaFamilia']

        if type(lista_familiares) != list:
            # Para que el bucle no tome los campos
            lista_familiares = [lista_familiares]

        for carga_flia in lista_familiares:
            cargasFamilia.append(
                {'nombre': 'cargaFamilia',
                 'tipo': carga_flia['parentesco'],
                 'desde': carga_flia['mesDesde'],
                 'hasta': carga_flia['mesHasta'],
                 'porc': carga_flia['porcentajeDeduccion'],
                 'descripcion': get_deduccion('cargaFamilia', carga_flia['parentesco'])
                 }
            )

    # Tomo Ganancias otros empleadores -----------------------------------
    if diccionario_base['presentacion'].get('ganLiqOtrosEmpEnt'):
        lista_gan_otro_emp = diccionario_base['presentacion']['ganLiqOtrosEmpEnt']['empEnt']

        if type(lista_gan_otro_emp) != list:
            # Para que el bucle no tome los campos
            lista_gan_otro_emp = [lista_gan_otro_emp]

        for ganancia_OE in lista_gan_otro_emp:
            for ganancia_mes_OE in ganancia_OE['ingresosAportes']['ingAp']:
                for item in ganancia_mes_OE:
                    if ganancia_mes_OE[item] != '0' and item != '@mes':
                        ganLiqOtrosEmpEnt.append(
                            {'nombre': 'GanOtroEmpleadores',
                             'tipo': item,
                             'importe': ganancia_mes_OE[item],
                             }
                        )

    # Tomo Percepciones -----------------------------------
    if diccionario_base['presentacion'].get('retPerPagos'):
        lista_percepciones = diccionario_base['presentacion']['retPerPagos']['retPerPago']

        if type(lista_percepciones) != list:
            # Para que el bucle no tome los campos
            lista_percepciones = [lista_percepciones]

        for percepcion in lista_percepciones:
            retPerPagos.append(
                {'nombre': 'retPerPago',
                 'tipo': percepcion['@tipo'],
                 'importe': percepcion['montoTotal'],
                 'descripcion': get_deduccion('retPerPago', percepcion['@tipo'])
                 }
            )

    empleado = EmpleadoSiradig(cuit=cuit,
                               nro_presentacion=nro_presentacion,
                               fecha=fecha,
                               deducciones=deducciones,
                               cargasFamilia=cargasFamilia,
                               ganLiqOtrosEmpEnt=ganLiqOtrosEmpEnt,
                               retPerPagos=retPerPagos)

    return empleado
