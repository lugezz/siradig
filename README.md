# Siradig Reader

Siradig Reader fue desarrollado con la finalidad de simplificar
el proceso de lectura masiva de formularios Siradig de AFIP de los empleados.

## Procedimiento de instalación

```bash
# Descargar repositorio
git clone git@github.com:lugezz/siradig.git

# Crear entorno virtual
python3 -m venv env

# Activamos el entorno virtual
source env/bin/activate

# Instalar requerimientos
pip install -r requirements.txt

# Creación Base de Datos MySQL
mysql -u root -p
CREATE DATABASE siradig CHARACTER SET utf8;

En archivo my_db.cnf cambiar usuario y contraseña del usuario de MySQL con privilegios

# SMTP Config
En archivo .env en el directorio raiz deben configurarse las siguientes variables de entorno:
- EMAIL_USER=mi_smtp@email.com
- EMAIL_PASSWORD=contreseña

```

## Uso

```

```

## Contribuciones
Son siempre bienvenidas las Pull Requests, para cambios mayores por favor abra un Issue primero para discutir la propuesta del cambio

Por favor asegurese de actualizar los tests apropiadamente

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)