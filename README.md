# Siradig Reader

Siradig Reader fue desarrollado con la finalidad de simplificar
el proceso de lectura masiva de formularios Siradig de AFIP de los empleados.

## Uso

Para detalles de como iniciar tu entorno lcoal de desarrollo, ingresa [aqui](docs/entorno-local.md)

## SMTP Config
Para que esta aplicacion sea capaz de enviar emails debes actualizar el archivo `local_settings.py`
con las referencias a tu servidor SMTP.

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tu usuaurio'
EMAIL_HOST_PASSWORD = 'tu clave'
```

## Contribuciones
Son siempre bienvenidas las Pull Requests, para cambios mayores por favor abra un Issue primero para discutir la propuesta del cambio

Por favor asegurese de actualizar los tests apropiadamente

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)