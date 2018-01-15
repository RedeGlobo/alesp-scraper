# -*- coding: utf-8 -*-
"""
Scraper de lotação de funcionários da Assembleia Legislativa do Estado de São Paulo
Criado em 2 de janeiro de 2018, às 22:06:26
@author: rodolfoviana
"""

import urllib.request
import xml.etree.cElementTree as et
import pandas as pd

req = urllib.request.urlopen('http://www.al.sp.gov.br/repositorioDados/administracao/funcionarios_lotacoes.xml')


def getvalueofnode(node):
    return node.text if node is not None else None


parsed_xml = et.parse(req)
dfcols = ['data_inicio', 'data_fim', 'nome', 'id_ua', 'ua']

df_xml = pd.DataFrame(columns=dfcols)

for node in parsed_xml.getroot():
    data_inicio = node.find('DataInicio')
    data_fim = node.find('DataFim')
    nome = node.find('NomeFuncionario')
    id_ua = node.find('IdUA')
    ua = node.find('NomeUA')

    df_xml = df_xml.append(
            pd.Series([getvalueofnode(data_inicio),
                       getvalueofnode(data_fim),
                       getvalueofnode(nome),
                       getvalueofnode(id_ua),
                       getvalueofnode(ua)], index=dfcols),
            ignore_index=True)

#   print(df_xml)

df_xml.to_csv('lotacao_funcionarios.csv', sep=';')

#<LotacaoFuncionario>
#    <DataFim>2008-08-28T00:00:00-03:00</DataFim>
#    <DataInicio>2007-03-27T00:00:00-03:00</DataInicio>
#    <IdUA>20447</IdUA>
#    <NomeFuncionario>ABDALLAH ABRÃO AUAD</NomeFuncionario>
#    <NomeUA>Gabinete do Deputado FERNANDO CAPEZ</NomeUA>
#</LotacaoFuncionario>
