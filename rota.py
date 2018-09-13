import os
from numpy import *
import random


class Rota(object):

    def __init__(self, caminho, matrizdistancia, premios, penalidades):
        self.caminho = caminho
        self.custo = self.calculacusto(caminho, matrizdistancia, penalidades)
        self.premio = self.calculapremio(caminho, premios)
        self.penalidade = self.calculapenalidade(caminho, penalidades)

    def calculacusto(self, caminhoentradanaotratado, matrizdistancia, penalidades):
        custo = 0
        caminhoentrada = []
        for espaco in caminhoentradanaotratado:
            if not espaco is None:
                caminhoentrada.append(espaco)
        # interar i vezes, sendo i o numero de elementos do caminho de entrada-1.
        # Ou seja, i vai receber as posicoes do caminho e caminhoentrada[i] o valor daquela posicao
        for i in range(len(caminhoentrada) - 1):
            custo += float(matrizdistancia[caminhoentrada[i]][caminhoentrada[i + 1]])
        custo += float(matrizdistancia[caminhoentrada[len(caminhoentrada) - 1]][caminhoentrada[0]])
        #calcula o numero de cidades.
        ncidades = len(matrizdistancia)
        penalidade = 0
        # iterar entre 0 e ncidades-1
        for i in range(ncidades):
            if not i in caminhoentrada: #caso a posicao nao esteja no caminho:
                penalidade+=float(penalidades[i])  # adicionar a penalidade daquela posicao
        custo += penalidade # somar penalidade a custo

        return custo

    def calculapremio(self, caminhoentradanaotratado, premios):
        premio = 0
        caminhoentrada = []
        for espaco in caminhoentradanaotratado:
            if not espaco is None:
                caminhoentrada.append(espaco)
        for index in caminhoentrada:
            premio += float(premios[index])
        return premio

    def calculapenalidade(self, caminhoentradanaotratado, penalidades):
        penalidade = 0
        caminhoentrada = []
        for espaco in caminhoentradanaotratado:
            if not espaco is None:
                caminhoentrada.append(espaco)
        for index in caminhoentrada:

            penalidade += float(penalidades[index])
        return penalidade

    def intersecao(self,lista1, lista2):
        lista3 = []
        for n in lista1:
            if not n in lista2:
                lista3.append(n)
        return lista3