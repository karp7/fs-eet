from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse 
from django.views import generic

from django.template import loader
import datetime
from django.utils import timezone

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Document, Project

from .forms import ProjectForm, DocumentForm


from django.conf import settings
import os


def index(request):

    prj_list = Project.objects.all()
    doc_list = Document.objects.all()

    return render(request, 'index.html', {
        'prj_list':prj_list,
        'doc_list':doc_list,
    })




def lsProject(request):
    prj_list = Project.objects.all()
    doc_list = Document.objects.all()

    return render(request, 'list_prj.html', {
        'prj_list':prj_list,
        'doc_list':doc_list,
    })



# Перегляд даних
def pView(request, id):

        prj = get_object_or_404(Project, id=id)
        doc_ls = Document.objects.filter(prjog = prj)
 

        return render(request, "detail_prj.html", {
                "prj":prj,
                "doc_ls":doc_ls,
        })

    # додавання данных до бд
def pAdd(request):
    mode_prj="Створення нового проекту"
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lsprj/')
            
    else:
        form = ProjectForm()
    return render(request, 'edit_prj.html', {
        'form': form,
        "mode_prj":mode_prj,        
    })


# Редагування даних
def pEdit(request, id):

    mode_prj="Редагування проекту"

    try:
        prj = get_object_or_404(Project, pk=id)
 
        if request.method == "POST":
            form = ProjectForm(request.POST, instance = prj)
            if form.is_valid():
                prj_fm = form.save(commit=False)
                prj_fm.save()

                return HttpResponseRedirect('/lsprj/')
        else:
            form = ProjectForm(instance = prj)
        return render(request, "edit_prj.html", {
                "form": form,
                "prj":prj,
                "mode_prj":mode_prj,
        })
    except ProjectForm.DoesNotExist:
        return HttpResponseNotFound("<h2>Проект не існує</h2>")

    # видалення проекту з бази даних
def pDelete(request, id):

    mode_prj="Видалення проекту"    
    try:
        prj = get_object_or_404(Project, pk=id)
        file_list = Document.objects.filter(prjog = prj)
 
        if request.method == "POST":
            form = ProjectForm(request.POST, instance = prj)
            if form.is_valid():
                prj_fm = form.save(commit=False)
                prj_fm.delete()

                return HttpResponseRedirect('/lsprj/')
        else:
            form = ProjectForm(instance = prj)
        return render(request, "delete_prj.html", {
                "form": form,
                "prj":prj,
                "file_list": file_list,
                "mode_prj":mode_prj,
        })
    except ProjectForm.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


    # додавання документів до бд
def fAdd(request, pg_id):
    
    mode_prj="Додати документ"    
    prj =  Project.objects.get(id = pg_id)
    file_list = Document.objects.filter(prjog = prj)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.prjog = prj
            doc.save()
            return HttpResponseRedirect('/pview/' + pg_id)
            
    else:
        form = DocumentForm()
    return render(request, 'add_doc.html', {
        'form': form,
        'file_list': file_list,
        'mode_prj':mode_prj,
    })


def del_load_Doc(request, id):
    # print('**************')
    response = HttpResponseRedirect("<h2>Помилка вивантаження</h2>") 
    if request.method == 'POST':
        list_id_doc = request.POST.getlist('select_file')
        delOrload = request.POST['delOrload']


        doc_list=[Document.objects.get(id=f_id) for f_id in list_id_doc]


        if delOrload == "Load":
            print("delOrload="+delOrload)
            response = loadFiles(doc_list)

        if delOrload == "Del":
            print("delOrload="+delOrload)
            response = fDelete(doc_list, id)            

    return response



def loadFiles(doc_list):


    zfpath=toZipp(doc_list)
    file_path = os.path.join(settings.MEDIA_ROOT, zfpath)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="multipart/form-data")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
            fh.close()
    return HttpResponseNotFound("<h2>Архів не створено</h2>")   


import zipfile #подключаем модуль



def toZipp(doc_list):

    os.chdir(settings.MEDIA_ROOT)
    arhiv_name='arhiv.zip' #создаем переменную - название и местоположение файла
    
    newzip=zipfile.ZipFile(arhiv_name,'w',zipfile.ZIP_DEFLATED) #создаем архив
    
    for doc in doc_list:
        fpath=doc.document.path 

        f_name_ls=fpath.split('\\')
        f_name = f_name_ls[len(f_name_ls) - 1] # ім'я файлу без розташування

        newzip.write(f_name) #добавляем файл в архив

    newzip.close() #закрываем архив
    return arhiv_name

    # удаление данных из бд
def fDelete(doc_list, pg_id):
    try:
        # doc = Document.objects.get(id = id)
        
        for doc in doc_list:
            doc.delete()

        return HttpResponseRedirect("/pview/" + pg_id)
    except Document.DoesNotExist:
        return HttpResponseNotFound("<h2>Документ не знайдено</h2>")