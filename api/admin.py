from django.contrib import admin
from api.models import Password


# Register your models here.
@admin.register(Password)
class PassWordADMin(admin.ModelAdmin):
    list_display = ["id", "user", "user_id"]
