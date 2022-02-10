from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register((Subject, Status, Contact))

admin.site.register((Booking, BookUpdate))

@admin.register(Customer, Tutor)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
