from django.contrib import admin
from .forms import PositionModelAdminForm
# Register your models here.
from .models import *

class PositionAdmin(admin.ModelAdmin):

	#date_hierarchy = 'date'
	form = PositionModelAdminForm

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(LogTemplate)
admin.site.register(Log)
admin.site.register(Recruiter)

