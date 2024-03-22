from django.db import models

# Create your models here.
class Professor(models.Model):
  nome = models.CharField(max_length=200)

  def __str__(self):
    return self.nome

class Curso(models.Model):
  nome = models.CharField(max_length=100)
  professor = models.ManyToManyField(Professor)

  def __str__(self):
    return self.nome
  
class Aluno(models.Model):
  nome = models.CharField(max_length=100)
  cursos = models.ManyToManyField(Curso)
  
  def __str__(self):
    return self.nome

class NotaCurso(models.Model):
  aluno = models.ForeignKey(Aluno, on_delete= models.CASCADE)
  curso = models.ForeignKey(Curso, on_delete= models.CASCADE)
  nota = models.DecimalField(max_digits=5, decimal_places=2)
