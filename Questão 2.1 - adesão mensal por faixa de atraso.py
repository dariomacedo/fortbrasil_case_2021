# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 07:57:24 2021

@author: dario
"""

import pandas as pd
import numpy as np

df = pd.read_csv('Questão 2 - Base 1.txt', delimiter = "\t")
df['DT_ACORDO'] = pd.to_datetime(df['DT_ACORDO'])


#NU_DIAS_ATRASO > 180 & NU_DIAS_ATRASO < 241 -> Faixa 0
#NU_DIAS_ATRASO > 240 & NU_DIAS_ATRASO < 301 -> Faixa 1
#NU_DIAS_ATRASO > 300 & NU_DIAS_ATRASO < 361 -> Faixa 2
#NU_DIAS_ATRASO > 360 & NU_DIAS_ATRASO < 421 -> Faixa 3
#NU_DIAS_ATRASO > 420 & NU_DIAS_ATRASO < 481 -> Faixa 4
#NU_DIAS_ATRASO > 480 & NU_DIAS_ATRASO < 541 -> Faixa 5

def label_resultado (row):
    if (row['NU_DIAS_ATRASO'] < 241):
        return 0
    elif (row['NU_DIAS_ATRASO'] < 301):
        return 1
    elif (row['NU_DIAS_ATRASO'] < 361):
        return 2
    elif (row['NU_DIAS_ATRASO']  < 421):
        return 3
    elif (row['NU_DIAS_ATRASO'] < 481):
        return 4
    elif (row['NU_DIAS_ATRASO'] < 541):
        return 5
    
df['FAIXA_ATRASO'] = df.apply(lambda row: label_resultado(row), axis=1)

lista = [11,3,4,6]
aux = 0
#adesao_mensal = list(range(len(lista)))

lista2 = [0,1,2,3,4,5]

adesao_mensal_por_faixa = np.zeros((len(lista2),len(lista)))

for i in lista:
    for j in lista2:
    #print(lista[aux])
        ocorrencias = df[(pd.DatetimeIndex(df['DT_ACORDO']).month == i) & (df['RESPOSTA'] == 1) & (df['FAIXA_ATRASO'] == j )]
        n_ocorrencias = df[(pd.DatetimeIndex(df['DT_ACORDO']).month == i) & (df['FAIXA_ATRASO'] == j )]
        adesao_mensal_por_faixa[j][aux] = 100*len(ocorrencias)/(len(n_ocorrencias)+0.05)
    aux = aux + 1
    
#Linhas: Por faixa de atraso
#Colunas: Por mês

print(adesao_mensal_por_faixa)
