from django.db import models
from django.utils import timezone
from datetime import datetime

    
class FuncionalidadesBasicas(models.Model):
    """
    Modelo para armazenar funções básicas de um projeto.
    
    Atributos:
        nome (str): O nome da função básica.
        descricao (str): Descrição da função básica.
        concluida (bool): Indica se a função básica foi concluída.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    concluida = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
    
    def funcao_concluida(self):
        """
        Marca a função básica como concluída.
        """
        self.concluida = True
        self.save()
    
    
    
class EscolhasDificuldades:
    """
    Classe auxiliar para definir as escolhas de dificuldade do projeto.
    """
    DIFICULDADE_CHOICES = [
        ('simples', 'Simples'),
        ('intermediario', 'Intermediario'),
        ('complexo', 'Complexo'),
        ('falta de recursos', 'Falta de recursos'),
        ('prazos apertados', 'Prazos apertados'),
        ('falta de experiencia', 'Falta de experiência'),
        ('complexidade do projeto', 'Complexidade do projeto'),
        ('falta de comunicacao', 'Falta de comunicação'),
        ('falta de suporte da equipe', 'Falta de suporte da equipe'),
        ('mundancas constantes de requisitos', 'Mundanças constantes de requisitos'),
        ('conflitos de interesse', 'Conflitos de interesse'),
        ('problema de integracao', 'Problemas de integração'),
        ('outros', 'Outros'),
    ]


class EstadoProjeto:
    """
    Classe auxiliar para definir as escolhas de dificuldade do projeto.
    """
    ESTADOS_PROJETOS = (
        ('andamento', 'Em andamento'),
        ('pausado', 'Pausado'),
        ('finalizado', 'Finalizado'),
    )


class Prioridade:
    """
    Classe auxiliar para definir as escolhas de dificuldade do projeto.
    """
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]



class Projeto(models.Model):
    """
    Modelo para representar um projeto.

    Atributos:
        nome (str): Nome do projeto.
        descricao (str): Descrição do projeto.
        funcoes_basicas (ManyToManyField): Funções básicas associadas ao projeto.
        dificuldade (str): Nível de dificuldade do projeto.
        prioridade (str): Prioridade do projeto.
        total_horas_gastas (float): Total de horas gastas no projeto.
        horas_previstas_por_dia (float): Horas previstas de trabalho por dia.
        email_usuario (str): Email do usuário responsável pelo projeto.
        dia_trabalho (ManyToManyField): Dias de trabalho associados ao projeto.
        estado_projeto (str): Estado atual do projeto.
        data_criada (DateTimeField): Data de criação do projeto.
        data_inicio (DateTimeField): Data de início do projeto.
        data_termino (DateTimeField): Data de término do projeto.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    funcoes_basicas = models.ManyToManyField('FuncionalidadesBasicas')
    dificuldade = models.CharField(max_length=50, choices=EscolhasDificuldades.DIFICULDADE_CHOICES)
    prioridade = models.CharField(max_length=10, choices=Prioridade.PRIORIDADE_CHOICES)
    total_horas_gastas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    horas_previstas_por_dia = models.DecimalField(max_digits=5, decimal_places=2)
    email_usuario = models.EmailField(null=True, blank=True)
    dia_trabalho = models.ManyToManyField('DiaTrabalho')
    estado_projeto = models.CharField(max_length=50, choices=EstadoProjeto.ESTADOS_PROJETOS)
    data_criada = models.DateTimeField(auto_now_add=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_termino = models.DateTimeField(null=True, blank=True)
    
    
    class Meta: 
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-total_horas_gastas']
    
    def __str__(self):
        return self.nome
    
    
    @property
    def days_ago(self):
        current_date = timezone.now()
        difference = current_date - self.data_criada
        return difference.days

    
    @property
    def hours_minutes_ago(self):
        current_date = timezone.now()
        difference = current_date - self.data_criada
        minutes, _ = divmod(difference.seconds, 60)
        if difference.days >= 1:
            return f"{difference.days} dias"
        elif difference.seconds >= 3600:
            return f"{difference.seconds // 3600} horas"
        else:
            return f"{minutes} minutos"
    
    
    def get_nome(self):
        return self.nome
    
    
    def set_nome(self, nome):
        self.nome = nome
        self.save()
        

    def get_estado(self):

        return self.estado_projeto
    
    
    def get_email(self):
        return self.email_usuario


    def get_horas_previstas_por_dia(self):
        """
        Retorna o número de horas previstas por dia para o projeto.

        Returns:
            Decimal: O número de horas previstas por dia para o projeto.
        """
        return self.horas_previstas_por_dia
    
    
    def set_horas_previstas_por_dia(self, horas):
        
        """
        Define o número de horas previstas por dia para o projeto e salva no banco de dados.

        Args:
            horas (Decimal): O número de horas previstas por dia para o projeto.
        """
        
        self.horas_previstas_por_dia = horas
        self.save()

        
    def get_dificuldade(self):
        
        return self.dificuldade


    def horas_gastas(self, tempo_feito):

        self.total_horas_gastas += tempo_feito
        self.save()
    
    
    
class DiaTrabalho(models.Model):
    """
    Modelo para representar um dia de trabalho em um projeto.
    
    Atributos:
        data (date): Data do dia de trabalho.
        horas (float): Horas trabalhadas no dia.
        bateu_hora_prevista (bool): Indica se as horas trabalhadas bateram com as horas previstas.
        passou_hora_prevista (bool): Indica se as horas trabalhadas ultrapassaram as horas previstas (considerando de 1 hora para cima).
    """
    
    data = models.DateField(auto_now_add=True)
    horas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bateu_hora_prevista = models.BooleanField(default=False)
    passou_hora_prevista = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)
    
    
    def data_trabalho(self):
        """
        Retorna a data do dia de trabalho formatada como uma string.

        Returns:
            str: A data do dia de trabalho formatada como uma string.
        """
        return str(self.data)
    
    
    def get_horas_feitas(self):
        """
        Retorna as horas feitas no dia.
        
        Returns:
            float: Horas feitas no dia.
        """
        return self.horas

    
    
    def bateu_meta(self):
        """
        Marca que as horas trabalhadas bateram com as horas previstas.
        """
        self.bateu_hora_prevista = True
        self.save()
        

    def nao_bateu_meta(self):
        """
        Marca que as horas trabalhadas ultrapassaram as horas previstas.
        """
        self.bateu_hora_prevista = False
        self.save()


    def ja_passou_hora_prevista(self):
        """
        Marca que as horas trabalhadas ultrapassaram as horas previstas no dia e salva no banco de dados.

        Esse método deve ser chamado quando as horas trabalhadas ultrapassam as horas previstas no dia de trabalho.
        Ele define o atributo passou_hora_prevista como True e salva essa alteração no banco de dados.

        """

        self.passou_hora_prevista = True
        self.save()