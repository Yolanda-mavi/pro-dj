
from django.forms import ModelForm

from django.forms.widgets import  TextInput
from appscore.mrp.models import Bom

#cambio pruebas11
#tambien existe un video 27 donde agrega propiedades por medio de una libreria tipo wigget que se instala (tweaks)

def comun_layout(form,layout):
    result = []
    for row in layout:
        cols=12 //len(row)
        result.append([
            {
                'field':form[field],
                'col':cols
            }
            for field in row
        ])
    return result

def customfield2_layout(form,layout):
    ##only cols pair
    result = []
    for row in layout:
        cols = int( len(row)/2)
        numero = 0
        cols_list = []
        for l in range( cols):
            cols_list.append(  {'field1': form[row[numero]], 'field2': form[row[numero+1]]}  )
            numero = numero + 2
        result.append( cols_list )
    return result

class BomForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(BomForm, self).__init__(*args, **kwargs)
        #para porpiedades en comun
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Bom
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
                'placeholder':"ingresar nombre",
            })
        }

    #se me paso agregar el save

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            self.add_error('name',"no es muy long")
        return cleaned