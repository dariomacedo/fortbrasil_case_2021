# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

df = pd.read_csv('Questão 1 - Base.txt', delimiter = "\t")
df['DT_VENCIMENTO'] = pd.to_datetime(df['DT_VENCIMENTO'])

#dataframe com SETEMBRO
df2 = df[(pd.DatetimeIndex(df['DT_VENCIMENTO']).month == 9)] 
#Não tem essa coluna no exemplo fornecido, dado não necessário
df2 = df2.drop('VL_FATURA', axis=1) 

#Os últimos 6 meses, sem contar setembro
teste = df[(pd.DatetimeIndex(df['DT_VENCIMENTO']).month > 2) & (pd.DatetimeIndex(df['DT_VENCIMENTO']).month < 9)]

fat_count = teste.groupby(['ID_CONTA']).size().rename('QTD_FATURAS_ULT_6M')
df2 = df2.join(fat_count, on=['ID_CONTA'],how='left')

#Retirando os clientes que não possuem fatura emitida nos últimos 6 meses
df2 = df2.fillna(value=0)

#Obtendo valor da fatuar média que é um dado necessário ao novo conjunto de dados
fat_media = teste.groupby(['ID_CONTA'])['VL_FATURA'].mean().reset_index().rename({'VL_FATURA': 'VL_MEDIO_FATURA'},axis=1)

#Adicionando ao conjunto de dados
df2 = pd.merge(df2,fat_media, on='ID_CONTA', how ='left')

#Processo para obter a quantidade de clientes que não pagaram a fatura
a = teste.groupby(['ID_CONTA', 'DS_ROLAGEM']).size().reset_index().rename({0: 'QTD_FATURAS_ULT_6M_FX1'},axis=1)
a_new = a.loc[a['DS_ROLAGEM']=='FX1'] 
a_new = a_new.drop('DS_ROLAGEM', axis=1)

#Realizando a última adição no conjunto de dados
df2 = pd.merge(df2,a_new, on='ID_CONTA', how ='left')

#Preenchendo com 0 onde tenho NaN
df2 = df2.fillna(value=0)

df2.to_csv('base_gerada_13.txt',sep="\t",index=False)
#for variavel in:
#    JAN_total = data[(pd.DatetimeIndex(data['DT_VENCIMENTO']).month == 1)]
#    JAN_nao_pago = data[(pd.DatetimeIndex(data['DT_VENCIMENTO']).month == 1) & (data['DS_ROLAGEM'] == 'FX1')]








#ESTUDANDO
# df['new'] = df['W'] + df['Y']
# df.drop('new',axis=1,inplace=True)
# df.loc['A'] -> Irá me retornar as linhas
#df.iloc['C'] ou ['2']
#df.loc['B','Y'] B é inha e Y coluna
# booldf = df>0 / df[booldf / df[df>0]
# df['W']>0

#teste_jan = data[data['DT_VENCIMENTO']]