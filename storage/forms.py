from django.forms import  ModelForm, CharField
from .models import Project, Document



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description',)
        labels = {
                'name': 'Назва проекту',
                'description': 'Стислий опис',
            }



class DocumentForm(ModelForm):
    # subject = CharField(label='Опис файлу',max_length=100)

    class Meta:
        model = Document
        fields = ('description', 'document', )

        labels = {
            'description': 'Назва',
            'document': 'Файл',
        }

        # help_texts = {
        #     'description': ('Назва документу'),
        #     'document': ('Прикріплення файлу'),
        # }
        # descr_doc = forms.CharField(label='Опис файлу', max_length=100)

