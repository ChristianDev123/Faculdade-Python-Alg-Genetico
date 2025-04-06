from datetime import datetime
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from GradeVoo import GradeVoo
from FilaPrioridade import FilaPrioridade

class LinhasAereas:
    def __init__(self, qtd_aeronaves, num_max_loops):
        self.qtd_aeronaves = qtd_aeronaves
        self.restricoes = []
        # dominio (origem;destino;tempo_de_voo;qtd_voos)
        self.rotas = self.listagem_rotas_disponiveis()
        # indivíduo
        self.grade_de_voos = GradeVoo(self.cria_grade_inicial())
        self.grade_de_voos_possiveis = FilaPrioridade(self.grade_de_voos)
        self.num_max_loops = num_max_loops

    def listagem_rotas_disponiveis(self):
        response = []
        with open('genes.txt','r', encoding='utf-8') as rotas:
            for line in rotas.readlines():
                origem, destino, tempo_de_voo, qtd_voos_diarios = line.replace('\n','').split(';')
                response.append({
                    'origem': origem,
                    'destino': destino,
                    'tempo_de_voo': float(tempo_de_voo),
                    'qtd_voos_diarios': int(qtd_voos_diarios)
                })
        return response

    def cria_grade_inicial(self):
        response = [[] for _ in range(self.qtd_aeronaves)]
        data_hora_inicial = datetime(2025,3,23,0,0,0)
        rotas = deepcopy(self.rotas)
        i_aviao = 0
        while(len(rotas) != 0):
            rota = rotas[0]
            # Gene: (Origem, Destino, Tempo Embarque, Tempo de Voo, Tempo de Desembarque)
            data_hora_inicial += relativedelta(hours=1)
            tempo_embarque = data_hora_inicial
            data_hora_inicial += relativedelta(hours=rota['tempo_de_voo'])
            tempo_voo = data_hora_inicial
            data_hora_inicial += relativedelta(minutes=30)
            tempo_desembarque = data_hora_inicial
            response[i_aviao%self.qtd_aeronaves].append((rota['origem'], rota['destino'], tempo_embarque, tempo_voo, tempo_desembarque))
            i_aviao += 1
            rotas.remove(rota)       
        return response    

    def adicionar_restricao(self, func_comp):
        self.restricoes.append(func_comp)
    
    def verifica_anomalo(self, individuo):
        for restricao in self.restricoes:
            if(restricao): return True
        return False

    def executar(self):
        for _ in range(self.num_max_loops):
            mutacoes = self.grade_de_voos.mutacao()
            mutacoes = [GradeVoo(mutacao) for mutacao in mutacoes]
            mutacoes = sorted(mutacoes, key=lambda x: x.fitness, reverse=True)
            if(len(mutacoes) > 0):
                self.grade_de_voos = mutacoes[0]

QTD_AERONAVES = 3

problema = LinhasAereas(QTD_AERONAVES, 1000)
problema.executar()
print(problema.grade_de_voos)