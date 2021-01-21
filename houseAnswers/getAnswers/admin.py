from django.contrib import admin
from .models import Provider,Fields 

admin.site.site_header = "Anwers Provider Admin"
admin.site.site_tittle = "Anwers Provider Admin"
class FieldsInline(admin.TabularInline):
    model = Fields
    extra = 3

class ProviderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["name"],
        }),
        ("URL", {
            "fields": ["url"],
        }),
        ("Priority", {
            "fields": ["priority"],
        }),
        ("Authentication", {
            "fields": ["auth_key"],
        })
    )
    
    inlines = [FieldsInline]

admin.site.register(Provider,ProviderAdmin)    
    

