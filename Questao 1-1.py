# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Questão 1 - Base.txt', delimiter = "\t")
df['DT_VENCIMENTO'] = pd.to_datetime(df['DT_VENCIMENTO'])

mes = max(pd.DatetimeIndex(df['DT_VENCIMENTO']).month)


lista_emi = list(range(mes))

for i in lista_emi:
    total = df[(pd.DatetimeIndex(df['DT_VENCIMENTO']).month == i+1)]
    total_nao_pago = df[(pd.DatetimeIndex(df['DT_VENCIMENTO']).month == i+1) & (df['DS_ROLAGEM'] == 'FX1')]
    lista_emi[i] = 100*len(total_nao_pago)/len(total)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([1,2,3,4,5,6,7,8,9], lista_emi)  # Plot some data on the axes.
plt.xlabel('Meses')
plt.ylabel('Faturas emitidas p/mês s/pagamento da anterior(%)')