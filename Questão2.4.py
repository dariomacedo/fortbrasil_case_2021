#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate #pesquisar aqui
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample



# In[2]:


#ID_CONTA DT_ACORDO NU_DIAS_ATRASO VALOR_CRELIQ DIVIDA_ATUAL RESPOSTA
df1 = pd.read_csv('Questão 2 - Base 1.txt', delimiter = "\t") 

#ID_CONTA DT_ACORDO QTD_PARCELAMENTO_3M QTD_PARCELAMENTO_6M QTD_PARCELAMENTO_12M
df2 = pd.read_csv('Questão 2 - Base 2.txt', delimiter = "\t")

#ID_CONTA DT_ACORDO LIMITE
df3 = pd.read_csv('Questão 2 - Base 3.txt', delimiter = "\t")

#ID_CONTA DT_ACORDO QTD_EXTRATOS QTD_FX0_GERAL QTD_FX1_GERAL QTD_FX2_GERAL QTD_FX0_3M
#TD_FX0_6M QTD_FX1_3M QTD_FX1_6M TD_FX2_3M TD_FX2_6M
df4 = pd.read_csv('Questão 2 - Base 4.txt', delimiter = "\t")

#ID_CONTA DT_ACORDO TD_CPC_10D QTD_CPC_1M QTD_CPC_3M QTD_CPC_6M QTD_CP_10D QTD_CP_1M 
#QTD_CP_3M QTD_CP_6M QTD_ACIONAMENTO_10D QTD_ACIONAMENTO_1M QTD_ACIONAMENTO_3M QTD_ACIONAMENTO_6M
df5 = pd.read_csv('Questão 2 - Base 5.txt', delimiter = "\t")


# In[3]:


#Realizar a junção de dataframes através da função pd.merge do pandas
#Juntando df1 e df2, exclui DT_ACORDO pq não precisa dessa variável no df2, pois já tenho no df1
df12 = pd.merge(df1,df2, on= ['ID_CONTA','DT_ACORDO'],how='left')

#Juntando df3 e df4
df34 = pd.merge(df3,df4,on= ['ID_CONTA','DT_ACORDO'],how='left') #MUDAR AQUI

#Juntando df12 e df34
df1234 = pd.merge(df12,df34,on= ['ID_CONTA','DT_ACORDO'],how='left')
#df1234 = pd.merge(df34,df12,on= ['ID_CONTA','DT_ACORDO'],how='left')

#Juntando df1234 e df5
df = pd.merge(df1234,df5,on= ['ID_CONTA','DT_ACORDO'],how='left') #MUDAR AQUI 
#df = pd.merge(df5,df1234,on= ['ID_CONTA','DT_ACORDO'],how='left') #MUDAR AQUI TBM
#df.info()


# In[4]:


(df.isnull().sum() / df.shape[0] * 100).sort_values(ascending=False)
#df = df.drop('DT_ACORDO_y',axis=1)


# In[5]:


def preencher_proporcional(col):
    """ Preenche valores ausentes na mesma proporção dos valores presentes

    Recebe uma coluna e retorna a coluna com os valores ausentes preenchidos
    na proporção dos valores previamente existentes."""
    
    # Gerando o dicionário com valores únicos e sua porcentagens
    percentages = col.value_counts(normalize=True).to_dict()

    # Tranformando as chaves e valores do dicionário em listas      
    percent = [percentages[key] for key in percentages]
    labels = [key for key in percentages]

    # Utilizando as listas para prencher os valores nulos na proporção correta 
    s = pd.Series(np.random.choice(labels, p=percent, size=col.isnull().sum()))
    col = col.fillna(s)
    
    # Verificando se todos os valores ausentes foram preenchidos e
    # preenchendo os que não tiverem sido
    if len(col.isnull()) > 0:
        col.fillna(value=max(percentages, key=percentages.get), inplace=True, axis=0)
        
    return col


# In[6]:


for col in df.iloc[:,1:].columns.tolist():
    if df[col].dtypes == 'O':
        df[col] = preencher_proporcional(df[col])
    else:
        df[col].fillna(value=df[col].median(), inplace=True, axis=0)


# In[7]:


#df.isnull().sum()


# In[8]:


df = df.dropna(axis=1)


# In[9]:


df['DT_ACORDO'] = pd.to_datetime(df['DT_ACORDO'])


# In[10]:


fig, ax = plt.subplots(figsize=(10,8))
sns.countplot(df['RESPOSTA'])
plt.show()

df['RESPOSTA'].value_counts()


# In[11]:


# Dividindo e padronizando o dataset original
df_teste = df
df_teste = df_teste.drop('DT_ACORDO',axis=1)

X = df_teste.drop('RESPOSTA', axis=1)
Y = df_teste['RESPOSTA']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_unb = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#Criando o dataset balanceado
maioria = df_teste[df_teste['RESPOSTA']==0]
minoria = df_teste[df_teste['RESPOSTA']==1]

minoria_balanceada = resample(minoria,replace=True,n_samples=70402)
df_balanceado = pd.concat([maioria,minoria_balanceada])

#Dividindo e padronizando o dataset balanceado
X_bl = df_balanceado.drop('RESPOSTA',axis=1)
Y_bl = df_balanceado['RESPOSTA']

X_train_bl, X_test_bl, Y_train_bl, Y_test_bl = train_test_split(X_bl,Y_bl)

scaler_bl = StandardScaler()
scaler_bl.fit(X_bl)
X_train_bl = scaler_bl.transform(X_train_bl)
X_test_bl = scaler_bl.transform(X_test_bl)

# Verificando o balanceamento
print(df_balanceado['RESPOSTA'].value_counts(), '\n')

fig, ax = plt.subplots(figsize=(8,6))
sns.countplot(df_balanceado['RESPOSTA'])
ax.set_title('Dados após o balnaceamento')
plt.show()


# In[12]:


# Criando os modelos utilizando validação cruzada
#cross_validation utilizada para evitar overfitting, quando o modelo perde generalização para outros conjunto de dados
logreg_balanceado  = cross_validate(LogisticRegression(solver='liblinear'), X_train_bl, Y_train_bl, cv=5, scoring=['accuracy', 'precision', 'recall', 'roc_auc'])
logreg = cross_validate(LogisticRegression(solver='liblinear'), X_train, Y_train, cv=5, scoring=['accuracy', 'precision', 'recall', 'roc_auc'])

# Gerando um DataFrame com os resultados 
summary = pd.DataFrame({
            'labels': ['accuracy', 'precision', 'recall', 'roc_auc'],
            'logreg_balanceado': [logreg_balanceado['test_accuracy'].mean(), logreg_balanceado['test_precision'].mean(), logreg_balanceado['test_recall'].mean(), logreg_balanceado['test_roc_auc'].mean()],
            'logreg': [logreg['test_accuracy'].mean(), logreg['test_precision'].mean(), logreg['test_recall'].mean(), logreg['test_roc_auc'].mean()]           
}).set_index('labels')
summary.index.name=None
summary = summary.transpose()    
summary.style.applymap(lambda x: 'background-color: lightgreen' if x >= 0.75 else '')

print(summary)


# In[ ]:




