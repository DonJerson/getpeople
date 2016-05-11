from django.contrib import admin

# Register your models here.
from .models import Candidate, Position

admin.site.register(Candidate)
admin.site.register(Position)
