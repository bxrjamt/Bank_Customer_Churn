import pandas as pd
import joblib
import sys

print("Verificando componentes de la aplicación...")
print("-" * 50)

try:
    df = pd.read_csv('data/processed/clientes_inferencia.csv')
    print(f"✅ Dataset cargado: {len(df)} filas")
    print(f"   Columnas principales: {', '.join(list(df.columns)[:8])}")
    print(f"✅ Rango de churn_proba: {df['churn_proba'].min():.4f} - {df['churn_proba'].max():.4f}")
except Exception as e:
    print(f"❌ Error cargando dataset: {e}")
    sys.exit(1)

try:
    modelo = joblib.load('models/modelo_churn.joblib')
    print(f"✅ Modelo cargado correctamente: {type(modelo).__name__}")
except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    sys.exit(1)

print(f"\n📊 Estadísticas del dataset:")
print(f"   - Edad: {df['Customer_Age'].min():.0f} - {df['Customer_Age'].max():.0f} años")
print(f"   - Límite crédito promedio: ${df['Credit_Limit'].mean():,.0f}")
print(f"   - Clientes con churn_proba > 0.5: {(df['churn_proba'] > 0.5).sum()}")
print(f"   - Productos por cliente: {sorted(df['Total_Relationship_Count'].unique())}")

print("\n✅ Todo listo para ejecutar: streamlit run src/app.py")
