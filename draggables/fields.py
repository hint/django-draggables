from django.db.models import PositiveSmallIntegerField
#from django.forms.widgets import HiddenInput


class DraggableAutoField(PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['null'] = True
        kwargs['blank'] = True
        super(DraggableAutoField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        if model_instance.pk:
            return super(DraggableAutoField, self).clean(value, model_instance)
        else:
            return None

    def formfield(self, **kwargs):
        formfield = super(DraggableAutoField, self).formfield(**kwargs)
        #formfield.widget = HiddenInput(attrs={'class': 'draggableAutoField'})
        formfield.widget.attrs['class'] += ' draggableAutoField'
        formfield.widget.attrs['readonly'] = 'readonly'
        return formfield



try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^draggables\.fields\.DraggableAutoField"])
except ImportError:
    pass