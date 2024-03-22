from django.urls import path
from app_projeto_final import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('aluno/', views.aluno, name='aluno'),
  path('professores/', views.professores, name='professores'),
  path('adicionar_nota/<int:aluno_id>/<int:curso_id>/', views.adicionar_nota, name='adicionar_nota'),
  path('editar_nota/<int:aluno_id>/<int:curso_id>/', views.editar_nota, name='editar_nota'),
  path('excluir_nota/<int:aluno_id>/<int:curso_id>/', views.excluir_nota, name='excluir_nota'),
  path('administrador/', views.administrador, name='administrador'),
  path('editar_professor_curso/<int:curso_id>/', views.editar_professor_curso, name='editar_professor_curso'),
  path('excluir_curso/<int:curso_id>/', views.excluir_curso, name='excluir_curso'),
  path('adicionar_professor/', views.adicionar_professor, name='adicionar_professor'),
  path('adicionar_curso/', views.adicionar_curso, name='adicionar_curso'),
  path('excluir_professor/<int:professor_id>/', views.excluir_professor, name='excluir_professor'),
  path('login/', views.user_login, name='login'),
  path('signup/', views.user_signup, name='signup'),
  path('logout/', views.user_logout, name='logout'),
  path('adicionar_aluno', views.adicionar_aluno, name='adicionar_aluno'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)