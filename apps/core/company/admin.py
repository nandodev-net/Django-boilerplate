from django.contrib import admin
from .models import (
    Company
)

class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'doctype', 'tax_document')
    list_display = ('store_code', 'name', 'doctype', 'tax_document', 'created')

admin.site.register(Company, CompanyAdmin)
