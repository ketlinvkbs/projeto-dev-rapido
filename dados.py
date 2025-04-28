import basedosdados as bd

bd.download(
    dataset_id="basedosdados.br_inpe_queimadas.microdados",
    billing_project_id="devrapido-458115",#id projeto google cloud
    savepath="queimadas"
)





print('Arrasou diva')