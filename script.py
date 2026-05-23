import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt

# Carga inicial de los datasets base de clientes y pedidos
# no cargamos reviews dado que solo se usa una vez en el 4
dfCustomersBase = pd.read_csv('./streamlit_resources/customers_dataset.csv')
dfOrdersBase = pd.read_csv('./streamlit_resources/orders_dataset.csv')

#########################################################################################
# Une clientes y pedidos filtrando por rango de fechas para contar clientes únicos por ciudad y estado
def loadData(fechaMin, fechaMax):    
    dfMergeOrdersCustomers = pd.merge(dfCustomersBase,dfOrdersBase, on='customer_id')
    dfMergeOrdersCustomers['order_purchase_timestamp'] = pd.to_datetime(dfMergeOrdersCustomers.order_purchase_timestamp, yearfirst=True)

    df_clientes_agrupados = dfMergeOrdersCustomers[['customer_state','customer_id','customer_city','customer_unique_id']].where((dfMergeOrdersCustomers['order_purchase_timestamp'] > pd.to_datetime(fechaMin, yearfirst=True)) &( dfMergeOrdersCustomers['order_purchase_timestamp'] < pd.to_datetime(fechaMax, yearfirst=True))).groupby(['customer_city','customer_state']).nunique().sort_values(['customer_unique_id'], ascending=False).reset_index()

    return df_clientes_agrupados

#########################################################################################
# Calcula porcentajes de pedidos y el ratio de pedidos por cliente único para cada ciudad
def loadData2(df):
    dfOrdersCustomersCity = df.copy()
    dfOrdersCustomersCity = dfOrdersCustomersCity.rename(columns={'customer_id':'orders_count','customer_unique_id':'customer_count'})
    dfOrdersCustomersCity['orders_percent'] = 0.0
    dfOrdersCustomersCity['orders_percent'] = round(dfOrdersCustomersCity['orders_count'] / dfOrdersCustomersCity['orders_count'].sum() * 100, 3)
    dfOrdersCustomersCity['proporcion_pedidos_cliente'] = round(dfOrdersCustomersCity['orders_count'] / dfOrdersCustomersCity['customer_count'],2)
    dfOrdersCustomersCity.reset_index()

    return dfOrdersCustomersCity[['customer_state', 'customer_city','orders_count','customer_count','orders_percent', 'proporcion_pedidos_cliente']]

#########################################################################################
# Obtiene la cantidad y el porcentaje de pedidos entregados tarde con respecto al total de cada ciudad
def loadData3A(dfEjercicio2):
    dfRetrasos = pd.merge(dfCustomersBase,dfOrdersBase, on='customer_id')
    
    dfRetrasos['pedidos_tarde'] = (
        pd.to_datetime(dfRetrasos['order_delivered_customer_date']) > 
        pd.to_datetime(dfRetrasos['order_estimated_delivery_date'])
    )

    dfTotalRetrasosCiudad = dfRetrasos.groupby(['customer_state', 'customer_city'])['pedidos_tarde'].sum().reset_index().sort_values('pedidos_tarde', ascending=False)

    dfTotalRetrasosCiudadCopia = dfTotalRetrasosCiudad.copy()

    dfTotalRetrasosCiudadCopia = pd.merge(dfTotalRetrasosCiudadCopia, dfEjercicio2[['customer_state', 'customer_city', 'orders_count']], on=['customer_state', 'customer_city'], how='left')

    dfTotalRetrasosCiudadCopia['porcentaje_retrasados'] = (dfTotalRetrasosCiudadCopia['pedidos_tarde'] / dfTotalRetrasosCiudadCopia['orders_count']) * 100
    dfTotalRetrasosCiudadCopia['city_state'] = dfTotalRetrasosCiudadCopia['customer_city'] + " (" + dfTotalRetrasosCiudadCopia['customer_state'] + ")"

    return dfTotalRetrasosCiudadCopia.sort_values(by=['pedidos_tarde','porcentaje_retrasados'], ascending=[False, False])

######
# Calcula el promedio de días de retraso que tienen los pedidos que llegaron tarde en cada ciudad
def loadData3B():
    dfTodosPedidosTiempo = pd.merge(dfCustomersBase, dfOrdersBase, on='customer_id')
    
    dfTodosPedidosTiempo['tiempo_retraso'] = ((
        pd.to_datetime(dfTodosPedidosTiempo['order_delivered_customer_date']) - 
        pd.to_datetime(dfTodosPedidosTiempo['order_estimated_delivery_date'])
    ).dt.total_seconds() / (24 * 3600)).round()

    dfTodosPedidosTiempoTarde = dfTodosPedidosTiempo[dfTodosPedidosTiempo['tiempo_retraso'] > 0]
    dfTodosPedidosTiempoTardeCity = dfTodosPedidosTiempoTarde.groupby(['customer_state', 'customer_city'])['tiempo_retraso'].mean().reset_index().sort_values('tiempo_retraso', ascending=False).rename(columns={'tiempo_retraso': 'tiempo_retraso_medio'})
    dfTodosPedidosTiempoTardeCity['city_state'] = dfTodosPedidosTiempoTardeCity['customer_city'] + " (" + dfTodosPedidosTiempoTardeCity['customer_state'] + ")"

    return dfTodosPedidosTiempoTardeCity

############################################################
# Carga las reseñas y calcula la puntuación media y el total de opiniones por estado (solo de pedidos a tiempo)
def loadData4():
    dfReviews = pd.read_csv('./streamlit_resources/order_reviews_dataset.csv')
    
    dfMergeOrdersCustomers = pd.merge(dfCustomersBase, dfOrdersBase, on='customer_id')
    
    # Condicional de si es tarde o no
    dfMergeOrdersCustomers['pedidos_tarde'] = (
        pd.to_datetime(dfMergeOrdersCustomers['order_delivered_customer_date']) > 
        pd.to_datetime(dfMergeOrdersCustomers['order_estimated_delivery_date'])
    )
    
    # Juntamos reseñas con los pedidos y clientes
    dfMergeReviewsCustomers = pd.merge(dfReviews, dfMergeOrdersCustomers, on='order_id')
    
    df_estado_reviews = dfMergeReviewsCustomers[dfMergeReviewsCustomers['pedidos_tarde'] == False].groupby('customer_state').agg({'review_score': 'mean', 'review_id': 'count'}).rename(columns={'review_score':'score_average','review_id':'review_count'}).reset_index()

    return df_estado_reviews.sort_values(by='score_average', ascending=False)

####################### INPUTS ###########################

st.title('Dashboard de Análisis de Ventas')
st.markdown('Filtra los datos por fecha y cantidad de elementos a mostrar.')

fechaMinInput = st.datetime_input(
    'Elige la Fecha minima',
    datetime.datetime(2014, 11, 19, 16, 45),
)

fechaMaxInput = st.datetime_input(
    'Elige la fecha maxima',
    datetime.datetime(2025, 11, 19, 16, 45),
)

numero_filas = st.number_input('Inserta un numero', value=10, step=1)

st.write('Estas filtrando por ', numero_filas , ' filas')

########################## Ejercicio 1 ################################

st.divider()
st.header('1. Clientes por estado y ciudad')

datos_clientes = loadData(fechaMinInput, fechaMaxInput)

st.write(datos_clientes[['customer_city','customer_state','customer_unique_id']].head(numero_filas))
st.divider()
st.bar_chart(datos_clientes.head(numero_filas), x='customer_city', y='customer_id')

########################## Ejercicio 2 ################################

st.divider()
st.header('2. Pedidos por ciudad')

datos_porcentajes = loadData2(datos_clientes)

st.write(datos_porcentajes.head(numero_filas))

st.divider()

etiquetas_ciudades = datos_porcentajes['customer_city'].head(numero_filas)
valores_porcentajes = datos_porcentajes['orders_percent'].head(numero_filas)

figura_grafico, eje_grafico = plt.subplots(figsize=(8, 8))

eje_grafico.pie(valores_porcentajes, labels=etiquetas_ciudades, autopct='%1.1f%%', startangle=90)
eje_grafico.axis('equal')

st.pyplot(figura_grafico)

st.markdown("Ratio de pedidos por cliente")
st.bar_chart(
    datos_porcentajes.head(numero_filas).set_index('customer_city')['proporcion_pedidos_cliente']
)

########################## Ejercicio 3 ################################

st.divider()
st.header('3. Análisis de retrasos en pedidos')

datos_retrasos = loadData3A(datos_porcentajes)

st.markdown('Datos de todos los retrasos por ciudad')
st.write(datos_retrasos)

st.bar_chart(
    datos_retrasos.head(numero_filas), 
    x='city_state', 
    y='pedidos_tarde'
)


st.divider()

st.markdown('Media de días tarde por ciudad')

datos_dias_retraso = loadData3B()

st.write(datos_dias_retraso)

st.bar_chart(
    datos_dias_retraso.head(numero_filas), 
    x='city_state', 
    y='tiempo_retraso_medio'
)

st.markdown('> Las ciudades grandes como Sao Paulo tienen un porcentaje de retrasos entre 5 y 25% porque los repartidores locales están saturados por el volumen de paquetes. En cambio, los pueblos lejanos como Montanha tienen esperas larguísimas porque las rutas de transporte hasta allí están rotas o fallan por completo')

########################## Ejercicio 4 ################################

st.divider()
st.header('4. Reviews y satisfacción del cliente')

datos_reviews_clientes = loadData4()

st.write(datos_reviews_clientes.head(numero_filas))


st.markdown("Puntuación media de valoraciones por estado")
st.bar_chart(
    datos_reviews_clientes.head(numero_filas), 
    x='customer_state', 
    y='score_average'
)
