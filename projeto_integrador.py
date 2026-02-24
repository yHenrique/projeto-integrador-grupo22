import pandas as pd

df = pd.read_csv('students_social_media_addiction.csv')

df_preparacao = df.rename(columns={'Student_ID':'ID',
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
df_preparacao['Gênero'] = df_preparacao['Gênero'].map(traduzir_genero)

# Traduzindo a coluna Nível_Acadêmico
traduzir_nivel_academico = {'Undergraduate':'Graduação',
                            'Graduate':'Pós-Graduação',
                            'High School':'Ensino Médio'}
df_preparacao['Nível_Acadêmico'] = df_preparacao['Nível_Acadêmico'].map(traduzir_nivel_academico)

# Traduzindo a coluna País
# Utilizar biblioteca

# Traduzindo a coluna Afeta_Desempenho_Acadêmico
traduzir_afeta_desempenho_academico = {'Yes':'Sim',
                                       'No':'Não'}
df_preparacao['Afeta_Desempenho_Acadêmico'] = df_preparacao['Afeta_Desempenho_Acadêmico'].map(traduzir_afeta_desempenho_academico)

# Traduzindo a coluna Status_Relação
traduzir_status_relacao = {'In Relationship':'Em Relacionamento',
                           'Single':'Solteiro',
                           'Complicated':'Complicado'}
df_preparacao['Status_Relação'] = df_preparacao['Status_Relação'].map(traduzir_status_relacao)



# print(df_preparacao['Status_Relação'].unique())
# df_preparacao.info()
# print(df_preparacao.head())