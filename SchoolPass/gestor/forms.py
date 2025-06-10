from django import forms

class UploadPlanilhaForm(forms.Form):
    arquivo = forms.FileField(label="Importar Grade (Excel)")