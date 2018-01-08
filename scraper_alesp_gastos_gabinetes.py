# -*- coding: utf-8 -*-
"""
Crawler de despesas de gabinetes da Assembleia Legislativa do Estado de São Paulo
Criado em 8 de janeiro de 2018, às 00:49:56
@author: rodolfoviana
"""

import xml.etree.cElementTree as ET
import csv

tree = ET.parse('despesas_gabinetes.xml')
root = tree.getroot()

with open('resultado.csv', 'w', encoding='utf-8') as despesas:
    csvwriter = csv.writer(despesas, delimiter=';')
    cabecalhos = []
    count = 0
    for i in root.findall('despesa'):
	    dep = []
	    if count == 0:
		    deputado = i.find('Deputado').tag
		    cabecalhos.append(deputado)
		    matricula = i.find('Matricula').tag
		    cabecalhos.append(matricula)
		    ano = i.find('Ano').tag
		    cabecalhos.append(ano)
		    mes = i.find('Mes').tag
		    cabecalhos.append(mes)
		    tipo = i.find('Tipo').tag
		    cabecalhos.append(tipo)
		    cnpj = i.find('CNPJ').tag
		    cabecalhos.append(cnpj)
		    fornecedor = i.find('Fornecedor').tag
		    cabecalhos.append(fornecedor)
		    valor = i.find('Valor').tag
		    cabecalhos.append(valor)
		    csvwriter.writerow(cabecalhos)
		    count += 1

	    deputado = i.find('Deputado').text
	    dep.append(deputado)
	    matricula = i.find('Matricula').text
	    dep.append(matricula)
	    ano = i.find('Ano').text
	    dep.append(ano)
	    mes = i.find('Mes').text
	    dep.append(mes)
	    tipo = i.find('Tipo').text
	    dep.append(tipo)
	    cnpj = i.find('CNPJ').text if i.find('CNPJ') else None
	    dep.append(cnpj)
	    fornecedor = i.find('Fornecedor').text
	    dep.append(fornecedor)
	    valor = i.find('Valor').text
	    dep.append(valor)
	    csvwriter.writerow(dep)
despesas.close()
