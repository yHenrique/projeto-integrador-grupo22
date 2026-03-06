import pandas as pd
# import country_converter as coco
import deep_translator as dt

# Importando a base de dados
df = pd.read_csv('data/base_original.csv')

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
# print(df_tratado['País'].unique())
df_tratado['País'] = df_tratado['País'].replace({'USA':'United States', 'UK':'United Kingdom', 'UAE':'United Arab Emirates'})
# for pais in df_tratado['País']:
#     pais_traduzido = dt.GoogleTranslator(source='en', target='pt').translate(pais)
#     df_tratado['País'][pais] = pais_traduzido

# Traduzindo a coluna Afeta_Desempenho_Acadêmico
traduzir_afeta_desempenho_academico = {'Yes':'Sim',
                                       'No':'Não'}
df_tratado['Afeta_Desempenho_Acadêmico'] = df_tratado['Afeta_Desempenho_Acadêmico'].map(traduzir_afeta_desempenho_academico)

# Traduzindo a coluna Status_Relação
traduzir_status_relacao = {'In Relationship':'Em Relacionamento',
                           'Single':'Solteiro',
                           'Complicated':'Complicado'}
df_tratado['Status_Relação'] = df_tratado['Status_Relação'].map(traduzir_status_relacao)

# Criando a base tratada
df_tratado.to_csv('data/base_tratada.csv', index=False)

# Exibindo informações
# print(df_tratado['Status_Relação'].unique())
# df_tratado.info()
# print(df_tratado.head())