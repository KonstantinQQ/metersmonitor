from django import forms
from django.contrib import admin, messages
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import QuerySet, Query


class QuerySetAdmin(admin.ModelAdmin):

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Набор), т.к. есть дочерние объекты, " \
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
            msg = "Невозможно удалить родительский объект (Набор), т.к. есть дочерние объекты, " \
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


class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute', 'qset', 'funcbyte', 'reqbyte', 'factor', 'unit', 'handler')
    list_filter = ['qset']

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            msg = "Невозможно удалить родительский объект (Запрос), т.к. есть дочерние объекты, " \
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
            msg = "Невозможно удалить родительский объект (Запрос), т.к. есть дочерние объекты, " \
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
            formfield.widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        return formfield

    def reqbyte(self, obj):
        return ' '.join(obj.req[i:i+2] for i in range(0, len(obj.req), 2))

    def funcbyte(self, obj):
        return ' '.join(obj.func[i:i + 2] for i in range(0, len(obj.func), 2))

    reqbyte.short_description = 'Данные'
    funcbyte.short_description = 'Команда'


admin.site.register(QuerySet, QuerySetAdmin)
admin.site.register(Query, QueryAdmin)
