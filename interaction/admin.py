from django.contrib import admin
from django_db_logger.models import StatusLog
from django_db_logger.admin import StatusLogAdmin


class UserStatusLogAdmin(StatusLogAdmin):
    list_per_page = 15
    StatusLogAdmin.colored_msg.short_description = 'Сообщение'
    StatusLogAdmin.traceback.short_description = 'Трассировка'
    StatusLogAdmin.create_datetime_format.short_description = 'Метка'

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


admin.site.unregister(StatusLog)
admin.site.register(StatusLog, UserStatusLogAdmin)
