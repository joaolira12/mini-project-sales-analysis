import pandas as pd
import numpy as np

df_vendas = pd.read_csv("mini_projeto_analise_de_vendas/vendas.csv")

#primeiras linhas
print(df_vendas.head())
print()

#últimas linhas
print(df_vendas.tail())
print()

print(df_vendas.info())
print()

print(df_vendas.describe())
print()

#Criar coluna de receita total por produto

df_vendas["Receita_Total_Produto"] = df_vendas["Quantidade"] * df_vendas["Preco_Unitario"]
print(df_vendas.head())
print()

#Selecionar somente as colunass 'Produto' e 'Receita Total Produtos'
print(df_vendas[["Produto", "Receita_Total_Produto"]].head())
print()

#Produtos em que a quantidade é maior que N
n = 20
print(df_vendas[df_vendas["Quantidade"] > 20].head())
print()

#Localizar somente os produtos com Monitor na coluna produto
print(df_vendas.loc[df_vendas["Produto"] == "Monitor",].head())
print()

#usando iloc para localizar por meio de índice numérico
print(df_vendas.iloc[0:3, 1:4])
print()

#Faturamento Total:
print(df_vendas["Receita_Total_Produto"].sum())
print()

#Preço médio unitario dos produtos:
print(df_vendas["Preco_Unitario"].mean())
print()


#Quantidade mínima e máxima de produtos vendidos:
print(df_vendas["Quantidade"].min())
print(df_vendas["Quantidade"].max())
print()

#Simulando valores ausentes no df
df_vendas_copia_nan = df_vendas.copy()

df_vendas_copia_nan.loc[df_vendas_copia_nan.sample(frac=0.05).index, "Preco_Unitario"]  = np.nan #sample seleciona % das linhas do df
df_vendas_copia_nan.loc[df_vendas_copia_nan.sample(frac=0.03).index, "Quantidade"] = np.nan

#verificando se existe valores ausentes
df_vendas_copia_nan.info()
print(df_vendas_copia_nan.isna())
print(df_vendas_copia_nan.isna().sum())

#Preencher com a média os valores nulos da coluna Quantidade
df_vendas_preenchido = df_vendas_copia_nan.copy()
media_quantidade = df_vendas_preenchido["Quantidade"].mean()
print(media_quantidade)
df_vendas_preenchido.fillna({"Quantidade": media_quantidade}, inplace=True)
df_vendas_preenchido.info()

#Remover valores ausentes encontrados em Preço Unitario
df_vendas_limpo = df_vendas_preenchido.dropna(subset=["Preco_Unitario"])
df_vendas_limpo.info()

#Agrupando por produto e calculando quantidade e receita total por produto
df_vendas_por_produto = df_vendas_limpo.groupby("Produto").agg( Quantidade_Total=("Quantidade", "sum"), Receita_Total=("Receita_Total_Produto", "sum")).reset_index()

print(df_vendas_por_produto)
print()

#ordenando por quantidade total
print(df_vendas_por_produto.sort_values(by="Quantidade_Total", ascending=False))
print()

#ordenando por receita total
print(df_vendas_por_produto.sort_values(by="Receita_Total", ascending=False))
print()

#convertendo as datas para o tipo adequado
df_vendas_limpo["Data_Venda"] = pd.to_datetime(df_vendas_limpo["Data_Venda"])

#analisando vendas por mês
df_vendas_limpo["Mes_Venda"] = df_vendas_limpo["Data_Venda"].dt.month
print(df_vendas_limpo.head())
print()

#Agrupando por mês e calculando receita total a cada mês
df_vendas_por_mes = df_vendas_limpo.groupby("Mes_Venda")["Receita_Total_Produto"].sum().reset_index()
print(f"{df_vendas_por_mes}")

#adicionando outro df (produtos)
df_produtos = pd.read_csv("mini_projeto_analise_de_vendas/produtos.csv")
print(df_produtos.head())
print()

#Fazendo o merge do df vendas e do df produto
df_merge = pd.merge(df_vendas_limpo, df_produtos, on="Produto", how="left")
print(f"{df_merge}\n")


#analisando receita total por categória
df_vendas_por_categoria = df_merge.groupby("Categoria")["Receita_Total_Produto"].sum().reset_index()
print(f"{df_vendas_por_categoria}\n")

#filtrando por coluna (Produto, Quantidade e Receita Total)
df_colunas_filtradas = df_merge.filter(items=["Produto", "Quantidade", "Receita_Total_Produto"])
print(f"{df_colunas_filtradas}\n")

#Filtrando Somente o produto teclado com quantidade maior que 10
df_query = df_merge.query("Produto == 'Teclado' and Quantidade > 10")
print(df_query)
