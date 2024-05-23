from django.shortcuts import get_object_or_404
from .models import FuncionalidadesBasicas, Projeto


def criar_funcao_para_projeto(nome_projeto, nome_funcao, descricao_funcao):
    # Obtém o projeto pelo nome (você pode ajustar isso necessario)
    projeto = get_object_or_404(Projeto, nome=nome_projeto)

    # Cria uma nova função basica associada ao projeto
    
    nova_funcao = FuncionalidadesBasicas.objects.create(nome=nome_funcao, descricao=descricao_funcao, )

    # Adiciona a nova funcao ao projeto
    projeto.funcoes_basicas.add(nova_funcao)