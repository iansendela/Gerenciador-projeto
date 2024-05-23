from django import forms
from .models import Projeto, FuncionalidadesBasicas, DiaTrabalho


class FormProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'dificuldade', 'prioridade', 'estado_projeto', 'horas_previstas_por_dia']


class FuncaoForm(forms.ModelForm):
    class Meta:
        model = FuncionalidadesBasicas
        fields = ['nome', 'descricao']
        
        

class DiaTrabalhoForm(forms.ModelForm):
    class Meta:
        model = DiaTrabalho
        fields = ['horas']
