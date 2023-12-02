from django.contrib import admin
from theater.models import Theater

# Register your models here.
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    # Add any specific configurations or customizations for the admin interface here
    pass

