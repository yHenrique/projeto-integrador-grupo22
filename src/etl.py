import pandas as pd
from babel import Locale
import country_converter as coco
import streamlit as st
import plotly.express as px
import numpy as np

# Importando a base de dados
df = pd.read_csv('../data/base_original.csv')

# Traduzindo os nomes das colunas
df_tratado = df.rename(columns={'Student_ID':'ID',
                                'Age':'Idade',
                                'Gender':'Gênero',
                                'Academic_Level':'Nível_Acadêmico',
                                'Country':'País',
                                'Avg_Daily_Usage_Hours':'Média_Uso_Diário',
                                'Most_Used_Platform':'Plataforma_Mais_Utilizada',
                                'Affects_Academic_Performance':'Afeta_Desempenho_Acadêmico',
                                'Sleep_Hours_Per_Night':'Horas_Sono',
                                'Mental_Health_Score':'Pontuação_Saúde_Mental',
                                'Relationship_Status':'Status_Relação',
                                'Conflicts_Over_Social_Media':'Conflitos_Sobre_Redes_Sociais',
                                'Addicted_Score':'Nível_Vício'})

# Traduzindo a coluna Gênero
traduzir_genero = {'Female':'Feminino',
                   'Male':'Masculino'}
df_tratado['Gênero'] = df_tratado['Gênero'].map(traduzir_genero)

# Traduzindo a coluna Nível_Acadêmico
traduzir_nivel_academico = {'Undergraduate':'Graduação',
                            'Graduate':'Pós-Graduação',
                            'High School':'Ensino Médio'}
df_tratado['Nível_Acadêmico'] = df_tratado['Nível_Acadêmico'].map(traduzir_nivel_academico)

# Traduzindo a coluna País
df_tratado['País'] = df_tratado['País'].replace({'USA':'United States', 'UK':'United Kingdom', 'UAE':'United Arab Emirates'})
cc = coco.CountryConverter()
df_tratado['País'] = cc.convert(names=df_tratado['País'], to='ISO2')

locale = Locale('pt', 'BR')
def traduzir_codigo(codigo):
    if pd.isna(codigo):
        return codigo
    return locale.territories.get(str(codigo).upper(), codigo)
df_tratado['País'] = df_tratado['País'].apply(traduzir_codigo)

# Traduzindo a coluna Afeta_Desempenho_Acadêmico
traduzir_afeta_desempenho_academico = {'Yes':'Sim',
                                       'No':'Não'}
df_tratado['Afeta_Desempenho_Acadêmico'] = df_tratado['Afeta_Desempenho_Acadêmico'].map(traduzir_afeta_desempenho_academico)

# Traduzindo a coluna Status_Relação
traduzir_status_relacao = {'In Relationship':'Em Relacionamento',
                           'Single':'Solteiro',
                           'Complicated':'Complicado'}
df_tratado['Status_Relação'] = df_tratado['Status_Relação'].map(traduzir_status_relacao)

df_tratado.drop(columns=['ID', 'Status_Relação', 'Conflitos_Sobre_Redes_Sociais'], inplace=True)

# Criando a base tratada
df_tratado.to_csv('../data/base_tratada.csv', index=False)

# Exibindo informações
# print(df_tratado['Status_Relação'].unique())
# df_tratado.info()
# print(df_tratado.head())

st.set_page_config(layout='wide')

st.title('Análise do dataset referente ao vício dos estudantes em redes sociais', text_alignment='center')
st.space(size='small')
st.dataframe(df_tratado)
st.space(size='medium')

st.header('Identificando a tendência entre maior tempo de uso diário de redes sociais por faixa etária:')
analise1_col1, analise1_col2 = st.columns([2, 4], border=True)

with analise1_col1:
    st.subheader('Quantidade de entrevistados por idade', text_alignment='center')
    qtd_por_idade = df_tratado['Idade'].value_counts().reset_index()
    qtd_por_idade.columns = ['Idade', 'Quantidade']
    fig = px.pie(qtd_por_idade, values='Quantidade', names='Idade')
    st.plotly_chart(fig)

with analise1_col2:
    st.subheader('Média de uso diário por idade', text_alignment='center')
    st.space(size='large')
    media_uso_diario_por_idade = df_tratado.groupby(['Idade', 'Gênero'])['Média_Uso_Diário'].mean().reset_index()
    st.bar_chart(media_uso_diario_por_idade, x='Idade', y='Média_Uso_Diário', color='Gênero', y_label='Média de Uso Diário', stack=False)
    st.write('Conclusão: Adolescentes de 18 anos tendem a passar mais tempo nas redes sociais, em principal, do gênero feminino, ' \
    'enquanto que, no geral, aqueles que têm 23 anos são os que menos utilizam.')

st.space('medium')
st.header('Analisando a relação entre o tempo de uso nas redes sociais e o desempenho escolar dos estudantes:')

analise2_col1, analise2_col2, analise2_col3 = st.columns([1, 2, 1])

with analise2_col2.container(border=True):
    st.subheader('Relação entre uso e desempenho', text_alignment='center')
    st.space(size='medium')
    media_uso_diario_afetar_desempenho = df_tratado.groupby(['Afeta_Desempenho_Acadêmico', 'Nível_Acadêmico'])['Média_Uso_Diário'].mean().reset_index()
    st.bar_chart(media_uso_diario_afetar_desempenho, x='Afeta_Desempenho_Acadêmico', y='Média_Uso_Diário', color='Nível_Acadêmico', x_label='Afeta o Desempenho Acadêmico', y_label='Média de Uso Diário', stack=False)
    st.write('Conclusão: Segundo os adolescentes entrevistados, usar as redes sociais até 4 horas por dia não afetam seu desempenho escolar.')

st.space('medium')
st.header('Identificando possíveis indícios do uso excessivo que possam estar relacionados a impactos negativos na rotina dos estudantes:')

analise3_col1, analise3_col2, analise3_col3 = st.columns([1, 1, 1], border=True)

df_tratado['Classificação_Sono'] = np.where(df_tratado['Horas_Sono'] >= 7, 'Mais de 7 horas', 'Menos de 7 horas')

with analise3_col1:
    st.subheader('Classificação do sono', text_alignment='center')
    fig = px.pie(df_tratado, names='Classificação_Sono', color='Classificação_Sono')
    st.plotly_chart(fig)
    st.write('Conclusão: Apenas metade dos entrevistados dormem a quantidade mínima de horas recomendadas por dia.', )

df_tratado['Classificação_Saúde_Mental'] = np.where(df_tratado['Pontuação_Saúde_Mental'] >= 6, 'Boa', 'Ruim')

with analise3_col2:
    st.subheader('Classificação da saúde mental', text_alignment='center')
    fig = px.pie(df_tratado, names='Classificação_Saúde_Mental', color='Classificação_Saúde_Mental')
    st.plotly_chart(fig)
    st.write('''Conclusão: Considerando a pontuação da saúde mental dos estudantes acima de 6 como 'bom' e abaixo de 6 como 'ruim', é possível inferir que quase 30% dos 
             entrevistados vivem com baixa saúde mental.''')
    
df_tratado['Classificação_Vício'] = np.where(df_tratado['Nível_Vício'] >= 6, 'Alto', 'Baixo')

with analise3_col3:
    st.subheader('Classificação do vício', text_alignment='center')
    fig = px.pie(df_tratado, names='Classificação_Vício', color='Classificação_Vício')
    st.plotly_chart(fig)
    st.write('Conclusão: Grande parte dos entrevistados afirmam estar viciados nas redes sociais.')

st.space('medium')
st.header('Identificando os países que apresentam a maior média de uso diário:')
analise4_col1, analise4_col2 = st.columns([1, 4], border=True)

with analise4_col1:
    st.subheader('Quantidade de entrevistados por país', text_alignment='center')
    st.space(size='small')
    contador_pais = df_tratado['País'].value_counts()
    st.dataframe(contador_pais.reset_index(name='Quantidade'), height=500)

with analise4_col2:
    st.subheader('Média de uso diário por país', text_alignment='center')
    st.space(size='medium')
    df_pais_filtrado = df_tratado[df_tratado['País'].map(contador_pais) > 1]
    media_uso_diario_pais = df_pais_filtrado.groupby('País')['Média_Uso_Diário'].mean()
    st.bar_chart(media_uso_diario_pais, x_label='País', y_label='Média de Uso Diário (Horas)', height=400, color='#008EE3', sort='-Média_Uso_Diário')
    st.write('Conclusão: Os Estados Unidos e os Emirados Árabes Unidos são os 2 países com a maior média de uso entre os perfis analisados, com uma média aproximada de 7 horas por dia,' \
    ' enquanto que a Suíça é o país com a menor média diária.')
    st.write('Obs: Utilizando apenas os dados de estudantes cujo país aparece mais de uma vez entre os entrevistados.')

st.space('medium')
st.header('Verificando a possibilidade de uma tendência de aumento no uso de redes sociais dados determinados perfis de estudantes:')

# st.write('Plataforma mais utilizada')
# soma_plataformas_mais_utilizadas = df_tratado['Plataforma_Mais_Utilizada'].sum()
# st.bar_chart(soma_plataformas_mais_utilizadas)