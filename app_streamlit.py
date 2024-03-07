import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import streamlit.components.v1 as c
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from pmdarima.arima import auto_arima
from statsmodels.tsa.seasonal import seasonal_decompose
from statistics import mode
from sklearn.metrics import mean_squared_error
import logging
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate=False
logger.setLevel(logging.CRITICAL)
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="DataChef",
                   page_icon=":electric_plug:")

color_de_fondo = "#363636"

seleccion = st.sidebar.radio("Menú", ['Introducción', 'ETL', 'Análisis de datos', 'Predicciones'], index=0)

if seleccion == "Introducción":
# if opcion_introduccion:
    st.subheader('Objetivo del proyecto:')
    img = Image.open("./Media/header.png")
    imagen = img.resize((800, 300))
    st.image(imagen)
    texto = """
                En un mercado gastronómico cada vez más competitivo, el éxito de un restaurante se sustenta en la eficiencia y la rentabilidad. 
                La intuición y la experiencia tradicionales ya no bastan en este entorno. 
                Para destacarse, los restaurantes deben valerse de herramientas que les permitan tomar decisiones estratégicas respaldadas por datos concretos. 
                El análisis de datos y la implementación de modelos predictivos se vuelven imprescindibles en este contexto. 
                Estas tecnologías innovadoras ofrecen una perspectiva hacia el futuro al proporcionar información valiosa sobre el comportamiento de los clientes, las tendencias del mercado y el rendimiento del negocio. 
                El propósito de este proyecto de análisis de datos es aprovechar estas tecnologías para optimizar las operaciones y estrategias de ventas del restaurante, aumentando su eficiencia y rentabilidad. 
                A través de un minucioso análisis de los datos disponibles, se identificarán áreas de mejora, se desarrollarán modelos predictivos para la demanda y la toma de decisiones, y se personalizará la experiencia del cliente."""
    st.write(texto)

elif seleccion == "ETL":
    st.subheader('Extracción inicial de datos:')
    texto = """Obtenemos los datos con los que el restaurante cuenta actualmente, a través de la API con la que el local trabaja.
                Podemos ver la estructura que tenian en ese momento:
            """
    st.write(texto)
    
    with st.expander('Datos sin procesar'):
        df = pd.read_csv("./base_de_datos/archivos_csv/ventas_historico.csv")
        st.write(df)
  
    st.subheader('Transformación de los datos:')
    texto ="""Creación de tablas y relaciones:
              Mediante cambios en la estructura de los datos, se definieron distintas tablas en las que dividimos los registros, para su escalabilidad.
              De esta manera la base de datos no solo es más eficiente y optimiza el rendimiento, sino que permite hacer análisis más detallados de algunos puntos importantes, como las ventas por productos."""
    st.write(texto)


    with st.expander('Tabla jerarquias'):
        df = pd.read_csv("./base_de_datos/archivos_csv/hierarchy_v2.csv")
        st.write(df)

    with st.expander('Tabla productos'):
        df = pd.read_csv("./base_de_datos/archivos_csv/product_v2.csv")
        st.write(df)

    with st.expander('Tabla ventas por productos'):
        df = pd.read_csv("./base_de_datos/archivos_csv/ventaxproducts_v2.csv")
        st.write(df)

    with st.expander('Tabla meseros'):
        df = pd.read_csv("./base_de_datos/archivos_csv/meseros.csv")
        st.write(df)

    with st.expander('Tabla mesas'):
        df = pd.read_csv("./base_de_datos/archivos_csv/mesas.csv")
        st.write(df)

    with st.expander('Tabla formas de pago'):
        df = pd.read_csv("./base_de_datos/archivos_csv/tipos_forma_pago.csv")
        st.write(df)     

    with st.expander('Tabla ventas por forma de pago'):
        df = pd.read_csv("./base_de_datos/archivos_csv/forma_pago.csv")
        st.write(df)

    with st.expander('Tabla ordenes'):
        df = pd.read_csv("./base_de_datos/archivos_csv/orders.csv")
        st.write(df)

    with st.expander('Tabla información sobre ordenes'):
        df = pd.read_csv("./base_de_datos/archivos_csv/orders_info.csv")
        st.write(df)   

    st.subheader('Estructura final de nuestra base de datos:')
    texto ="""Relaciones entre las distintas tablas:"""
    st.write(texto)    

    # with st.expander('Relaciones'):
    img = Image.open("./Media/diagrama.png")
    imagen = img.resize((800, 400))
    st.image(imagen)    

elif seleccion == "Análisis de datos":

    st.write("## Análisis de datos:")
    st.write("A través de Power BI realizamos un análisis de los datos del restaurante, que se pueden consultar de manera interactiva en el siguiente dashboard:")

    st.write("<iframe width='1000' height='600' src='https://app.powerbi.com/view?r=eyJrIjoiYmM1YTUzNWEtOGEwNC00NTlmLTg2YTQtOWIyNzEyYzdmOTExIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9' style='display:block;margin:auto;'></iframe>", unsafe_allow_html=True)

elif seleccion == "Predicciones":

    df_pivot = pd.read_csv("./base_de_datos/archivos_csv/pivot.csv")
    df_pivot['fecha'] = pd.to_datetime(df_pivot['fecha'])
    df_pivot.set_index('fecha', inplace=True)
    df_pivot = df_pivot.rolling(window=3, min_periods=1).mean()
    # st.write(df_pivot)

    opciones = [product for product in df_pivot.columns[:-1]]
    opcion_seleccionada = st.selectbox('Selecciona un producto:', opciones)
    
    # Realizar la descomposición estacional
    decomposed = seasonal_decompose(df_pivot[opcion_seleccionada], model='additive', period=4)
    # Graficar
    st.subheader('Descomposición estacional:')
    # texto = """
    #         Gráfico de tendencia: La tendencia de las cantidades vendidas del producto muestra la variación  a lo largo de aproximadamente dos años y medio. Estas tendencias podría indicar cambios en la demanda del producto, influenciados por factores externos como la introducción de nuevos productos competidores, cambios en el mercado, o modificaciones en las estrategias de marketing y ventas.\n
    #         Gráfico de estacionalidad: La estacionalidad es muy regular y pronunciada, con picos y valles que ocurren en intervalos consistentes semana tras semana. Esto sugiere que hay factores estacionales que afectan las ventas del producto en un ciclo semanal. Estos podrían estar relacionados con hábitos de consumo que varían en los días de la semana, promociones semanales, o factores externos como eventos o festividades que ocurren regularmente y que tienen un impacto en las ventas.\n
    #         Gráfico de residuales : Los residuos representan las variaciones en las ventas que no son explicadas por la tendencia general o por la estacionalidad. Estas variaciones parecen ser bastante erráticas y no siguen un patrón claro, lo que sugiere que hay otros factores aleatorios o no medidos que están afectando las ventas del producto. Esto podría incluir eventos inesperados como cambios económicos, incidentes de suministro, o actividades promocionales no regulares.
    #         """
    # st.write(texto)

    # fig, axs = plt.subplots(3, 1, figsize=(10, 20))
    # # Graficar la tendencia
    # axs[0].set_title('Tendencia')
    # axs[0].plot(decomposed.trend)
    # axs[0].tick_params(axis='x', rotation=45)
    # # Graficar la estacionalidad
    # axs[1].set_title('Estacionalidad')
    # axs[1].plot(decomposed.seasonal)
    # axs[1].tick_params(axis='x', rotation=45)
    # # Graficar los residuales
    # axs[2].set_title('Residuales')
    # axs[2].plot(decomposed.resid)
    # axs[2].tick_params(axis='x', rotation=45)
    # # Mostrar la gráfica en Streamlit
    # st.pyplot(fig)

 # Graficar la estacionalidad
    st.write("Gráfico de tendencia: La tendencia de las cantidades vendidas del producto muestra la variación  a lo largo de aproximadamente dos años y medio. Estas tendencias podría indicar cambios en la demanda del producto, influenciados por factores externos como la introducción de nuevos productos competidores, cambios en el mercado, o modificaciones en las estrategias de marketing y ventas.\n")
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    axs.set_title('Tendencia')
    axs.plot(decomposed.trend)
    axs.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Graficar la estacionalidad
    st.write("Gráfico de estacionalidad: La estacionalidad es muy regular y pronunciada, con picos y valles que ocurren en intervalos consistentes semana tras semana. Esto sugiere que hay factores estacionales que afectan las ventas del producto en un ciclo semanal. Estos podrían estar relacionados con hábitos de consumo que varían en los días de la semana, promociones semanales, o factores externos como eventos o festividades que ocurren regularmente y que tienen un impacto en las ventas.")
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    axs.set_title('Estacionalidad')
    axs.plot(decomposed.seasonal)
    axs.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Graficar los residuales
    st.write("Gráfico de residuales : Los residuos representan las variaciones en las ventas que no son explicadas por la tendencia general o por la estacionalidad. Estas variaciones parecen ser bastante erráticas y no siguen un patrón claro, lo que sugiere que hay otros factores aleatorios o no medidos que están afectando las ventas del producto. Esto podría incluir eventos inesperados como cambios económicos, incidentes de suministro, o actividades promocionales no regulares.")
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    axs.set_title('Residuales')
    axs.plot(decomposed.resid)
    axs.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    def walk_forward_validation(data, n_test):
        if len(data) < n_test:
            raise ValueError("No hay suficientes datos para realizar la validación cruzada.")
    
        predictions = []
        train, test = data[:-n_test], data[-n_test:]
        history = [x for x in train]
        # st.write(train)
        # st.write(test)
            
        for i in range(len(test)):
            model = auto_arima(history, seasonal=True, m=4, stepwise=True, suppress_warnings=True, 
                            error_action="ignore", max_order=None, trace=False)
            yhat = model.predict(n_periods=1)[0]
            predictions.append(yhat)
            # st.write(test.iloc[i])
            history.append(test.iloc[i])  # Agrega observaciones al entrenamiento para el próximo ciclo.
            
        error = np.sqrt(mean_squared_error(test, predictions))
        return error, test, predictions, model

    resultados_rmse_wf= {}
    modelos_entrenados = {}

    # Ajuste de la cantidad de datos de prueba para la validación cruzada
    n_test = 5  # Ejemplo: usar los últimos 5 puntos para la prueba

    serie_temporal = df_pivot[opcion_seleccionada].dropna()  
    # Aplicar validación cruzada "walk-forward"
    error, test, predictions, model = walk_forward_validation(serie_temporal, n_test)
    # Almacenar el modelo entrenado
    modelos_entrenados[opcion_seleccionada] = model

    st.subheader('Predicciones vs valores reales:')
    # st.write(modelos_entrenados)
    st.write("El Root Mean Square Error (RMSE) es una medida de la precisión de un modelo de regresión. Mide la diferencia entre los valores predichos por el modelo y los valores observados. Cuanto menor sea, mejor se ajusta el modelo a los datos observados.")
    # Imprimir el RMSE para cada producto
    st.write(f"RMSE de validación cruzada para {opcion_seleccionada}: {error:.3f}")
    st.write("Veamos gráficamente la diferencia entre las predicciones y los valores observados, para un periodo determinado: ")

    # Fechas para el eje x
    fechas = serie_temporal.index[-n_test:]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fechas, test, marker='o', label='Real')
    ax.plot(fechas, predictions, marker='x', linestyle='--', label='Pronóstico')
    ax.set_title(f'Validación Cruzada Walk-Forward para {opcion_seleccionada}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valores')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    def predict_for_specific_date(product, target_date, df_pivot, modelos_entrenados):
        if product not in df_pivot.columns:
            st.write("Producto no encontrado.")
            return None
        
        model = modelos_entrenados.get(product)
        
        if model is None:
            st.write("No se encontró un modelo entrenado para este producto.")
            return None

        target_date = pd.to_datetime(target_date)
        # st.write(target_date)
        last_known_data = df_pivot[product].dropna()
        # st.write(last_known_data)
        last_known_date = last_known_data.index[-1]
        # st.write(last_known_date)

        if target_date <= last_known_date:
            print("La fecha objetivo debe ser posterior a la última fecha conocida en los datos.")
            return None

        periods_ahead = (target_date - last_known_date).days // 7

        # Asumiendo que los datos son semanales, ajustamos la serie temporal
        future_data = last_known_data.copy()
        # st.write(future_data.index[-1])
        for i in range(periods_ahead):
            # Entrenar el modelo con los datos actuales
            model = auto_arima(future_data, seasonal=True, m=4, stepwise=True, suppress_warnings=True,
                            error_action="ignore", max_order=None, trace=False)

            # Predecir el siguiente punto
            next_prediction = model.predict(n_periods=1)[0]
            # st.write(next_prediction)
            # Actualizar los datos históricos con la nueva predicción
            new_index = future_data.index[-1] + pd.DateOffset(weeks=1)
            # st.write(new_index)
            # st.write(future_data)
            future_data = pd.concat([future_data, pd.Series([next_prediction], index=[new_index])])

        prediction_for_target_date = future_data.iloc[-1]
        return prediction_for_target_date

    producto_seleccionado = opcion_seleccionada  # Asegúrate de que este producto esté en df_pivot.columns
   
    # Obtener la fecha actual
    today = datetime.date.today()
    # Definir la fecha mínima y máxima permitida para el input
    min_date = datetime.date(today.year, 3, 1)
    max_date = datetime.date(today.year, 3, 31)

    st.subheader('Realizar predicción:')
    # Permitir que el usuario seleccione una fecha en marzo
    st.write("A continuación puede realizar una predicción para el producto seleccionado. El resultado será para la semana total, no para el día específico:")
    fecha_objetivo = st.date_input("Selecciona una fecha:", min_value=min_date, max_value=max_date)
    # Convertir la fecha seleccionada a string
    fecha_objetivo_str = fecha_objetivo.strftime('%Y-%m-%d')
    st.write(f"Fecha seleccionada: {fecha_objetivo_str}")

    # Asegúrate de que df_pivot y modelos_entrenados están definidos y contienen los datos/modelos correctos
    prediccion = predict_for_specific_date(producto_seleccionado, fecha_objetivo, df_pivot, modelos_entrenados)

    st.write(f"La predicción de ventas ajustada al final de la semana para {producto_seleccionado} en {fecha_objetivo} es:")
    st.write(f"{ceil(prediccion)} unidades.")
