import pandas as pd
import matplotlib.pyplot as plt

# Carregar os DataFrames
df_clientes = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_customers_dataset.csv")
df_geolocalizacao = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_geolocation_dataset.csv")
df_itens_pedido = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_order_items_dataset.csv")
df_pagamentos_pedido = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_order_payments_dataset.csv")
df_avaliacoes_pedido = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_order_reviews_dataset.csv")
df_pedidos = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_orders_dataset.csv")
df_produtos = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_products_dataset.csv")
df_vendedores = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/olist_sellers_dataset.csv")
df_traducao_categoria = pd.read_csv("Brazilian E-Commerce Public Dataset by Olist/product_category_name_translation.csv")

# Lidando com valores ausentes (se necessário)
# Preenchendo valores nulos nas colunas de datas em df_pedidos com a mensagem "data indisponível"
df_pedidos['order_approved_at'] = df_pedidos['order_approved_at'].fillna('data indisponível')
df_pedidos['order_delivered_carrier_date'] = df_pedidos['order_delivered_carrier_date'].fillna('data indisponível')
df_pedidos['order_delivered_customer_date'] = df_pedidos['order_delivered_customer_date'].fillna('data indisponível')

# Preenchendo valores nulos nas colunas de comentário em df_avaliacoes_pedido com "sem comentários"
df_avaliacoes_pedido['review_comment_title'] = df_avaliacoes_pedido['review_comment_title'].fillna('sem comentários')
df_avaliacoes_pedido['review_comment_message'] = df_avaliacoes_pedido['review_comment_message'].fillna('sem comentários')

print('1. Análise de Performance de Vendas')
print('a. Volume de Vendas por Categoria: Identificar quais categorias de produtos têm o maior volume de vendas e em quais períodos (mensal, trimestral)')

# Passo 1: Agrupar os dados de vendas por categoria de produto e calcular o volume de vendas
merged_df = pd.merge(df_itens_pedido, df_produtos, on='product_id', how='inner')
volume_vendas_por_categoria = merged_df.groupby('product_category_name')['order_id'].count().reset_index()
volume_vendas_por_categoria.columns = ['product_category_name', 'volume_vendas']
volume_vendas_por_categoria = volume_vendas_por_categoria.sort_values(by='volume_vendas', ascending=False)

# Imprimir volume de vendas por categoria de produto
print("Volume de Vendas por Categoria de Produto:")
print(volume_vendas_por_categoria)
print("\n\n\n")

# Plotar gráfico de barras do volume de vendas por categoria de produto
plt.figure(figsize=(10, 6))
plt.bar(volume_vendas_por_categoria['product_category_name'], volume_vendas_por_categoria['volume_vendas'], color='skyblue')
plt.xlabel('Categoria de Produto')
plt.ylabel('Volume de Vendas')
plt.title('Volume de Vendas por Categoria de Produto')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


print('2. Análise de Logística')
print('a. Prazos de Entrega: Calcular o tempo médio de entrega e identificar os fatores que influenciam atrasos nas entregas.')
# Passo 1: Calcular o tempo de entrega para cada pedido.
# Converter as colunas de data para datetime
df_pedidos['order_purchase_timestamp'] = pd.to_datetime(df_pedidos['order_purchase_timestamp'])
df_pedidos['order_delivered_customer_date'] = pd.to_datetime(df_pedidos['order_delivered_customer_date'], errors='coerce')

# Calcular o tempo de entrega para cada pedido
df_pedidos['tempo_entrega'] = df_pedidos['order_delivered_customer_date'] - df_pedidos['order_purchase_timestamp']

# Passo 2: Calcular o tempo médio de entrega.
# Calcular o tempo médio de entrega, excluindo valores "data indisponível"
tempo_medio_entrega = df_pedidos[df_pedidos['order_delivered_customer_date'].notnull()]['tempo_entrega'].mean()
print("Tempo Médio de Entrega: ", tempo_medio_entrega)
print("\n\n\n")

# Calcular o tempo de trânsito de cada pedido
df_pedidos['order_approved_at'] = pd.to_datetime(df_pedidos['order_approved_at'], errors='coerce')
df_pedidos['order_delivered_carrier_date'] = pd.to_datetime(df_pedidos['order_delivered_carrier_date'], errors='coerce')
df_pedidos['order_delivered_customer_date'] = pd.to_datetime(df_pedidos['order_delivered_customer_date'], errors='coerce')

# Filtrar pedidos com todas as datas disponíveis
df_pedidos_validos = df_pedidos.dropna(subset=['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

# Calcular o tempo de trânsito
df_pedidos_validos['tempo_transito'] = df_pedidos_validos['order_delivered_customer_date'] - df_pedidos_validos['order_approved_at']

# Exibir estatísticas do tempo de trânsito
print("Estatísticas do Tempo de Trânsito:")
print(df_pedidos_validos['tempo_transito'].describe())
print("\n\n\n")
print("\n\n\n")


print('3. Análise de Satisfação do Cliente')
print('a. Avaliações de Produtos: Analisar a distribuição das avaliações dos produtos e identificar os produtos com as melhores e piores avaliações')
# Passo 1: Fundir os DataFrames df_avaliacoes_pedido e df_itens_pedido usando a coluna 'order_id' como chave de junção
avaliacoes_itens_fundidos = pd.merge(df_avaliacoes_pedido, df_itens_pedido, on='order_id', how='inner')

# Passo 2: Calcular a média das avaliações de cada produto
media_avaliacoes_produto = avaliacoes_itens_fundidos.groupby('product_id')['review_score'].mean().reset_index()

# Passo 3: Classificar os produtos com base na média das avaliações
produtos_classificados = media_avaliacoes_produto.sort_values(by='review_score', ascending=False)

# Imprimir estatísticas das avaliações dos produtos
print("Estatísticas das Avaliações dos Produtos:")
print(produtos_classificados['review_score'].describe())

# Imprimir os produtos com as melhores e piores avaliações
print("\nProdutos com as Melhores Avaliações:")
print(produtos_classificados.head(10))  # Os 10 produtos com as melhores avaliações

print("\nProdutos com as Piores Avaliações:")
print(produtos_classificados.tail(10))  # Os 10 produtos com as piores avaliações
# Plotar gráfico de barras das avaliações médias dos produtos
plt.figure(figsize=(10, 6))
plt.bar(produtos_classificados['product_id'].head(10), produtos_classificados['review_score'].head(10), color='lightgreen')
plt.xlabel('ID do Produto')
plt.ylabel('Avaliação Média')
plt.title('Top 10 Produtos com Melhores Avaliações')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

print("\nProdutos com as Piores Avaliações:")
print(produtos_classificados.tail(10))  # Os 10 produtos com as piores avaliações
# Plotar gráfico de barras das avaliações médias dos produtos
plt.figure(figsize=(10, 6))
plt.bar(produtos_classificados['product_id'].tail(10), produtos_classificados['review_score'].tail(10), color='lightcoral')
plt.xlabel('ID do Produto')
plt.ylabel('Avaliação Média')
plt.title('Top 10 Produtos com Piores Avaliações')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
print("\n\n\n")
print("\n\n\n")


print('4. Análise Financeira')
print('a. Análise de Lucratividade por Categoria: Calcular a lucratividade de diferentes categorias de produtos, levando em conta o custo dos produtos e o preço de venda.')
# Calcular o custo total de cada categoria de produto
merged_df = pd.merge(df_itens_pedido, df_produtos, on='product_id', how='inner')
custo_por_categoria = merged_df.groupby('product_category_name')['price'].sum().reset_index()
custo_por_categoria.columns = ['product_category_name', 'custo_total']

# Calcular o preço total de venda de cada categoria de produto
preco_por_categoria = merged_df.groupby('product_category_name')['freight_value'].sum().reset_index()
preco_por_categoria.columns = ['product_category_name', 'preco_total']

# Calcular a lucratividade de cada categoria de produto
lucratividade_por_categoria = pd.merge(custo_por_categoria, preco_por_categoria, on='product_category_name', how='inner')
lucratividade_por_categoria['lucro'] = lucratividade_por_categoria['preco_total'] - lucratividade_por_categoria['custo_total']

# Ordenar por lucratividade da maior para a menor
lucratividade_por_categoria = lucratividade_por_categoria.sort_values(by='lucro', ascending=False)

# Imprimir lucratividade por categoria de produto
print("\nLucratividade por Categoria de Produto (da maior para a menor):")
print(lucratividade_por_categoria)
print("\n\n\n")
print("\n\n\n")

# Plotar gráfico de barras da lucratividade por categoria de produto
plt.figure(figsize=(10, 6))
plt.bar(lucratividade_por_categoria['product_category_name'], lucratividade_por_categoria['lucro'], color='orange')
plt.xlabel('Categoria de Produto')
plt.ylabel('Lucro')
plt.title('Lucratividade por Categoria de Produto')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


print(' 5. Análise de Marketing')
print('a. Análise de Conversão de Vendas: Estudar a taxa de conversão de vendas com base em diferentes fontes de tráfego (orgânico, pago, social, etc.).')
# Passo 1: Filtrar transações concluídas
transacoes_concluidas = df_pedidos[df_pedidos['order_status'] == 'delivered']

# Passo 2: Adicionar a coluna 'payment_type' ao DataFrame `transacoes_concluidas`
transacoes_concluidas = pd.merge(transacoes_concluidas, df_pagamentos_pedido[['order_id', 'payment_type']], on='order_id', how='inner')

# Passo 3: Agrupar as transações concluídas por tipo de pagamento
grupo_transacoes_concluidas = transacoes_concluidas.groupby('payment_type')

# Passo 4: Calcular o número de transações concluídas para cada tipo de pagamento
total_transacoes_concluidas = grupo_transacoes_concluidas.size().reset_index(name='transacoes_concluidas')

# Passo 5: Calcular o número total de transações concluídas
total_transacoes = total_transacoes_concluidas['transacoes_concluidas'].sum()

# Passo 6: Calcular a taxa de conversão de vendas para cada tipo de pagamento
total_transacoes_concluidas['taxa_conversao'] = (total_transacoes_concluidas['transacoes_concluidas'] / total_transacoes) * 100

# Exibir os resultados
print("\nTaxa de Conversão de Vendas por Tipo de Pagamento:")
print(total_transacoes_concluidas[['payment_type', 'taxa_conversao']])

## Plotar gráfico de pizza da taxa de conversão de vendas por tipo de pagamento
plt.figure(figsize=(8, 8))
plt.pie(total_transacoes_concluidas['taxa_conversao'], labels=total_transacoes_concluidas['payment_type'], autopct='%1.1f%%')
plt.title('Taxa de Conversão de Vendas por Tipo de Pagamento')
plt.axis('equal')
plt.tight_layout()
plt.show()
