from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Email)
admin.site.register(Email_File)
admin.site.register(Drive_File)
