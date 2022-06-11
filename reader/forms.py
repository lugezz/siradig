from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Seleccione archivo resultadosXML.zip',
        help_text='Máximo 42 Mb'
    )
