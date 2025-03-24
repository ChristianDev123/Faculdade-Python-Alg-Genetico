from datetime import datetime
from dateutil.relativedelta import relativedelta
from copy import deepcopy
class LinhasAereas:
    def __init__(self, qtd_aeronaves):
        self.qtd_aeronaves = qtd_aeronaves
        self.restricoes = []
        # dominio (origem;destino;tempo_de_voo;qtd_voos)
        self.rotas = self.listagem_rotas_disponiveis()
        self.listagem_rotas_disponiveis()
        # indivíduo
        self.grade_de_voos = self.cria_grade_inicial()

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
            
            for _ in range(rota['qtd_voos_diarios']):
                data_hora_inicial += relativedelta(hours=1)
                response[i_aviao%self.qtd_aeronaves].append((rota['origem'], rota['origem'], data_hora_inicial))
                data_hora_inicial += relativedelta(hours=rota['tempo_de_voo'])
                response[i_aviao%self.qtd_aeronaves].append((rota['origem'], rota['destino'], data_hora_inicial))
                data_hora_inicial += relativedelta(minutes=30)
                response[i_aviao%self.qtd_aeronaves].append((rota['destino'],rota['destino'], data_hora_inicial))
                i_aviao += 1

            rotas.remove(rota)       
        return response    

    def adicionar_restricao(self, func_comp):
        self.restricoes.append(func_comp)
    
    def verifica_anomalo(self, individuo):
        for restricao in self.restricoes:
            if(restricao): return True
        return False

    def calcula_fitness(self, individuo):
        return 0
    
    def mutacao(self, individuo, genes):
        return []

    def cross_over(self, individuo1, individuo2):
        return []

QTD_AERONAVES = 10

problema = LinhasAereas(QTD_AERONAVES)
for aviao in problema.grade_de_voos:
    print(aviao)