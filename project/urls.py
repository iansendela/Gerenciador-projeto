from django.urls import path
from project import views

urlpatterns = [
    path('criar_projeto/', views.criar_projeto, name='criar_projeto'),
    # URL para criar um novo projeto.
    
    path('', views.inicial, name='projetos'),
    # URL para a página inicial que mostra todos os projetos em andamento.

    path('adicionar_funcao/<int:projeto_id>/', views.adicionar_funcao, name='nova_funcao'),
    # URL para adicionar uma nova função básica a um projeto específico.

    path('detalhes_projeto/<int:projeto_id>/', views.detahes_projeto, name='detalhes_projeto'),
    # URL para exibir os detalhes de um projeto específico.

    path('adicionar_trabalho/<int:projeto_id>/', views.adicionar_diasTrabalho, name='adicionar_trabalho'),
    # URL para adicionar um registro de horas de trabalho a um projeto específico.

    path('marcar_concluida/<int:projeto_id>/', views.conclui_funcao, name='marcar_concluida'),
    # URL para marcar uma função básica como concluída em um projeto específico.

    path('detalhes_funcao/<int:projeto_id>/', views.detahes_funcao, name='detalhes_funcao'),
    # URL para exibir os detalhes de uma função básica em um projeto específico.

    path('update/funcao/<int:projeto_id>/', views.update_funcao, name='update_funcao'),
    # URL para atualizar os detalhes de uma função básica em um projeto específico.

    path('uptade/projeto/<int:projeto_id>/', views.update_projeto, name='update_projeto'),
    # URL para atualizar os detalhes de um projeto específico.

    path('todas_funcoes/<int:projeto_id>/', views.todas_funcoes, name='funcoes'),
    # URL para exibir todas as funcionalidades de um projeto específico.

    path('projetos/', views.todos_projetos, name='todos_projetos'),
    # URL para exibir todos os projetos cadastrados.

    path('apagar/projeto/<int:projeto_id>/', views.apagar_projeto, name='apagar_projeto'),
    # URL para apagar um projeto específico.

    path('apagar/funcao/<int:projeto_id>/', views.apagar_funcao, name='apagar_funcao'),
    # URL para apagar uma funcionalidade específica.

    path('pesquisar/', views.pesquisar, name='pesquisar'),
    # URL para realizar uma pesquisa nos projetos cadastrados.
]
