from django.contrib import admin
from app_projeto_final.models import Professor, Curso, Aluno, NotaCurso

# Register your models here.
admin.site.register(Professor)
admin.site.register(Curso)
admin.site.register(Aluno)
admin.site.register(NotaCurso)