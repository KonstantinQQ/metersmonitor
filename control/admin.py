from django import forms
from django.contrib import admin, messages
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DeviceType, Hub, Protocol, Device


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'typename')

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Тип устройства), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(object_id,),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Тип устройства), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'typename':
            formfield.strip = False
            formfield.widget = forms.Textarea(attrs={'cols': 80, 'rows': 5})
        return formfield


class HubAdmin(admin.ModelAdmin):

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Концентратор), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(object_id,),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Концентратор), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)


class ProtocolAdmin(admin.ModelAdmin):

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Протокол), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(object_id,),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Протокол), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'model', 'mk', 'protocol', 'hub', 'addr', 'qset', 'is_active', 'is_portforwarding')
    list_filter = ('type', 'protocol', 'qset', 'is_active')
    fieldsets = [
        ('Характеристики устройства', {'fields': ['type', 'model', 'mk', 'protocol', 'hub', 'addr', 'qset',
                                                  'is_active', 'is_portforwarding']}),
        ('Параметры порта', {'fields': ['baudrate', 'parity', 'bytesize', 'stopbits']}),
        ('Примечание', {'fields': ['fn']})
    ]

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Устройство), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(object_id,),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Устройство), т.к. есть дочерние объекты, " \
                  "ссылающиеся на него"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                                 current_app=self.admin_site.name, )
            return HttpResponseRedirect(return_url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'fn':
            formfield.strip = False
            formfield.widget = forms.Textarea(attrs={'cols': 80, 'rows': 5})
        return formfield


admin.site.site_header = 'Управление системой наблюдения за устройствами'
admin.site.site_title = "Система мониторинга"
admin.site.index_title = 'Настройка мониторинга'

admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Hub, HubAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Device, DeviceAdmin)
