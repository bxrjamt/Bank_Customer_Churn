# 💳 Abandono de Clientes de Tarjeta de Crédito

## 📌 Caso de negocio
El abandono de clientes (customer churn) es uno de los principales problemas en el sector financiero, especialmente en productos como las tarjetas de crédito, donde la rentabilidad depende directamente del nivel de uso y de la relación a largo plazo con el cliente.
Cuando un cliente deja de utilizar su tarjeta o decide cancelar el producto, la entidad bancaria no solo pierde los ingresos asociados a las transacciones, sino también el potencial de rentabilidad futura. Además, captar nuevos clientes suele ser significativamente más costoso que retener a los existentes.

Este proyecto tiene como objetivo desarrollar un modelo de predicción de abandono de clientes de tarjeta de crédito, utilizando información demográfica y, especialmente, variables de comportamiento y uso del producto. De esta forma, permitirá a la entidad adelantarse a la decisión de abandono de sus clientes, actuando en consecuencia para maximizar su relación en el tiempo y minimizar la pérdida de ingresos generados por el abandono.

## 🎯 Objetivos del Proyecto
Los objetivos principales de este proyecto son:

- Analizar el perfil demográfico y el comportamiento de los clientes.
- Comprender las diferencias entre clientes activos y clientes que abandonan (churn).
- Evaluar la calidad y coherencia de los datos disponibles.
- Construir modelos de machine learning para predecir el abandono de clientes.
- Identificar las variables más relevantes asociadas al churn.
- Traducir los resultados obtenidos en conclusiones accionables desde el punto de vista del negocio.


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

## Descripción del Dataset
Este dataset, disponible en Kaggle en formato CSV, contiene información de clientes de tarjetas de crédito de una entidad bancaria y se utiliza para abordar un problema de clasificación binaria, cuyo objetivo es predecir la probabilidad de abandono de un cliente (customer churn), es decir, identificar qué clientes tienen mayor riesgo de cancelar o dejar de utilizar el servicio.

Cada observación un cliente individual, identificado por un código único, e incluye variables demográficas, socioeconómicas y, principalmente, variables relacionadas con el uso de la tarjeta, las transacciones realizadas y la relación del cliente con el banco durante los últimos 12 meses.

La variable objetivo es Attrition_Flag, que indica si el cliente permanece activo (Existing Customer) o si ha abandonado el servicio de tarjeta de crédito (Attrited Customer). El conjunto de datos presenta un desbalance de clases, con aproximadamente un 84% de clientes activos frente a un 16% de clientes que han abandonado.

### Variables
- **CLIENTNUM**: identificador único del cliente.
- **Attrition_Flag**: estado del cliente (*Existing Customer* o *Attrited Customer*).
- **Customer_Age**: edad del cliente.
- **Gender**: género del cliente (M: masculino, F: femenino).
- **Dependent_count**: número de personas dependientes del cliente.
- **Education_Level**: nivel educativo del cliente.
- **Marital_Status**: estado civil del cliente.
- **Income_Category**: categoría de ingresos del cliente.
- **Card_Category**: tipo de tarjeta de crédito contratada.
- **Months_on_Book**: antigüedad del cliente en la entidad (en meses).
- **Total_Relationship_Count**: número total de productos contratados con el banco.
- **Months_Inactive_12_mon**: número de meses de inactividad en los últimos 12 meses.
- **Contacts_Count_12_mon**: número de contactos entre el banco y el cliente en los últimos 12 meses.
- **Credit_Limit**: límite de crédito asignado a la tarjeta.
- **Total_Revolving_Bal**: saldo de crédito utilizado.
- **Avg_Open_To_Buy**: crédito disponible (límite menos saldo utilizado).
- **Avg_Utilization_Ratio**: porcentaje de utilización del crédito disponible.
- **Total_Trans_Amt**: importe total de las transacciones realizadas en los últimos 12 meses.
- **Total_Trans_Ct**: número total de transacciones realizadas en los últimos 12 meses.
- **Total_Amt_Chng_Q4_Q1**: variación del importe de las transacciones entre el cuarto y el primer trimestre.
- **Total_Ct_Chng_Q4_Q1**: variación del número de transacciones entre el cuarto y el primer trimestre.







