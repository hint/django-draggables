from django.conf import settings
from django.conf.urls.defaults import patterns
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest

from fields import DraggableAutoField


class DraggableAdmin(ModelAdmin):
    '''
    Add drag & drop functionality to your models.

    Usage:
        class MyAdmin(DraggableAdmin):
            model = MyDraggableModel # contains draggables.fields.DraggableAutoField
    '''

    def __init__(self, model, admin_site):
        super(DraggableAdmin, self).__init__(model, admin_site)
        if DraggableAdmin.get_draggable_auto_field(self):
            self.ordering = [DraggableAdmin.get_draggable_auto_field(self).name,]
        for inline in self.inline_instances:
            if DraggableAdmin.get_draggable_auto_field(inline):
                inline.opts.ordering = [DraggableAdmin.get_draggable_auto_field(inline).name]
                DraggableAdmin.get_draggable_auto_field(inline).editable = True

    @staticmethod
    def get_draggable_auto_field(klass):
        '''
        Return instance of draggables.fields.DraggableAutoField
        '''
        draggable_auto_field = None
        for field in klass.model._meta.fields:
            if isinstance(field, DraggableAutoField):
                if draggable_auto_field:
                    raise ImproperlyConfigured('Two instances of draggables.fields.DraggableAutoField on the %s model' % klass.model)
                else:
                    draggable_auto_field = field
        return draggable_auto_field

    def _media(self):
        '''
        Add jquery.draggables.js to any admin view
        '''
        media = super(DraggableAdmin, self)._media()
        i18n_javascript = reverse('admin:%s_%s_changelist' % (
            self.opts.app_label, self.opts.module_name,
        ))
        if DraggableAdmin.get_draggable_auto_field(self):
            media.add_js(('admin_jqueryui/js/admin_jqueryui.min.js',
                          '%sjsi18n/' % i18n_javascript,
                          'draggables/jquery.draggables.js',))
        return media
    media = property(_media)

    def i18n_javascript(self, request):
        '''
        Displays the i18n JavaScript that the Django admin requires.

        This takes into account the USE_I18N setting. If it's set to False, the
        generated JavaScript will be leaner and faster.
        '''
        if settings.USE_I18N:
            from django.views.i18n import javascript_catalog
        else:
            from django.views.i18n import null_javascript_catalog as javascript_catalog
        return javascript_catalog(request, packages='draggables')

    def save_positions(self, request):
        '''
        Execute UPDATE ... WHERE id = ... SET position = ... queries
        These should be fast enough
        '''
        if not request.POST.get('order[]'):
            return HttpResponseBadRequest()
        for position, pk in enumerate(request.POST.getlist('order[]')):
            self.model.objects.filter(pk=pk).\
                update(**{DraggableAdmin.get_draggable_auto_field(self).name: position + 1})
        return HttpResponse()

    def get_urls(self):
        '''
        Add save_positions to admin urls
        '''
        urls = super(DraggableAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^save_positions/$', self.admin_site.admin_view(self.save_positions)),
            (r'^jsi18n/$', self.admin_site.admin_view(self.i18n_javascript)),
        )
        return my_urls + urls
