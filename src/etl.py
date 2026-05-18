import pandas as pd
from babel import Locale
import country_converter as coco

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