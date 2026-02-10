from django.forms import ModelForm
from django.forms.widgets import Textarea,TextInput
from django.views.generic import CreateView
from appscore.base.models import Product

#tambien existe un video 27 donde agrega propiedades por medio de una libreria tipo wigget que se instala (tweaks)
class ProductForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        #para porpiedades en comun
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True



    class Meta:
        model = Product
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            #para pocos capos se puede perzonalizar asi los campos
            'name': TextInput(attrs={
                # 'class':"form-control",
                'placeholder':"ingresar nombre",
                # 'autocomplete': 'off'


            }),
            'description': Textarea(attrs={
            # 'class': "form-control",
            'placeholder': "ingresar nombre",
            # 'autocomplete': 'off',
            'rows': 3,
            'cols': 100

        }
        )
        }