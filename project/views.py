from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormProjeto, FuncaoForm, DiaTrabalhoForm
from .models import Projeto, DiaTrabalho, FuncionalidadesBasicas
from datetime import date

# Cria um projeto
def criar_projeto(request):
    """
    Cria um novo projeto.

    Cria um novo projeto com base nos dados enviados pelo formulário.
    Redireciona para a página de visualização de todos os projetos após a criação.

    Returns:
        HttpResponse: Redireciona para a página de visualização de todos os projetos.
    """
    
    
    if request.method == 'POST':
        form = FormProjeto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos_projetos')
    else:
        form = FormProjeto()
        
    return render(request, 'form/adicionar_projeto.html', {'form': form})



# É a pagina inicial ele vai mostrar todos os projetos "em endamento"
def inicial(request):
    """
    Exibe a página inicial mostrando todos os projetos em andamento.

    Retorna uma renderização da página inicial com todos os projetos em andamento.

    Returns:
        HttpResponse: Renderização da página inicial com todos os projetos em andamento.
    """
    projetos = Projeto.objects.all()
    return render(request, 'visualizar/inicial.html', {'projetos': projetos})



# adiciona uma funcionalidade ao projeto
def adicionar_funcao(request, projeto_id):
    """
    Adiciona uma nova funcionalidade a um projeto específico.

    Adiciona uma nova funcionalidade ao projeto identificado por 'projeto_id' com base nos dados enviados pelo formulário.
    Redireciona para a página de detalhes do projeto após a adição da funcionalidade.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto ao qual a funcionalidade será adicionada.

    Returns:
        HttpResponse: Redireciona para a página de detalhes do projeto após a adição da funcionalidade.
    """
    projeto = Projeto.objects.get(pk=projeto_id)
    if request.method == 'POST':
        form = FuncaoForm(request.POST)
        if form.is_valid():
            funcao = form.save(commit=False)
            funcao.save()
            projeto.funcoes_basicas.add(funcao)
            # Redireciona para a página de detalhes do projeto após adicionar a funcionalidade
            return redirect('detalhes_projeto', projeto_id=projeto_id)
    else:
        form = FuncaoForm()
    return render(request, 'form/adicionar_funcao.html', {'form': form, 'projeto': projeto})



# Adicionar quantas horas do dia X o usuario se dedicou ao projeto
def adicionar_diasTrabalho(request, projeto_id):
    """
    Adiciona um registro de horas trabalhadas a um projeto específico.

    Adiciona um registro de horas trabalhadas ao projeto identificado por 'projeto_id' com base nos dados enviados pelo formulário.
    Redireciona para a página de detalhes do projeto após a adição do registro.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto ao qual o registro será adicionado.

    Returns:
        HttpResponse: Redireciona para a página de detalhes do projeto após a adição do registro.
    """
    projeto = Projeto.objects.get(pk=projeto_id)
    if request.method == 'POST':
        form = DiaTrabalhoForm(request.POST)
        if form.is_valid():
            diaTrabalho = form.save(commit=False)
            diaTrabalho.save()
            projeto.dia_trabalho.add(diaTrabalho)
            return redirect('detalhes_projeto', projeto_id=projeto_id)
    else:
        form = DiaTrabalhoForm()
    
    return render(request, 'form/form_trabalho.html', {'form':form, 'projeto': projeto})


# Mostrar detalhes do projeto X
def detahes_projeto(request, projeto_id):
    
    projeto = Projeto.objects.get(pk=projeto_id)
    
    dias_trabalho = DiaTrabalho.objects.filter(projeto=projeto)
    
    hora_total_gasta = sum(dia.get_horas_feitas() for dia in dias_trabalho)
    
    exibir_botao = True

    tamanho_funcao = projeto.funcoes_basicas.count()
    
    
    today = date.today()
    
    today_texto = str(today)
    
    
    for trabalho in dias_trabalho:
        
        trabalho_texto = str(trabalho)
        
        if trabalho_texto == today_texto and trabalho.horas > 0:
            exibir_botao = False # ele esconde o botão de adcionar horas trabalha
            
    
    



    context = {
        'projeto': projeto,
        'dias_trabalho': dias_trabalho,
        'hora_total_gasta': hora_total_gasta,
        'tamanho_funcao': tamanho_funcao,
        'exibir_botao': exibir_botao,
    }
    
    for trabalho in dias_trabalho:
        if trabalho.horas >= projeto.horas_previstas_por_dia:
            trabalho.bateu_meta()
        else:
            trabalho.nao_bateu_meta()
    
    return render(request, 'visualizar/detalhes_projeto.html', context)


# Marca a Funcionalidade X como concluida
def conclui_funcao(request, projeto_id):
    """
    Marca uma função básica como concluída em um projeto específico.

    Marca uma função básica como concluída no projeto identificado por 'projeto_id'.
    Redireciona para a página de detalhes do projeto após a conclusão da função.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto ao qual a função será marcada como concluída.

    Returns:
        HttpResponse: Redireciona para a página de detalhes do projeto após a conclusão da função.
    """
    projeto = get_object_or_404(FuncionalidadesBasicas, pk=projeto_id)
    projeto.funcao_concluida()
    return redirect('detalhes_projeto', projeto)



# Detalhes da Funcionalidade
def detahes_funcao(request, projeto_id):
    """
    Exibe os detalhes de uma função básica em um projeto específico.

    Exibe os detalhes da função básica identificada por 'projeto_id'.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID da função básica a ser visualizada.

    Returns:
        HttpResponse: Renderização da página de detalhes da função básica.
    """
    
    funcao = get_object_or_404(FuncionalidadesBasicas, pk=projeto_id)
    return render(request, 'visualizar/detalhes_funcao.html', {'funcao': funcao})


# Editar a Funcionalidade X
def update_funcao(request, projeto_id):
    """
    Atualiza os detalhes de uma função básica em um projeto específico.

    Atualiza os detalhes da função básica identificada por 'projeto_id' com base nos dados enviados pelo formulário.
    Redireciona para a página de detalhes do projeto após a atualização da função.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID da função básica a ser atualizada.

    Returns:
        HttpResponse: Renderização da página de atualização da função básica.
    """
    funcao = get_object_or_404(FuncionalidadesBasicas, pk=projeto_id)
    if request.method =='POST':
        form = FuncaoForm(request.POST, instance=funcao)
        if form.is_valid():
            form.save()
            return redirect('detalhes_projeto', projeto_id=projeto_id)
    else:
        form = FuncaoForm(instance=funcao)
        
    return render(request, 'update/update_funcao.html', {'form': form})


# Edita o projeto X
def update_projeto(request, projeto_id):
    """
    Atualiza os detalhes de um projeto específico.

    Atualiza os detalhes do projeto identificado por 'projeto_id' com base nos dados enviados pelo formulário.
    Redireciona para a página de visualização de todos os projetos após a atualização do projeto.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto a ser atualizado.

    Returns:
        HttpResponse: Redireciona para a página de visualização de todos os projetos após a atualização do projeto.
    """
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    if request.method == 'POST':
        form = FormProjeto(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('projetos', projeto_id=projeto_id)
    else:
        form = FormProjeto(instance=projeto)

    return render(request, 'update/update_projeto.html', {'form': form})


# visualiza todas as funções criadas de um projeto X
def todas_funcoes(request, projeto_id):
    """
    Exibe todas as funcionalidades de um projeto específico.

    Exibe todas as funcionalidades do projeto identificado por 'projeto_id'.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto a ser visualizado.

    Returns:
        HttpResponse: Renderização da página de visualização de todas as funcionalidades do projeto.
    """
    projeto = Projeto.objects.get(pk=projeto_id)

    return render(request, 'visualizar/todas_funcoes.html', {'projeto': projeto})



# serve para eu visualizar todos os projetos cadastrados
def todos_projetos(request):
    """
    Exibe todos os projetos cadastrados.

    Exibe todos os projetos cadastrados no sistema.

    Args:
        request (HttpRequest): Requisição HTTP.

    Returns:
        HttpResponse: Renderização da página de visualização de todos os projetos cadastrados.
    """
    
    
    # falta adicionar filtros

     
    dificuldade_selecionada = request.GET.get('dificuldade', '')
    prioridade_selecionada = request.GET.get('prioridade', '')
    status_selecionado = request.GET.get('status', '')
    
    
    projetos = Projeto.objects.all()
    
    # Filtra as tarefas com base no termo de pesquisa
    # Filtra as projetos com base na categoria
    if dificuldade_selecionada:
        projetos = Projeto.objects.filter(dificuldade=dificuldade_selecionada)

    # filtrar por prioriadade
    if prioridade_selecionada:
        projetos = projetos.filter(prioridade=prioridade_selecionada)


    # Filtrar com base no estados
    if status_selecionado:
        projetos = projetos.filter(estado_projeto=status_selecionado)
    
    
    
    
    context = {
        'projetos': projetos,
        'dificuldade_selecionada': dificuldade_selecionada,
        'prioridade_selecionada': prioridade_selecionada,
        'status_selecionado': status_selecionado,
    }

    return render(request, 'visualizar/todos_projetos.html', context )



# Apaga o projeto X com todos os seus detalhes
def apagar_projeto(request, projeto_id):
    """
    Apaga um projeto específico.

    Apaga o projeto identificado por 'projeto_id' e todos os seus detalhes associados.
    Redireciona para a página de visualização de todos os projetos após a exclusão.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID do projeto a ser excluído.

    Returns:
        HttpResponse: Redireciona para a página de visualização de todos os projetos após a exclusão.
    """
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    projeto.delete()
    return redirect('projetos')


# Apaga a funcionalidad X
def apagar_funcao(request, projeto_id):
    """
    Apaga uma funcionalidade específica.

    Apaga a funcionalidade identificada por 'projeto_id'.
    Redireciona para a página de detalhes do projeto após a exclusão.

    Args:
        request (HttpRequest): Requisição HTTP.
        projeto_id (int): ID da funcionalidade a ser excluída.

    Returns:
        HttpResponse: Redireciona para a página de detalhes do projeto após a exclusão.
    """
    funcao = get_object_or_404(FuncionalidadesBasicas, pk=projeto_id)
    funcao.delete()
    return redirect('detalhes_projeto')



# filtro no arquivo base.html
# ainda não está funcionar
def pesquisar(request):
    """
    Realiza uma pesquisa nos projetos cadastrados.

    Realiza uma pesquisa nos projetos cadastrados com base no termo de pesquisa fornecido.
    Exibe os resultados da pesquisa na página inicial.

    Args:
        request (HttpRequest): Requisição HTTP.

    Returns:
        HttpResponse: Renderização da página inicial com os resultados da pesquisa.
    """
    
    termo_pesquisa = request.GET.get('termo_pesquisa', '')  # Obtém o valor do campo de pesquisa
    
    # Filtra as tarefas com base no termo de pesquisa
    if termo_pesquisa:
        projetos = Projeto.objects.filter(nome__icontains=termo_pesquisa)
        
    
    context = {
        'projetos': projetos,
        'termo_pesquisa': termo_pesquisa,
    }
    
    
    return render(request, 'resultados_pesquisa.html', context)