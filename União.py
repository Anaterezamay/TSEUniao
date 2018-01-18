
# coding: utf-8

# In[ ]:


#Escolha um ano. Só temos os dados disponíveis a partir de 2006
ano = input ('Qual ano de eleição, a partir de 2006, você deseja consultar?')

#Faz o Download e Unzip os arquivos txt dos candidatos
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
zipurl = (f'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip')
print('Estamos apenas começando!')

with urlopen(zipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall('Candidatos')
print('Calma, seus candidatos por ano já foram selecionados.')

#Faz o Download e Unzip os arquivos txt dos bens
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
zipurl = (f'http://agencia.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_{ano}.zip')
print('Mais um pouquinho')
with urlopen(zipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall('Bens')
print('E agora os bens deles!')

import csv
import pandas as pd


estado = input('Digite a sigla do estado desejado:')
estado = estado.upper()

#Transformar o TXT em CSV - Bens dos candidatos
with open(f"Bens\\bem_candidato_{ano}_{estado}.txt", "r") as f:
    content = f.readlines()

with open(f"bem_candidato_{ano}_{estado}.csv", "w+") as csvfile:
    csvfile.writelines(content)
csvfile.close()  

#Abrindo e lendo o arquivo csv com o código e os bens dos candidatos
lista_bens = open(f'bem_candidato_{ano}_{estado}.csv', encoding='latin1')
leitor_bens = csv.reader(lista_bens, delimiter = ';')


#Limpando e pegando só as informações necessárias do arquivo
arquivo_saida = open(f'saidabens{estado}.csv', mode='w', encoding='latin1')
escritor =  csv.writer(arquivo_saida, lineterminator='\n')
escritor.writerow(['Ano', 'Codigo', 'Tipo', 'Descricao', 'Valor'])

#Vai gerar um novo arquivo em csv só com as colunas que a gente quer
for registro in leitor_bens:
    escritor.writerow([registro[2], registro[5], registro[7], registro[8], registro[9]])
arquivo_saida.close()



#Transformar o TXT em CSV - Lista dos candidatos com o código
with open(f"Candidatos\\consulta_cand_{ano}_{estado}.txt", "r") as f:
    content = f.readlines()

with open(f"consulta_cand_{ano}_{estado}.csv", "w+") as csvfile:
    csvfile.writelines(content)
csvfile.close()    

#Abrindo e lendo o arquivo csv com o nome e código dos candidatos
lista_nomes = open(f'consulta_cand_{ano}_{estado}.csv', encoding='latin1')
leitor_nomes = csv.reader(lista_nomes, delimiter = ';')



#Limpando e pegando só as informações necessárias do arquivo
arquivo_saida = open(f'saidacandidatos{estado}.csv', mode='w', encoding='latin1')
escritor = csv.writer(arquivo_saida, lineterminator='\n')
escritor.writerow(['Ano', 'Cidade', 'Cargo', 'Nome', 'Nome Urna', 'Codigo', 'Situacao'])

#Vai gerar um novo arquivo em csv só com as colunas que a gente quer
for registro in leitor_nomes:
    escritor.writerow([registro[2], registro[7], registro[9], registro[10], registro[14], registro[11], registro[-2]])
arquivo_saida.close()

#No final, ele gera dois arquivos: o saidacandidato.csv e o saidabens.csv. Agora vamos para a parte 2 do código:

#Agora é a parte da junção das duas tabelas e a filtragem utilizando o pandas:

#Pegar o código do estado digitado antes e salvar na variável
estado_analise = estado
estado_analise = estado_analise.upper()


#Ler os arquivos de saída já limpos com o pandas
bens_analise = pd.read_csv(f'saidabens{estado_analise}.csv', encoding='latin1')
candidatos_analise = pd.read_csv(f'saidacandidatos{estado_analise}.csv', encoding='latin1')

#Juntar os dois arquivos de saída em um só com a correspondência pelo código de cada candidato
juntar_tabelas = pd.merge(bens_analise, candidatos_analise, on='Codigo')

#Criando um filtro com o pandas para escolher o cargo que será analisado
cargo_escolhido = input('Qual cargo você quer analisar? Ex.: Vereador, Deputado, Prefeito ou Vice-prefeito. MAs não se esqueça de ver quais cargos estavam abertos aquele ano, viu? ')
cargo_escolhido = cargo_escolhido.upper()
filtrado = juntar_tabelas[juntar_tabelas.Cargo == cargo_escolhido]



#Criando um filtro com o pandas para escolher a situação analisada.
#Não consegui fazer funcionar esse filtro. Ele não aceita as duas situações que podem ocorrer na situação ELEITOS

situacao_escolhida = input('Qual a situação politica você quer? Eleitos, suplentes ou não eleitos?')
situacao_escolhida = situacao_escolhida.upper()
if situacao_escolhida == 'ELEITOS':
    filtrado_situacao = filtrado[(filtrado.Situacao == 'ELEITO POR QP') | (filtrado.Situacao == 'ELEITO POR MÉDIA')]
elif situacao_escolhida == 'SUPLENTES':
    filtrado_situacao = filtrado[filtrado.Situacao == 'SUPLENTE']
elif situacao_escolhida == 'NÃO ELEITOS':
    filtrado_situacao = filtrado[filtrado.Situacao == 'NÃO ELEITO']


if ano == '2008'or'2012'or'2016':
    
    #Criando um filtro para cidade
    cidade_escolhida = input(f'Qual cidade do estado {estado_analise} você quer analisar?')
    cidade_escolhida = cidade_escolhida.upper()
    filtrado_cidade = filtrado_situacao[filtrado_situacao.Cidade == cidade_escolhida]



#Somando o total dos bens de cada politico
total_cada_politico = filtrado.groupby('Codigo').Valor.sum()


#Salvando a tabela limpa e analisada como csv
filtrado_cidade.to_csv(f'tabelafinal{estado_analise}.csv')

