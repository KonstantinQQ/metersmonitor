from django.contrib import admin
from .models import Quality


class QualityAdmin(admin.ModelAdmin):
    list_display = ('dev', 'attr', 'value', 'unit', 'tmstamp')
    list_filter = ['dev']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        # extra_context['show_delete'] = False
        # extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def unit(self, obj):
        return obj.qry.unit

    def attr(self, obj):
        return obj.qry.attribute

    def tmstamp(self, obj):
        return f'{obj.timestamp:%d.%m.%Y %H:%M:%S}'

    unit.short_description = 'Ед. изм.'
    tmstamp.short_description = 'Метка'
    attr.short_description = 'Атрибут'


admin.site.register(Quality, QualityAdmin)
