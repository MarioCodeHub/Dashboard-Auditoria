import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(page_title="Dashboard de Auditoría", layout="wide")
st.title("📊 Dashboard de Auditoría y Control Operativo")

# GENERACIÓN DE DATOS
np.random.seed(42)
num_registros = 500
sedes = ['Sede Norte', 'Sede Sur', 'Sede Centro', 'Sede Occidente']
categorias = ['Nómina', 'Servicios', 'Suministros', 'Ventas', 'Mantenimiento']

fecha_inicio = datetime.now() - timedelta(days=60)
fechas = [fecha_inicio + timedelta(days=int(np.random.randint(0, 60))) for _ in range(num_registros)]

data = {
    'ID_Transaccion': [f"TRX-{1000 + i}" for i in range(num_registros)],
    'Fecha': fechas,
    'Sede': np.random.choice(sedes, num_registros),
    'Categoria': np.random.choice(categorias, num_registros),
    'Ingresos': np.round(np.random.uniform(500, 5000, num_registros), 2),
    'Egresos': np.round(np.random.uniform(200, 3500, num_registros), 2),
    'Estado_Operativo': np.random.choice(['Completado', 'Pendiente', 'En Revisión'], num_registros, p=[0.7, 0.2, 0.1])
}

df = pd.DataFrame(data)

df['Saldo_Esperado'] = df['Ingresos'] - df['Egresos']
desfases = np.random.choice([0, 0, 0, 0, -150, 200, -50, 300], num_registros)
df['Saldo_Real'] = df['Saldo_Esperado'] + desfases
df['Diferencia_Cuadre'] = df['Saldo_Real'] - df['Saldo_Esperado']
df['Tiene_Inconsistencia'] = df['Diferencia_Cuadre'] != 0

st.sidebar.header("🔍 Filtros de Auditoría")
sede_seleccionada = st.sidebar.selectbox("🏢 Selecciona Sede:", ['TODAS'] + list(df['Sede'].unique()))
chk_solo_descuadres = st.sidebar.checkbox("🚨 Mostrar solo descuadres")

df_filtrado = df.copy()
if sede_seleccionada != 'TODAS':
    df_filtrado = df_filtrado[df_filtrado['Sede'] == sede_seleccionada]

if chk_solo_descuadres:
    df_filtrado = df_filtrado[df_filtrado['Tiene_Inconsistencia'] == True]

ing_f = df_filtrado['Ingresos'].sum()
egr_f = df_filtrado['Egresos'].sum()
balance_f = df_filtrado['Saldo_Esperado'].sum()
desc_f = df_filtrado['Diferencia_Cuadre'].abs().sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Ingresos", f"${ing_f:,.2f}")
col2.metric("💸 Egresos", f"${egr_f:,.2f}")
col3.metric("📈 Balance Teórico", f"${balance_f:,.2f}")
col4.metric("⚠️ Descuadre Total", f"${desc_f:,.2f}")

st.divider()

fig = px.bar(
    df_filtrado,
    x='Fecha',
    y='Diferencia_Cuadre',
    color='Tiene_Inconsistencia',
    color_discrete_map={False: '#2ecc71', True: '#e74c3c'},
    title=f'📊 Arqueo de Caja y Descuadres Diarios - {sede_seleccionada}',
    labels={'Diferencia_Cuadre': 'Descuadre ($)', 'Tiene_Inconsistencia': '¿Tiene Descuadre?'}
)
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Detalle de Transacciones")
columnas_mostrar = [
    'ID_Transaccion', 'Sede', 'Fecha', 'Ingresos',
    'Egresos', 'Saldo_Esperado', 'Saldo_Real', 'Diferencia_Cuadre', 'Tiene_Inconsistencia'
]
st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True)
