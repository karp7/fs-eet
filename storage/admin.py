from django.contrib import admin


# Register your models here.

from .models import Project, Document

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')



@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('document', 'description')
	# raw_id_fields = ('document',)
	# raw_id_fields = ('prjog',)