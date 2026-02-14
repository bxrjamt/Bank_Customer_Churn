import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import random
from pathlib import Path

st.set_page_config(page_title="Sistema de Retención - Banco Hispanis", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
    :root{--primary:#0f3460;--accent:#1e88e5;--muted:#333333}
    .stApp { 
        background: linear-gradient(135deg, #c3e7ff 0%, #b3deff 100%);
        color: #000000;
    }
    body {
        background-color: #c3e7ff !important;
    }
    .stContainer, [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #c3e7ff 0%, #b3deff 100%);
        color: #000000;
    }
    .header{padding:18px; border-radius:10px; margin-bottom:8px; background:#ffffff; border-left:5px solid var(--primary)}
    .card{background:#ffffff;padding:12px;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.1);border:1px solid #e2e8f0}
    .email-box{background:#ffffff;padding:16px;border-left:5px solid var(--primary);border-radius:8px;color:#000000}
    .small{color:#333333;font-size:13px}
    h1, h2, h3, h4, h5, h6 {color: #000000 !important;}
    p, span, div {color: #000000 !important;}
    .stMetric {background:#ffffff;padding:12px;border-radius:10px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
    .stDataFrame {background:#ffffff !important;color:#000000 !important;}
    [data-testid="stBaseButton"]:nth-child(2) > button {
        background-color: #FCD34D !important;
        color: #000000 !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def cargar_datos():
    try:
        ruta = Path(__file__).parent.parent / "data" / "processed" / "clientes_inferencia.csv"
        return pd.read_csv(ruta)
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None


@st.cache_resource
def cargar_modelo():
    try:
        ruta = Path(__file__).parent.parent / "models" / "modelo_churn.joblib"
        return joblib.load(ruta)
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None


def identificar_variable_debil(cliente):
    problemas = []
    if cliente['Credit_Limit'] < 3000:
        problemas.append('credito')
    if cliente['Months_Inactive_12_mon'] >= 4:
        problemas.append('inactividad')
    if cliente['Avg_Utilization_Ratio'] < 0.3:
        problemas.append('uso')
    if cliente['Total_Trans_Ct'] < 50:
        problemas.append('transacciones')
    if cliente['Total_Relationship_Count'] <= 2:
        problemas.append('productos')

    for p in ['inactividad','uso','credito','productos','transacciones']:
        if p in problemas:
            return p
    return 'uso'


def generar_beneficio(variable, cliente):
    ofertas = {
        'credito': (f"Aumento límite a ${int(cliente['Credit_Limit']*1.5):,}", "Más flexibilidad financiera."),
        'inactividad': ("5% cashback 3 meses", "Incentivo para reactivar uso."),
        'uso': ("-2pp en interés", "Tasa preferente para tu tarjeta."),
        'productos': ("Cuenta Premium sin comisiones", "Beneficios exclusivos."),
        'transacciones': ("3,000 puntos al completar 5 compras", "Programa de recompensas.")
    }
    return {'oferta': ofertas[variable][0], 'detalle': ofertas[variable][1]}


def generar_email(cliente, beneficio=None, variable=None, razon=None, valor=None):
    # Lista de gestores y lista de nombres femeninos para detectar género
    gestores = [
        {"nombre": "Ana", "apellido": "Torres", "email": "ana.torres@bancohispanis.com"},
        {"nombre": "Carlos", "apellido": "Gómez", "email": "carlos.gomez@bancohispanis.com"},
        {"nombre": "Lucía", "apellido": "Martínez", "email": "lucia.martinez@bancohispanis.com"},
        {"nombre": "Javier", "apellido": "López", "email": "javier.lopez@bancohispanis.com"},
        {"nombre": "Laura", "apellido": "Sánchez", "email": "laura.sanchez@bancohispanis.com"},
        {"nombre": "Daniel", "apellido": "Pérez", "email": "daniel.perez@bancohispanis.com"},
        {"nombre": "María", "apellido": "Romero", "email": "maria.romero@bancohispanis.com"}
    ]
    nombres_femeninos = ["Ana", "Lucía", "Laura", "María"]

    # Elegir gestor aleatoriamente
    gestor = random.choice(gestores)
    gestor_nombre = f"{gestor['nombre']} {gestor['apellido']}"
    gestor_email = gestor["email"]
    es_mujer = gestor['nombre'] in nombres_femeninos

    # Saludo según edad
    if cliente["Customer_Age"] < 30:
        saludo = "Hola"
    elif cliente["Customer_Age"] <= 50:
        saludo = "Estimad@"
    else:
        saludo = "Distinguid@"

    # -------------------------
    # Detectar variable más débil
    # -------------------------
    if cliente["Credit_Limit"] < 5000:
        motivo = (
            f"Hemos visto que tu límite de crédito actual es de {cliente['Credit_Limit']} €, "
            "y creemos que disponer de un mayor margen puede darte más comodidad en tu día a día."
        )
        beneficio = "un aumento del 5 % en tu límite de crédito"

    elif cliente["Months_Inactive_12_mon"] > 6:
        motivo = (
            f"En los últimos 12 meses has estado {int(cliente['Months_Inactive_12_mon'])} meses sin actividad, "
            "algo que puede ocurrir cuando cambian las rutinas."
        )
        beneficio = "un cashback del 0.3 % en tus próximas compras"

    elif cliente["Avg_Utilization_Ratio"] < 0.2:
        motivo = (
            f"Actualmente tu nivel de utilización del crédito es bajo "
            f"(ratio de {cliente['Avg_Utilization_Ratio']:.2f}), "
            "y queremos que puedas aprovecharlo en mejores condiciones."
        )
        beneficio = "una reducción del interés de tu crédito de entre un 1 % y un 2 %"

    elif cliente["Total_Relationship_Count"] == 1:
        motivo = (
            "Actualmente solo cuentas con un producto en Banco Hispanis, "
            "y creemos que podrías beneficiarte de una relación más completa con nosotros."
        )
        beneficio = "un nuevo producto del banco con condiciones especiales"

    else:
        motivo = (
            "Tu perfil muestra un uso equilibrado de nuestros productos, "
            "y queremos seguir ofreciéndote ventajas adaptadas a ti."
        )
        beneficio = "un beneficio exclusivo adaptado a tu perfil"

    # -------------------------
    # Email final
    # -------------------------
    return f"""
{saludo} cliente,

Espero que se encuentre bien. Mi nombre es {gestor_nombre} y soy tu gestor/a de cuentas en Banco Hispanis.
{motivo}
Por este motivo, queremos ofrecerte {beneficio}, con el objetivo de que sigas sacando el máximo partido a nuestros servicios.
Si tienes cualquier duda o necesitas asesoramiento para aprovechar mejor tu cuenta, no dudes en ponerte en contacto conmigo. Estaré encantad@ de ayudarte.

Un saludo muy cordial,

{gestor_nombre}
Gestor/a de Cuentas
Banco Hispanis
Tel: 123-456-789
Email: {gestor_email}
"""


def generar_prompt(cliente):
    # Ajustamos el tono según la edad
    if cliente['Customer_Age'] < 30:
        tono = "relajado, amigable y con un toque de cercanía. Usa expresiones más coloquiales."
    elif 30 <= cliente['Customer_Age'] <= 50:
        tono = "profesional pero accesible. Mantén un equilibrio entre seriedad y amabilidad."
    else:
        tono = "formal y respetuoso, con un enfoque en mostrar confianza y seguridad."

    prompt = f"""
    Este cliente tiene {cliente['Customer_Age']} años, un límite de crédito de {cliente['Credit_Limit']}, ha estado inactivo {cliente['Months_Inactive_12_mon']} meses en los últimos 12 meses,
    ha realizado {cliente['Total_Trans_Ct']} transacciones y tiene un ratio de utilización de {cliente['Avg_Utilization_Ratio']}. Además, su Total_Relationship_Count es {cliente['Total_Relationship_Count']}.

    Si el límite de crédito es bajo, ofrécele un aumento de un 5% de crédito para retenerlo.
    Si ha estado inactivo muchos meses o tiene pocas transacciones, ofrécele un incentivo como cashback del 0.1% al 0.3% para volver a utilizar los productos.
    Si tiene baja utilización ofrécele intereses menores reduciendo 1% o 2% el interés del crédito.
    Si tiene un solo producto (Total_Relationship_Count bajo), ofrécele otro producto del banco con descuento.

    Ofrece únicamente un beneficio basado en la variable con el rendimiento más bajo.

    Genera un email de comunicación personalizado utilizando un tono {tono}. El mensaje debe ser claro y adaptarse al perfil del cliente según sus datos.
    """
    return prompt


# CARGA
df = cargar_datos()
modelo = cargar_modelo()
if df is None or modelo is None:
    st.stop()


with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bank-building.png", width=72)
    st.markdown("## 🎚️ Controles de Retención")
    st.markdown('---')
    umbral = st.slider('Umbral de churn', min_value=0.3, max_value=0.9, value=0.5, step=0.05)
    edad_min, edad_max = int(df['Customer_Age'].min()), int(df['Customer_Age'].max())
    edad_rango = st.slider('Rango de edad', min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max))
    productos = st.multiselect('Nº de productos', options=sorted(df['Total_Relationship_Count'].unique()), default=sorted(df['Total_Relationship_Count'].unique()))
    st.markdown('---')
    analizar = st.button('🚀 Analizar clientes en riesgo', type='primary', use_container_width=True)
    #resetear = st.button('🔄 Resetear Filtros',type="tertiary", use_container_width=True)
    
    #if resetear:
        # Limpiar el session state para resetear los filtros
        #if 'df_filtrado' in st.session_state:
            #del st.session_state['df_filtrado']
        #if 'umbral' in st.session_state:
            #del st.session_state['umbral']
        #st.rerun()
    
    st.info('Ajusta el umbral para segmentar distintos niveles de riesgo')


st.markdown('<div class="header"><h2 style="margin:0">🏦 Sistema de Retención de Clientes – Banco Hispanis</h2></div>', unsafe_allow_html=True)


if analizar or 'df_filtrado' not in st.session_state:
    with st.spinner('Analizando...'):
        df_filtrado = df[(df['churn_proba'] >= umbral) & (df['Customer_Age'] >= edad_rango[0]) & (df['Customer_Age'] <= edad_rango[1]) & (df['Total_Relationship_Count'].isin(productos))].copy()
        df_filtrado = df_filtrado.sort_values('churn_proba', ascending=False)
        st.session_state['df_filtrado'] = df_filtrado
        st.session_state['umbral'] = umbral

if 'df_filtrado' in st.session_state:
    df_filtrado = st.session_state['df_filtrado']
    total = len(df)
    riesgo_cnt = len(df_filtrado)
    pct = (riesgo_cnt/total*100) if total>0 else 0
    riesgo_prom = df_filtrado['churn_proba'].mean() if riesgo_cnt>0 else 0

    c1, c2, c3, c4 = st.columns([1.6,1,1,1])
    c1.markdown(f"<div class='card'><div style='font-weight:700;font-size:20px'>👥 {total:,}</div><div class='small'>Clientes Totales</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><div style='font-weight:700;font-size:20px'>⚠️ {riesgo_cnt:,}</div><div class='small'>Clientes en Riesgo</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><div style='font-weight:700;font-size:20px'>📈 {pct:.1f}%</div><div class='small'>% en Riesgo</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'><div style='font-weight:700;font-size:20px'>🎯 {riesgo_prom:.1%}</div><div class='small'>Riesgo Medio</div></div>", unsafe_allow_html=True)

    st.markdown('---')

    if len(df_filtrado)>0:
        st.subheader('📋 Clientes en Riesgo')
        df_muestra = df_filtrado[['Customer_Age','Credit_Limit','Months_Inactive_12_mon','Avg_Utilization_Ratio','Total_Relationship_Count','churn_proba']].copy()
        df_muestra.columns = ['Edad','Límite Crédito','Meses Inactivo','Uso Crédito','Nº Productos','Probabilidad Churn']
        df_muestra['Límite Crédito'] = df_muestra['Límite Crédito'].map(lambda x: f"${x:,.0f}")
        df_muestra['Uso Crédito'] = df_muestra['Uso Crédito'].map(lambda x: f"{x:.1%}")
        # Mostrar siempre el valor calculado en el dataset (crudo) con 8 decimales
        df_muestra['Probabilidad Churn'] = df_muestra['Probabilidad Churn'].map(lambda x: f"{x:.8f}")
        st.dataframe(df_muestra, width='stretch', height=340)

        # Análisis individual a ancho completo y datos ordenados
        st.subheader('👤 Análisis Individual')
        idx = st.selectbox('Selecciona cliente', options=df_filtrado.index, format_func=lambda x: f"Cliente #{x} - {df_filtrado.loc[x,'churn_proba']:.8f}")
        cliente = df_filtrado.loc[idx]
        
        
        # Mapeo de variables a nombres en español
        mapeo_variables = {
                "Credit_Limit": "Límite de crédito",
                "Months_Inactive_12_mon": "Meses inactivo",
                "Avg_Utilization_Ratio": "Ratio de utilización",
                "Total_Trans_Ct": "Total transacciones",
                "Total_Relationship_Count": "Total productos vinculados"
            }
        
        factores = []
        if cliente['Credit_Limit'] < 3000:
            factores.append(("Credit_Limit", f"${cliente['Credit_Limit']:,.0f}"))
        if cliente['Months_Inactive_12_mon'] >= 4:
            factores.append(("Months_Inactive_12_mon", f"{int(cliente['Months_Inactive_12_mon'])} meses"))
        if cliente['Avg_Utilization_Ratio'] < 0.3:
            factores.append(("Avg_Utilization_Ratio", f"{cliente['Avg_Utilization_Ratio']:.1%}"))
        if cliente['Total_Trans_Ct'] < 50:
            factores.append(("Total_Trans_Ct", f"{int(cliente['Total_Trans_Ct'])}"))
        if cliente['Total_Relationship_Count'] <= 2:
            factores.append(("Total_Relationship_Count", f"{int(cliente['Total_Relationship_Count'])}"))

        # Construir el contenido completo de la tarjeta
        contenido_tarjeta = "<div class='card' style='padding:10px; border-radius:6px;'>"
        contenido_tarjeta += "Variables que pueden influir en la decisión de irse:<br>"

        if len(factores) == 0:
            contenido_tarjeta += "- No se detectan factores críticos según los umbrales definidos."
        else:
            for variable, valor in factores:
                var_español = mapeo_variables.get(variable, variable)
                contenido_tarjeta += f"- <strong>{var_español}</strong>: {valor}<br>"

        contenido_tarjeta += "</div>"

        # Mostrar todo en un solo st.markdown para evitar bloques vacíos
        st.markdown(contenido_tarjeta, unsafe_allow_html=True)

            # Conclusión breve y concreta (recuadro amarillo) con icono de alerta
        weak = identificar_variable_debil(cliente)
        mapping_conclusion = {
                'credito': '⚠️ Bajo límite de crédito',
                'inactividad': '⚠️ Alta inactividad',
                'uso': '⚠️ Bajo uso del crédito',
                'productos': '⚠️ Pocos productos vinculados',
                'transacciones': '⚠️ Pocas transacciones'
            }
        conclusion_text = mapping_conclusion.get(weak, '⚠️ Factor de riesgo detectado')
        st.warning(conclusion_text)

        st.markdown('---')

        # Generar email personalizado (simulado con los umbrales)
        email = generar_email(cliente)
        st.subheader('📧 Comunicación de Retención')
        # Convertir saltos de línea en <br> para máximo ajuste
        email_html = email.strip().replace("\n", "<br>")

        # Mostrar email en tarjeta compacta
        st.markdown(f"""
        <div style='background:#f0f8ff; border-left:5px solid #0f3460; padding:5px; margin-bottom:4px; font-size:15px; line-height:1.2;'>
        {email_html}
        </div>
        """, unsafe_allow_html=True)

            
        # Crear botones pegados usando HTML
        st.markdown("""
        <div style="display: flex; gap: 0px;">
            <form action="#" target="_self">
                <input type="submit" value="📧 Enviar Email" style="margin:0; padding:6px 12px; font-size:14px;">
            </form>
            <form action="#" target="_self">
                <input type="submit" value="📞 Programar Llamada" style="margin:0; padding:6px 12px; font-size:14px;">
            </form>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('---')

        # Visualizaciones colocadas después del análisis individual (abajo)
        st.subheader('📊 Visualizaciones')
        fig, axes = plt.subplots(2, 2, figsize=(18, 10))  # 2 filas x 2 columnas

        # 1) Media de churn_proba por número de productos - fila 1, columna 1
        ax1 = axes[0, 0]
        if 'Total_Relationship_Count' in df.columns:
            mean_by_products = df.groupby('Total_Relationship_Count')['churn_proba'].mean().sort_index()
            sns.barplot(x=mean_by_products.index.astype(str), y=mean_by_products.values, palette='Blues_d', ax=ax1)
            ax1.set_title('Relación entre Número de Productos y Probabilidad de Churn', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Número de Productos')
            ax1.set_ylabel('Probabilidad de Churn (%)')
            for i, v in enumerate(mean_by_products.values):
                ax1.text(i, v/2, f"{v*100:.1f}%", ha='center', va='center', color='white', fontweight='bold')
        else:
            sns.histplot(df['churn_proba'], bins=28, color='#4f46e5', ax=ax1)
            ax1.set_xlabel('churn_proba')

        # 2) Estado del cliente - fila 1, columna 2
        ax2 = axes[0, 1]
        # Filtrar por edad y productos (sin umbral) para mostrar todos los clientes
        df_v = df[(df['Customer_Age'] >= edad_rango[0]) & (df['Customer_Age'] <= edad_rango[1]) & (df['Total_Relationship_Count'].isin(productos))].copy()
        df_v['cat'] = df_v['churn_proba'].apply(lambda x: 'En Riesgo' if x>=st.session_state.get('umbral',umbral) else 'Seguros')
        conteo = df_v['cat'].value_counts().reindex(['Seguros','En Riesgo']).fillna(0)
        sns.barplot(x=conteo.index, y=conteo.values, palette=['#10b981','#ef4444'], ax=ax2)
        ax2.set_title('Distribución de Clientes por Estado de Riesgo', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Estado del cliente')
        ax2.set_ylabel('Cantidad de Clientes')
        for i, v in enumerate(conteo.values):
            ax2.text(i, v/2, f"{int(v)}", ha='center', va='center', color='white', fontweight='bold')

        # 3) Boxplot por rango de edad - fila 2, columna 1
        ax3 = axes[1, 0]
        df_edad = df.copy()
        df_edad['rango'] = pd.cut(df_edad['Customer_Age'], bins=[0,35,50,65,100], labels=['<35','35-50','50-65','65+'])
        sns.boxplot(data=df_edad, x='rango', y='churn_proba', palette='viridis', ax=ax3)
        ax3.axhline(st.session_state.get('umbral',umbral), color='red', linestyle='--')
        ax3.set_title('Probabilidad de Churn por Rango de Edad', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Rango de edad')
        ax3.set_ylabel('Probabilidad de Churn')

        # 4) Mapa de calor: Churn por Límite de Crédito vs Inactividad - fila 2, columna 2
        ax4 = axes[1, 1]
        if 'Credit_Limit' in df.columns and 'Months_Inactive_12_mon' in df.columns:
            df_heatmap = df.copy()
            df_heatmap['credit_bin'] = pd.cut(df_heatmap['Credit_Limit'], bins=5, labels=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'])
            df_heatmap['inactivity_bin'] = pd.cut(df_heatmap['Months_Inactive_12_mon'], bins=4, labels=['0-3 meses', '3-6 meses', '6-9 meses', '9+ meses'])
            heatmap_data = df_heatmap.pivot_table(values='churn_proba', index='inactivity_bin', columns='credit_bin', aggfunc='mean')
            sns.heatmap(heatmap_data * 100, annot=True, fmt='.1f', cmap='RdYlGn_r', ax=ax4, cbar_kws={'label': 'Churn %'})
            ax4.set_title('Churn por Límite de Crédito e Inactividad', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Límite de Crédito')
            ax4.set_ylabel('Meses Inactivo')

        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.info('No hay clientes en riesgo con los filtros actuales.')
else:
    st.info("👈 Ajusta filtros y haz clic en 'Analizar clientes en riesgo' para comenzar")

st.markdown('---')
st.markdown("<div style='text-align:center;color:#6b7280;font-weight:700'>🏦 Banco Hispanis</div>", unsafe_allow_html=True)
