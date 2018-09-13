from timeit import timeit

from tools import *
import time

from cv_coleta_brkga.rota import Rota


def main():
    # Lendo arquivos e gerando matriz de distancias
    stringsarquivo = lerarquivo('distancias11.csv')
    ncidades = len(stringsarquivo)
    distancia = criarmatrizdistancia(stringsarquivo, ncidades)
    stringsarquivo = lerarquivo('premios11.csv')
    premios = criarvetorvalores(stringsarquivo, ncidades)
    stringsarquivo = lerarquivo('penalties11.csv')
    penalidades = criarvetorvalores(stringsarquivo, ncidades)

    inicio = time.time()

    # Gerando populacao inicial
    tampop = 100
    porcentagemcorte = 0.5
    premiominimo = 30546
    populacao = gerarpopulacaoaleatoria(ncidades, tampop, distancia, porcentagemcorte, premiominimo, premios, penalidades)
    populacao = sorted(populacao, key=lambda rota: rota.custo)  # Ordenacao da populacao

    # Fazendo as geracoes
    melhor = None
    ngeracoes = 1000
    for i in range(0, ngeracoes):
        #aumenta o tempo!!!
        #print('it:' + str(i))
        # Cruzamentos
        nfilhos = tampop
        filhos = gerarfilhos(tampop, populacao, ncidades, distancia, nfilhos, premios, penalidades, premiominimo)
        filhos = sorted(filhos, key=lambda rota: rota.custo)
        # Mutações
        mutantes = gerarmutantes(tampop, ncidades, distancia, porcentagemcorte, premiominimo, premios, penalidades)
        mutantes = sorted(mutantes, key=lambda rota: rota.custo)

        # Ver quem passa para proxima geracao:
        populacao = sobreviver(populacao, tampop, filhos, mutantes)
        populacao = sorted(populacao, key=lambda rota: rota.custo)


        # Salvando e exibindo melhor
        if melhor is None:
            melhor = populacao[0]

            print('Melhor custo: ' + str(melhor.custo))
        else:
            if populacao[0].custo < melhor.custo:
                melhor = populacao[0]


                print('Melhor custo: ' + str(melhor.custo))
                print('Caminho: ' + str(melhor.caminho))
    #Tempo final para execucao
    fim = time.time()
    final = fim - inicio

    print('Melhor solucao encontrada: ' + str(melhor.custo))
    print('Melhor solucao encontrada[caminho]: ' + str(melhor.caminho))
    print('Premio encontrado[caminho]: ' + str(melhor.premio))


    caminhoentrada = [x for x in range(0,27)]
    penalidadeTest = 0
    caminhoentrada = Rota.intersecao('__main__',caminhoentrada,melhor.caminho)
    for index in caminhoentrada:
        penalidadeTest += float(penalidades[index])

    print('Penalidades encontrado[caminho]: ' +str(penalidadeTest))
    print('Custo da Rota:' +str(melhor.custo - penalidadeTest))
    print('Tempo de execução: ' +str(final))

if __name__ == '__main__':
    main()

