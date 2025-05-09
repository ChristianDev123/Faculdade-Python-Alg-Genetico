from copy import deepcopy
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

class GradeVoo:
    def __init__(self, grade):
        self.grade = grade
        self.fitness = self.calc_fitness()
        self.horario_inicio = datetime(2025,6,4,0,0,0)

    def encontrar_possiveis_rotas(self, origem):
        response = []
        for i_aviao, aviao in enumerate(self.grade):
            for i_rota, rota in enumerate(aviao):
                if(rota[0] == origem):
                    response.append((i_aviao, i_rota))
        return response

    def swap(self, de:tuple, para:tuple):
        response = deepcopy(self.grade)
        rota_atual = response[de[0]][de[1]]
        response[de[0]][de[1]] = response[para[0]][para[1]]
        response[para[0]][para[1]] = rota_atual
        return response

    def recalcular_tempo(self, grade):
        for i_aviao, aviao in enumerate(grade):
            horario_inicio = deepcopy(self.horario_inicio)
            for i_rota, rota in enumerate(aviao):
                horario_embarque = rota[2]
                horario_chegada = rota[3]
                copia_rota = list(rota)

                if(i_rota != 0): horario_inicio += relativedelta(hours=1)
                copia_rota[2] = horario_inicio
                horario_inicio += relativedelta(hours=((horario_chegada-horario_embarque).seconds/3600))
                copia_rota[3] = horario_inicio
                horario_inicio += relativedelta(minutes=30)
                copia_rota[4] = horario_inicio
                grade[i_aviao][i_rota] = tuple(copia_rota)
        return grade

    def mutacao(self):
        mutacoes = []
        grade = deepcopy(self.grade)
        # identificacao de problema
        destino_anterior = grade[0][0][1]
        for i_aviao, aviao in enumerate(grade):
            for i_rota, rota in enumerate(aviao):
                if(i_rota != 0 and destino_anterior != rota[0]):
                    # possibilidade de mudanças
                    possibilidades = self.encontrar_possiveis_rotas(destino_anterior)
                    for possibilidade in possibilidades:
                        nova_grade = self.swap((i_aviao, i_rota),possibilidade)
                        nova_grade = self.recalcular_tempo(nova_grade)
                        mutacoes.append(nova_grade)

                    return mutacoes
                destino_anterior = rota[1]
        return mutacoes

    def calc_fitness(self):
        response = 0
        rota_anterior = self.grade[0]
        for aviao in self.grade:
            for i_rota, rota in enumerate(aviao):
                if(i_rota == 0): continue
                if(rota_anterior[1] != rota[0]):
                    response -= 1000
                else:
                    response += 1
                
                response -= (rota[4]-rota[2]).seconds/(60*60)
                rota_anterior = rota
        return response
    
    def cross_over(self, grade2):
        linhas = len(self.grade)
        colunas = len(self.grade[0])
        metade = colunas // 2  # Ponto de divisão das colunas

        # Criando a matriz mesclada
        matriz_resultante = []
        for i in range(linhas):
            nova_linha = self.grade[i][:metade] + self.grade[i][metade:]  # Pega metade de cada matriz
            matriz_resultante.append(nova_linha)
        matriz_resultante = self.recalcular_tempo(matriz_resultante)
        return matriz_resultante    
                 
    def __lt__(self, grade2):
        return self.fitness > grade2.fitness

    def __repr__(self):
        representacao = ''
        molde = ''
        for num_aviao, aviao in enumerate(self.grade):
            molde += f'\n\n Avião {num_aviao + 1} ({self.fitness}): \n\n'
            for rota in aviao:
                data_embarque = rota[2].strftime('%Y-%m-%d %H:%M:%S')
                data_voo = rota[3].strftime('%Y-%m-%d %H:%M:%S')
                data_desembarque = rota[4].strftime('%Y-%m-%d %H:%M:%S')
                molde += f"{rota[0]} - {rota[1]} | Embarque: {data_embarque} | Chegada: {data_voo} | Desembarque: {data_desembarque}\n"
        representacao += molde
        return representacao