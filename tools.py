import os
from numpy import *
import random
import rota
import timeit
from copy import copy
import statistics
from fractions import Fraction as F
from decimal import Decimal as D


def lerarquivo(nomearquivo):
    ref_arquivo = open(nomearquivo, "r")
    linhas = ref_arquivo.readlines()
    ref_arquivo.close()
    return linhas


def criarmatrizdistancia(stringsarquivo, ncidades):
    matrizdistancia = []
    for l in range(0, ncidades):
        colunas = []
        linhastring = stringsarquivo[l].replace("\n", "").split(';')
        for c in range(0, ncidades):
            colunas.append(linhastring[c])
        matrizdistancia.append(colunas)
    return matrizdistancia


def criarvetorvalores(stringsarquivo, ncidades):
    colunas = []
    linhastring = stringsarquivo[0].replace("\n", "").split(';')
    for c in range(0, ncidades):
        colunas.append(linhastring[c])

    return colunas


def solucaogulosaaleatoria(porcentagemcorte, ncidades, distancia, premiominimo, premios):
    # Sorteando a primeira cidade
    # cidadeinicial = random.choice(range(ncidades))
    cidadeinicial = 0
    premioatual = float(premios[0])
    # print(cidadeinicial)


def calculacusto(caminho, matrizdistancia):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += float(matrizdistancia[caminho[i]][caminho[i + 1]])

    custo += float(matrizdistancia[caminho[len(caminho) - 1]][caminho[0]])
    return custo


def gerarcaminhoaleatorio(ncidades):
    caminhoaleatiorio = random.sample(range(ncidades), ncidades)
    return caminhoaleatiorio


def gerarpopulacaoaleatoria(ncidades, tampop, matrizdistancia, porcentagemcorte, premiominimo, premios, penalidades):
    populacao = []
    for i in range(tampop):
        solucao = solucaogulosaaleatoria(porcentagemcorte, ncidades, matrizdistancia, premiominimo, premios)
        rotasolucao = rota.Rota(solucao, matrizdistancia, premios, penalidades)
        populacao.append(rotasolucao)
    return populacao


def split(w):
    x = w[0]
    left = []
    right = []
    for i in range(1, len(w)):
        if w[i].custo <= x.custo:
            left += [w[i]]
        else:
            right += [w[i]]
    return left, x, right


def quicksort(w):
    if len(w) < 2:
        return w
    else:
        w1, x, w2 = split(w)
        return quicksort(w1) + [x] + quicksort(w2)


def printpop(populacao):
    for i in populacao:
        printrota(i)


def printrota(rota):
    print(rota.caminho)
    print(rota.custo)
    print(rota.premio)


def caminhofilhovazio(ncidades):
    filhocaminho = []
    for i in range(ncidades):
        filhocaminho.append(False)
    return filhocaminho


def tamfatia(ncidades, porcentagemdafatia):
    return int(ncidades * porcentagemdafatia)


def cortarpai2(pai2, fimcorte, ncidades, cortepai1):
    primeiravez = 0
    cortepai2 = []
    rodar = True
    i = fimcorte
    while rodar:
        if i == fimcorte and primeiravez == 0 or i != fimcorte:

            if not pai2.caminho[i] in cortepai1:
                cortepai2.append(pai2.caminho[i])
        if i == fimcorte:
            if primeiravez == 0:
                primeiravez = 1
            else:
                rodar = False
        if i + 1 == ncidades:
            i = -1
        i += 1
    return cortepai2


def porcorte2nofilho(fimcorte, cortepai2, filhocaminho, ncidades):
    primeiravez = 0
    rodar = True
    i = fimcorte
    j = 0
    for corte in cortepai2:
        filhocaminho[i] = corte
        i += 1
        if i == ncidades:
            i = 0


def cruzamento(entradapai1, entradapai2, ncidades, distancia, premios, penalidades):
    pai1 = entradapai1
    pai2 = entradapai2
    pai1.caminho = entradapai1.caminho.copy()
    pai2.caminho = entradapai2.caminho.copy()
    diferencatam = ncidades - len(pai1.caminho)
    for i in range(diferencatam):
        pai1.caminho.append(None)
    diferencatam = ncidades - len(pai2.caminho)
    for i in range(diferencatam):
        pai2.caminho.append(None)

    # Criando caminho filho vazio
    filhocaminho = caminhofilhovazio(ncidades)

    # Escolhendo qual fatia do pai 1
    tamslice = tamfatia(ncidades, 0.4)
    iniciocorte = random.sample(range(ncidades - tamslice), 1)[
        0]  # random sample ira pegar uma casa valida para iniciar o corte.
    fimcorte = iniciocorte + tamslice

    # Corte no pai 1
    cortepai1 = pai1.caminho[iniciocorte:fimcorte]

    # Corte no pai 2
    cortepai2 = cortarpai2(pai2, fimcorte, ncidades, cortepai1)

    # Pondo no caminho filho
    filhocaminho[iniciocorte:fimcorte] = cortepai1
    porcorte2nofilho(fimcorte, cortepai2, filhocaminho, ncidades)

    # Criando filho
    filho = rota.Rota(filhocaminho, distancia, premios, penalidades)

    return filho


def getquantelite(tampop):
    quantelite = int(tampop * 0.1)
    if quantelite < 1:
        quantelite = 1
    return quantelite


def gerarfilhos(tampop, populacao, ncidades, distancia, nfilhos, premios, penalidades, premiominimo):
    # Selecionar pais

    quantelite = getquantelite(tampop)
    elite = populacao[:quantelite]
    nelite = populacao[quantelite:]
    filhos = []
    # Cruzamentos
    for i in range(0, nfilhos):
        pai1 = elite[random.randrange(0, quantelite)]
        pai2 = nelite[random.randrange(quantelite, len(nelite))]
        filho = cruzamento(populacao[0], populacao[1], ncidades, distancia, premios, penalidades)
        if filho.premio >= premiominimo:
            filhos.append(filho)
        else:
            i = i - 1
    return filhos


def gerarmutantes(tampop, ncidades, distancia, porcentagemcorte, premiominimo, premios, penalidades):
    nmutantes = int(tampop * 0.3)
    mutantes = []
    for i in range(0, nmutantes):
        solucao = solucaogulosaaleatoria(porcentagemcorte, ncidades, distancia, premiominimo, premios)
        mutante = rota.Rota(solucao, distancia, premios, penalidades)
        mutantes.append(mutante)
    return mutantes


# retorna o i de um individuo
def roulettewheel(possivelpopulacao):
    #
    somatotalfitness = 0
    for individuo in possivelpopulacao:
        somatotalfitness += individuo.fitness
    #
    seletor = random.uniform(0, somatotalfitness)
    roleta = 0
    i = 0
    for individuo in possivelpopulacao:
        roleta += individuo.fitness
        if roleta > seletor:
            return i
        i += 1


def sobreviver(populacao, tampop, filhos, mutantes):
    # Ver quem passa para proxima geracao:
    # Elite
    quantelite = getquantelite(tampop)
    elite = populacao[:quantelite]
    nelite = populacao[quantelite:]
    # 1) Juntar elite,melhores da pop passada e pop nova num grande vetor
    possivelpopulacao = []
    possivelpopulacao = concatenate((elite, nelite[:int(tampop / 2)]), axis=0)
    possivelpopulacao = concatenate((possivelpopulacao, filhos), axis=0)
    # 2) Ordenar esse grande vetor e cortar solucoes ruins
    possivelpopulacao = sorted(possivelpopulacao, key=lambda rota: rota.custo)
    possivelpopulacao = possivelpopulacao[:tampop - len(mutantes)]
    # 3) Adicionar as mutações e ordenar outra vez
    possivelpopulacao = concatenate((possivelpopulacao, mutantes), axis=0)
    possivelpopulacao = sorted(possivelpopulacao, key=lambda rota: rota.custo)
    sobreviventes = possivelpopulacao
    return sobreviventes

    return sobreviventes


def atualizardistanciaparaatualcitycands(citycands, cidadeatual, matrizdistancia):
    for city in citycands:
        city.atualizardistanciaparacidadeatual(cidadeatual, matrizdistancia)
    return citycands


from cidadecandidata import CidadeCandidata


def getslicesorteavel(porcentagem, ncidades, citycands):
    porcentagemcorte = porcentagem
    slicesorteavel = int(1 + porcentagemcorte * (len(citycands) - 1))
    return slicesorteavel


def gerarlistacidadescandidatas(ncidades, cidadeinicial, matrizdistancia):
    citycands = []
    for i in range(ncidades):
        if not i == cidadeinicial:
            citycand = CidadeCandidata(i, cidadeinicial, matrizdistancia)
            citycands.append(citycand)

    # Ordenando pela distancia para a distancia atual
    citycands = sorted(citycands, key=lambda CidadeCandidata: CidadeCandidata.distanciaparacidadeatual)
    # printcidadescandidatas(citycands)
    return citycands


def solucaogulosaaleatoria(porcentagemcorte, ncidades, distancia, premiominimo, premios):
    # Sorteando a primeira cidade
    # cidadeinicial = random.choice(range(ncidades))
    cidadeinicial = 0
    premioatual = float(premios[0])
    # print(cidadeinicial)

    # Criando uma lista com cidades candidatas.
    citycands = gerarlistacidadescandidatas(ncidades, cidadeinicial, distancia)

    # Vetor de solução
    solucaogulosa = []
    solucaogulosa.append(cidadeinicial)
    # Fazer ate completar solucao
    while len(solucaogulosa) < ncidades and premioatual <= premiominimo:
        # Ver quantas cidades entram no sorteio
        slicesorteavel = getslicesorteavel(porcentagemcorte, ncidades, citycands)
        citycands[:slicesorteavel]
        # Sorteio da nova cidade atual

        cidadeatual = random.choice(citycands[:slicesorteavel])
        # Adicionar cidade sorteada ao vetor de solucao e removê-lo das candida-tas
        premioatual += float(premios[cidadeatual.numero])
        solucaogulosa.append(cidadeatual.numero)
        citycands.remove(cidadeatual)

        # Atualizar lista de distancias para cidade atual e reordenar por essa distância
        citycands = atualizardistanciaparaatualcitycands(citycands, cidadeatual, distancia)
        citycands = sorted(citycands, key=lambda CidadeCandidata: CidadeCandidata.distanciaparacidadeatual)

    return solucaogulosa
