from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from NamesDatabase.models import Name

admin.site.unregister(Group)
admin.site.register(Name)