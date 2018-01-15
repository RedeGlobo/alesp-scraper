# -*- coding: utf-8 -*-
"""
Crawler de despesas de gabinetes da Assembleia Legislativa do Estado de São Paulo
Criado em 8 de janeiro de 2018, às 00:49:56
@author: rodolfoviana
"""

from __future__ import print_function
from xml.sax import ContentHandler, parse
import requests
import xml.etree.cElementTree as ET
import csv

file = requests.get('http://www.al.sp.gov.br/repositorioDados/deputados/despesas_gabinetes.xml')

with open('despesas_gabinetes.xml','wb') as f:
	f.write(file.content)

class Handler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.despesa = {}
        self.despesas = []
        self.current_field = None
        self.in_despesa = False
        self.indent = 0

    def startElement(self, name, attrs):
        print('{}Start element: {}'.format('\t' * self.indent, name))
        self.indent += 1
        if self.in_despesa:
            self.current_field = name
            self.despesa[name] = ''

        if name == 'despesa':
            self.in_despesa = True

    def endElement(self, name):
        self.indent -= 1
        print('{}End element: {}'.format('\t' * self.indent, name))
        if name == 'despesa':
            self.despesas.append(self.despesa)
            self.despesa = {}
            self.in_despesa = False
            self.current_field = None

    def characters(self, content):
        if content.strip():
            print('{}chars: {}'.format('\t' * self.indent, repr(content)))
        if self.in_despesa and self.current_field:
            self.despesa[self.current_field] += content


def gravar_despesas(writer, despesas):
    cabecalhos = [
        'Deputado',
        'Matricula',
        'Ano',
        'Mes',
        'Tipo',
        'CNPJ',
        'Fornecedor',
        'Valor'
    ]
    writer.writerow(cabecalhos)

    for despesa in despesas:
        writer.writerow([despesa.get(c, '').strip() for c in cabecalhos])


def main():

    handler = Handler()
    with open('despesas_gabinetes.xml', 'r', encoding='utf-8') as xml_file:
        parse(xml_file, handler)

    print('Found {} despesas'.format(len(handler.despesas)))

    with open('despesas.csv', 'w', encoding='latin-1') as f_handle:
        writer = csv.writer(f_handle)
        gravar_despesas(writer, handler.despesas)


if __name__ == "__main__":
    main()
