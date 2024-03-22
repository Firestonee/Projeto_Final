from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from app_projeto_final.models import Aluno, Professor, Curso, NotaCurso
from django.contrib.auth import authenticate, login, logout 
from app_projeto_final.forms import UserCreationForm, LoginForm

# Create your views here.

def home(request):
  return render(request, 'home.html')

def aluno(request):
  alunos = Aluno.objects.all()
  cursos = Curso.objects.all()
  notas = NotaCurso.objects.select_related('aluno', 'curso').all()
  return render(request, 'alunos.html', {'alunos':alunos, 'cursos':cursos, 'notas': notas})

def professores(request):
  professores = Professor.objects.all()
  return render(request, 'professores.html', {'professores':professores})

def adicionar_nota(request, aluno_id, curso_id):
  aluno = Aluno.objects.get(pk=aluno_id)
  curso = Curso.objects.get(pk=curso_id)
  notas = NotaCurso.objects.all()

  if NotaCurso.objects.filter(aluno=aluno, curso=curso).exists():
    return HttpResponse('Nota para esse curso já exite!')
  
  if request.method == 'POST':
    nova_nota_curso = request.POST.get('adicionar_nota')
    aluno = Aluno.objects.get(pk=aluno_id)
    curso = Curso.objects.get(pk=curso_id)
    NotaCurso.objects.create(aluno=aluno, curso=curso, nota=nova_nota_curso)
    return redirect('aluno')

  return render(request, 'adicionar_nota.html', {'aluno': aluno,'curso': curso, 'notas':notas})

def editar_nota(request, aluno_id, curso_id):
  aluno = Aluno.objects.get(pk=aluno_id)
  curso = Curso.objects.get(pk=curso_id)
  notas = NotaCurso.objects.all()

  if request.method == 'POST':
      nota_editada_value = request.POST.get('nota_editada')
      nota_editada = get_object_or_404(NotaCurso, aluno=aluno, curso=curso)  # Obtém a instância correta de NotaCurso
      nota_editada.nota = nota_editada_value  # Atualiza o valor da nota
      nota_editada.save()

      return redirect('aluno')

  return render(request, 'editar_nota.html', {'aluno':aluno, 'curso':curso, 'notas':notas})

def excluir_nota(request, aluno_id, curso_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    curso = get_object_or_404(Curso, pk=curso_id)

    nota = get_object_or_404(NotaCurso, aluno=aluno, curso=curso)


    if request.method == 'POST':
       
        nota.delete()
        
        return redirect('aluno')

    return render(request, 'excluir_nota.html', {'aluno': aluno, 'curso': curso, 'nota': nota})

def administrador(request):
  cursos = Curso.objects.all()
  professores = Professor.objects.all()
  return render(request, 'administrador.html', {'cursos': cursos, 'professores': professores})

def editar_professor_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if request.method == 'POST':
        professores_selecionados = request.POST.getlist('professores')

        curso.professor.set(professores_selecionados)

        return redirect('administrador')

    professores = Professor.objects.all()
    return render(request, 'editar_professor_curso.html', {'curso': curso, 'professores': professores})

def excluir_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    
    if request.method == 'POST':
        curso.delete()
        return redirect('administrador')

    return render(request, 'excluir_curso.html', {'curso': curso})

def adicionar_professor(request):
   if request.method == 'POST':
      novo_professor_nome = request.POST.get('novo_professor')  
      novo_professor = Professor(nome=novo_professor_nome)
      novo_professor.save()

      return redirect('administrador')

   return render(request, 'adicionar_professor.html')

def adicionar_curso(request):
    if request.method == 'POST':
        novo_curso_nome = request.POST.get('novo_curso')  # Obtém o nome do novo curso do formulário
        professor_id = request.POST.get('curso')  # Obtém o ID do professor selecionado no formulário

        # Verifica se o professor selecionado existe
        try:
            professor = Professor.objects.get(id=professor_id)
        except Professor.DoesNotExist:
            return render(request, 'adicionar_curso.html', {'error_message': 'Professor selecionado não encontrado.'})

        # Cria um novo objeto Curso com o nome e professor fornecidos
        novo_curso = Curso(nome=novo_curso_nome)
        novo_curso.save()  # Salva o novo curso no banco de dados

        novo_curso.professor.set([professor])

        return redirect('administrador')  # Redireciona para a página desejada após adicionar o curso

    # Obtém todos os professores para preencher o menu suspenso
    professores = Professor.objects.all()
    return render(request, 'adicionar_curso.html', {'professores': professores})

def excluir_professor(request, professor_id):
    # Obtém o objeto do professor ou retorna um erro 404 se não for encontrado
    professor = get_object_or_404(Professor, pk=professor_id)
    
    if request.method == 'POST':
        # Exclui o professor do banco de dados
        professor.delete()
        return redirect('administrador')  # Redireciona para a página desejada após excluir o professor
    
    return render(request, 'excluir_professor.html', {'professor': professor})

def user_signup(request):
  form = UserCreationForm(request.POST)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('login')
    else:
      form = UserCreationForm()
  return render(request, 'signup.html', {'form': form})
  
def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
    if user:
      login(request, user)
      return redirect('home')
  else:
    form = LoginForm()

  return render(request, 'login.html', {'form': form})

def user_logout(request):
  logout(request)
  return redirect('home')

def adicionar_aluno(request):
    cursos = Curso.objects.all()

    if request.method == 'POST':
        nome_aluno = request.POST.get('nome_aluno')
        curso_id = request.POST.get('curso')  # Pegar o ID do curso selecionado

        if nome_aluno and curso_id:
           curso = Curso.objects.get(id=curso_id)
           novo_aluno = Aluno(nome=nome_aluno)
           novo_aluno.save()
           novo_aluno.cursos.add(curso)
          
        return redirect('aluno')
          
    cursos = Curso.objects.all()
    return render(request, 'adicionar_aluno.html', {'cursos': cursos})