# 💳 Abandono de Clientes de Tarjeta de Crédito

## 📌 Caso de negocio
El abandono de clientes (customer churn) es uno de los principales problemas en el sector financiero, especialmente en productos como las tarjetas de crédito, donde la rentabilidad depende directamente del nivel de uso y de la relación a largo plazo con el cliente.
Cuando un cliente deja de utilizar su tarjeta o decide cancelar el producto, la entidad bancaria no solo pierde los ingresos asociados a las transacciones, sino también el potencial de rentabilidad futura. Además, captar nuevos clientes suele ser significativamente más costoso que retener a los existentes.

Este proyecto tiene como objetivo desarrollar un modelo de predicción de abandono de clientes de tarjeta de crédito, utilizando información demográfica y, especialmente, variables de comportamiento y uso del producto. De esta forma, permitirá a la entidad adelantarse a la decisión de abandono de sus clientes, actuando en consecuencia para maximizar su relación en el tiempo y minimizar la pérdida de ingresos generados por el abandono.

--------

## 🎯 Objetivos del Proyecto
Los objetivos principales de este proyecto son:

- Analizar el perfil demográfico y el comportamiento de los clientes.
- Comprender las diferencias entre clientes activos y clientes que abandonan (churn).
- Evaluar la calidad y coherencia de los datos disponibles.
- Construir modelos de machine learning para predecir el abandono de clientes.
- Identificar las variables más relevantes asociadas al churn.
- Traducir los resultados obtenidos en conclusiones accionables desde el punto de vista del negocio.

--------

## 📁 Estructura del Proyecto

```
credit_card_churn/
│
├── data/
│   ├── raw/BankChurn.csv      # Dataset original
│   └── processed/    # Datasets limpios y preparados
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_conclusions.ipynb
│
├── src/
│   └── app.py    
│
├── README.md
└── requirements.txt

```

--------

## Descripción del Dataset
Este dataset, disponible en Kaggle en formato CSV, contiene información de clientes de tarjetas de crédito de una entidad bancaria y se utiliza para abordar un problema de clasificación binaria, cuyo objetivo es predecir la probabilidad de abandono de un cliente (customer churn), es decir, identificar qué clientes tienen mayor riesgo de cancelar o dejar de utilizar el servicio.

Cada observación un cliente individual, identificado por un código único, e incluye variables demográficas, socioeconómicas y, principalmente, variables relacionadas con el uso de la tarjeta, las transacciones realizadas y la relación del cliente con el banco durante los últimos 12 meses.

La variable objetivo es Attrition_Flag, que indica si el cliente permanece activo (Existing Customer) o si ha abandonado el servicio de tarjeta de crédito (Attrited Customer). El conjunto de datos presenta un desbalance de clases, con aproximadamente un 84% de clientes activos frente a un 16% de clientes que han abandonado.

### Variables

- **CLIENTNUM**: número de cuenta del cliente. 
- **Attrition_Flag**: estado del cliente (*Existing Customer* o *Attrited Customer*).
- **Customer_Age**: edad del cliente.
- **Gender**: género del cliente (M: masculino, F: femenino).
- **Dependent_count**: número de personas dependientes del cliente.
- **Education_Level**: nivel educativo del cliente (Sin educación, Escuela Secundaria, Graduado, Universidad, Postgrado, Doctorado y Desconocido). 
- **Marital_Status**: estado civil del cliente (Soltero, Casado, Divorciado y Desconocido).
- **Income_Category**: categoría de ingresos del cliente (Menos de $40K, $40K-$60K, $60K-$80K, $80K-$120K, $120K+ y Desconocido).  
- **Card_Category**: tipo de tarjeta utilizada (Blue, Silver, Gold y Platinum). 
- **Months_on_Book**: tiempo como cliente (en meses)
- **Total_Relationship_Count**: número de productos utilizados por los clientes en el banco.  
- **Months_Inactive_12_mon**: periodo de inactividad en los últimos 12 meses.  
- **Contacts_Count_12_mon**: número de interacciones entre el banco y el cliente en los últimos 12 meses.  
- **Credit_Limit**: límite nominal de transacción de la tarjeta de crédito en un periodo. 
- **Total_Revolving_Bal**: fondos totales utilizados en un periodo.  
- **Avg_Open_To_Buy**: diferencia entre el límite de crédito asignado a la cuenta del titular y el saldo actual.
- **Avg_Utilization_Ratio**: porcentaje de utilización de la tarjeta de crédito.
- **Total_Trans_Amt**: importe total de las transacciones en los últimos 12 meses.
- **Total_Trans_Ct**: número total de transacciones realizadas en los últimos 12 meses.
- **Total_Amt_Chng_Q4_Q1**: incremento del importe de transacciones del cliente entre el cuarto y el primer trimestre.  
- **Total_Ct_Chng_Q4_Q1**: incremento del número de transacciones del cliente entre el cuarto y el primer trimestre. 

--------
## Herramientas utilizadas

- **Jupyter Notebook**: Para documentar el análisis paso a paso, incluyendo limpieza de datos, visualizaciones y comentarios.  
- **Python (pandas, matplotlib, seaborn)**: Para procesar los datos, calcular métricas clave y generar gráficos para el análisis exploratorio.  
- **SQL (SQLite)**: Para realizar consultas que permitan segmentar clientes, productos y regiones, y obtener insights claros de la base de datos.  
- **Power BI**: Para crear dashboards interactivos que muestren las ventas, KPIs y tendencias a lo largo del tiempo.

--------






