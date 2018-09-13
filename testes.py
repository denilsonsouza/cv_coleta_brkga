from tools import *
from rota import Rota
# Lendo arquivos e gerando matriz de distancias
stringsarquivo = lerarquivo('distancias11.csv')
ncidades = len(stringsarquivo)
distancia = criarmatrizdistancia(stringsarquivo, ncidades)
stringsarquivo = lerarquivo('premios11.csv')
premios = criarvetorvalores(stringsarquivo, ncidades)
stringsarquivo = lerarquivo('penalties11.csv')
penalidades = criarvetorvalores(stringsarquivo, ncidades)

# Gerando populacao inicial
tampop = 10
porcentagemcorte = 0.5
premiominimo = 7932
populacao = gerarpopulacaoaleatoria(ncidades, tampop, distancia, porcentagemcorte, premiominimo, premios, penalidades)
populacao = sorted(populacao, key=lambda rota: rota.custo)
# Fazendo as geracoes
melhor = None
ngeracoes = 3

nfilhos = tampop
filhos = gerarfilhos(tampop, populacao, ncidades, distancia, nfilhos, premios, penalidades, premiominimo)
filhos = sorted(filhos, key=lambda rota: rota.custo)

# Mutações
mutantes = gerarmutantes(tampop, ncidades, distancia, porcentagemcorte, premiominimo, premios, penalidades)
mutantes = sorted(mutantes, key=lambda rota: rota.custo)
# Ver quem passa para proxima geracao:
populacao = sobreviver(populacao, tampop, filhos, mutantes)

printpop(populacao)
printpop(filhos)
printpop(mutantes)

