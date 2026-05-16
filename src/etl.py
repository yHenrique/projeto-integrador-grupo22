import pandas as pd
# import country_converter as coco
import deep_translator as dt
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

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
# for pais in df_tratado['País']:
#     pais_traduzido = dt.GoogleTranslator(source='en', target='pt').translate(pais)
#     df_tratado['País'] = df_tratado['País'].replace({pais:pais_traduzido})

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
st.dataframe(df_tratado)

st.header('Identificando a tendência entre maior tempo de uso diário de redes sociais por faixa etária:')
analise1_col1, analise1_col2 = st.columns([2, 4], border=True)

with analise1_col1:
    st.subheader('Quantidade de estudantes entrevistados por idade')
    qtd_por_idade = df_tratado['Idade'].value_counts().reset_index()
    qtd_por_idade.columns = ['Idade', 'Quantidade']
    fig = px.pie(qtd_por_idade, values='Quantidade', names='Idade')
    st.plotly_chart(fig)

with analise1_col2:
    st.subheader('Média de uso diário por idade')
    media_uso_diario_por_idade = df_tratado.groupby(['Idade', 'Gênero'])['Média_Uso_Diário'].mean().reset_index()
    st.bar_chart(media_uso_diario_por_idade, x='Idade', y='Média_Uso_Diário', color='Gênero', y_label='Média de Uso Diário', stack=False)
    st.write('Conclusão: Adolescentes de 18 anos tendem a passar mais tempo nas redes sociais, em principal, as garotas, ' \
    'enquanto que, no geral, aqueles que têm 23 anos são os que menos utilizam.')

st.header('Analisando a relação entre o tempo de uso nas redes sociais e o desempenho escolar dos estudantes:')
analise2_col1, analise2_col2, analise2_col3 = st.columns([1, 1, 1])

with analise2_col1:
    media_uso_diario_afetar_desempenho = df_tratado.groupby(['Afeta_Desempenho_Acadêmico', 'Nível_Acadêmico'])['Média_Uso_Diário'].mean().reset_index()
    st.bar_chart(media_uso_diario_afetar_desempenho, x='Afeta_Desempenho_Acadêmico', y='Média_Uso_Diário', color='Nível_Acadêmico', x_label='Afeta o Desempenho Acadêmico', y_label='Média de Uso Diário', stack=False)
    st.write('Conclusão: Segundo os adolescentes entrevistados, usar as redes sociais até 4 horas por dia não afetam seu desempenho escolar.')

st.header('Identificando possíveis indícios do uso excessivo que possam estar relacionados a impactos negativos na rotina dos estudantes:')

st.header('Identificando os países que apresentam maior média de uso diário:')
col1, col2 = st.columns([1, 4], border=True)

with col1:
    st.text('Quantidade de estudantes entrevistados por país')
    contador_pais = df_tratado['País'].value_counts()
    st.dataframe(contador_pais.reset_index(name='Quantidade'))

with col2:
    df_pais_filtrado = df_tratado[df_tratado['País'].map(contador_pais) > 1]
    media_uso_diario_pais = df_pais_filtrado.groupby('País')['Média_Uso_Diário'].mean()
    st.bar_chart(media_uso_diario_pais, x_label='País', y_label='Média de Uso Diário (Horas)', height=400)
    st.write('Conclusão: Os Estados Unidos e os Emirados Árabes Unidos são os 2 países com a maior média de uso entre os perfis analisados, com uma média aproximada de 7 horas por dia,' \
    ' enquanto que a Suíça é o país com a menor média diária.')
    st.write('Obs: Utilizando apenas os dados de estudantes cujo país aparece mais de uma vez entre os entrevistados.')

st.header('Verificando a possibilidade de uma tendência de aumento no uso de redes sociais dados determinados perfis de estudantes:')

# st.write('Plataforma mais utilizada')
# soma_plataformas_mais_utilizadas = df_tratado['Plataforma_Mais_Utilizada'].sum()
# st.bar_chart(soma_plataformas_mais_utilizadas)