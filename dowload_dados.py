import basedosdados as bd

query = """
SELECT * FROM `basedosdados.br_inpe_queimadas.microdados`
"""
df=bd.read_sql(query, billing_project_id="id do projeteo no google cloud")

df.to_csv('queimadas.csv', index=False)



print('Arrasou diva')
