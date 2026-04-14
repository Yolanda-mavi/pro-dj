from django.db.models.fields import DecimalField
from django.forms import ModelForm
from django import forms
from django.forms.widgets import  TextInput
from appscore.rdata.models import Partner

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


class PartnerForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        #para porpiedades en comun
        for form in self.visible_fields():

            if form.name in ['birthdate','registration_dt','off_dt','license_exp_dt','card_exp_dt','card_fast_exp_dt']:
                form.field.widget.attrs['class'] = 'form-control datepicker'
                form.field.widget.attrs['placeholder'] = 'yyyy-mm-dd'
                form.field.widget.attrs['type'] = 'text'
            elif form.name not in ['legal_rep','country','state','partner'] :
                form.field.widget.attrs['class'] = 'form-control'
            else:
                form.field.widget.attrs['class'] = 'tomselect'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Partner
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
                'placeholder':"ingresar nombre",
            }),
        }
    #se me paso agregar el save

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            self.add_error('name',"no es muy long")
        return cleaned
