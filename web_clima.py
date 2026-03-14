import streamlit as st
import pandas as pd
import os
import plotly.graph_objs as go

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Clima El Faique", layout="centered", page_icon="🏛️")

# 2. CSS: EQUILIBRIO INSTITUCIONAL Y MODERNO
st.markdown("""
<style>
    /* Fondo oscuro pero no negro total */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main .block-container { padding-top: 2.5rem; max-width: 850px; }
    
    /* Banner Institucional */
    .institucional-header {
        background: linear-gradient(90deg, #1A2980 0%, #26D0CE 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
        border: 1px solid #2A3B8C;
    }
    .institucional-title { margin: 0; font-size: 2.2rem; font-weight: 800; color: white; letter-spacing: 0.5px; }
    .institucional-subtitle { margin: 5px 0 0 0; font-size: 1rem; font-weight: 500; color: #E0F2FE; text-transform: uppercase; letter-spacing: 1.5px;}
    
    /* Tarjetas con toques de color */
    .card-container { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
    .ux-card {
        flex: 1;
        background-color: #161B22;
        border-top: 4px solid #30363D;
        border-radius: 10px;
        padding: 1.5rem 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        text-align: center;
        transition: transform 0.2s;
    }
    .ux-card:hover { transform: translateY(-3px); }
    
    /* Colores específicos para cada métrica */
    .card-temp { border-top-color: #3399FF; }
    .card-hum { border-top-color: #00C853; }
    .card-alert { border-top-color: #FFD700; background-color: rgba(255, 215, 0, 0.03); }
    .card-normal { border-top-color: #00E5FF; }
    
    .ux-icon { font-size: 2rem; margin-bottom: 0.5rem; display: block; }
    .ux-label { font-size: 0.8rem; text-transform: uppercase; color: #8B949E; font-weight: 600; letter-spacing: 1px; }
    .ux-value { font-size: 2rem; font-weight: 700; color: #FFFFFF; margin-top: 0.5rem; line-height: 1.1;}
    .alert-text { color: #FFD700; }
    .normal-text { color: #00E5FF; }
    
    /* Panel de Contactos */
    .contacto-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-size: 0.95rem;
    }
    .update-text { text-align: right; color: #8B949E; font-size: 0.85rem; margin-bottom: 1rem; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# 3. ENCABEZADO CON ESCUDO
st.markdown("""
<div class="institucional-header">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d6/Escudo_san_miguel_de_el_faique.png" alt="Escudo de San Miguel de El Faique" style="width: 90px; margin-bottom: 15px; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.5));">
    <h1 class="institucional-title">Municipalidad Distrital de San Miguel de El Faique</h1>
    <div class="institucional-subtitle">Portal Oficial de Alerta Temprana 🌧️</div>
</div>
""", unsafe_allow_html=True)

# 4. LÓGICA Y TARJETAS
if os.path.exists("historial_clima.csv"):
    df = pd.read_csv("historial_clima.csv")
    df['Timestamp'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])
    ultimo_dato = df.iloc[-1]
    
    st.markdown(f"<div class='update-text'>Última lectura automática: Hoy a las {ultimo_dato['Hora']}</div>", unsafe_allow_html=True)
    
    es_lluvia = "Lluvia" in ultimo_dato['Condición']
    clase_tarjeta_condicion = "card-alert" if es_lluvia else "card-normal"
    clase_texto_condicion = "alert-text" if es_lluvia else "normal-text"
    icono_condicion = "⚠️" if es_lluvia else "✅"
    
    st.markdown(f"""
    <div class="card-container">
        <div class="ux-card {clase_tarjeta_condicion}">
            <span class="ux-icon">{icono_condicion}</span>
            <span class="ux-label">Estado</span>
            <div class="ux-value {clase_texto_condicion}">{ultimo_dato['Condición'].capitalize()}</div>
        </div>
        <div class="ux-card card-temp">
            <span class="ux-icon">🌡️</span>
            <span class="ux-label">Temperatura</span>
            <div class="ux-value">{ultimo_dato['Temperatura (°C)']}°C</div>
        </div>
        <div class="ux-card card-hum">
            <span class="ux-icon">💧</span>
            <span class="ux-label">Humedad</span>
            <div class="ux-value">{ultimo_dato['Humedad (%)']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN: RECOMENDACIONES DINÁMICAS ---
    if es_lluvia:
        st.markdown("""
        <div style="background-color: rgba(255, 215, 0, 0.08); border-left: 4px solid #FFD700; padding: 15px; border-radius: 6px; margin-bottom: 25px;">
            <h4 style="color: #FFD700; margin-top: 0; font-size: 1.1rem;">⚠️ Directivas de Defensa Civil</h4>
            <p style="margin-bottom: 0; color: #E0E0E0; font-size: 0.95rem; line-height: 1.5;">
            • Evite cruzar quebradas, ríos o badenes con caudal incrementado.<br>
            • Asegure los techos de calamina de su vivienda.<br>
            • Aléjese de laderas inestables o trochas con riesgo de deslizamientos.<br>
            • En caso de emergencia, comuníquese de inmediato con las autoridades locales.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: rgba(0, 229, 255, 0.05); border-left: 4px solid #00E5FF; padding: 15px; border-radius: 6px; margin-bottom: 25px;">
            <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.1rem;">✅ Condiciones Estables</h4>
            <p style="margin-bottom: 0; color: #E0E0E0; font-size: 0.95rem; line-height: 1.5;">
            Las vías y trochas carrozables del distrito se encuentran en condiciones normales. Manténgase hidratado y proteja a los niños y adultos mayores de los cambios bruscos de temperatura propios de la sierra piurana.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 5. GRÁFICO
    st.markdown("<h4 style='color: #E0E0E0; font-weight: 600; font-size: 1.1rem; margin-bottom: 0;'>📊 Comportamiento de la Temperatura</h4>", unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Timestamp'], 
        y=df['Temperatura (°C)'],
        mode='lines+markers',
        line=dict(color='#3399FF', width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(51, 153, 255, 0.1)',
        marker=dict(size=6, color='#0E1117', line=dict(color='#3399FF', width=2)),
        hovertemplate='%{y:.1f}°C<br>%{x|%H:%M}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        xaxis=dict(showgrid=False, zeroline=False, tickformat='%H:%M', tickfont=dict(color='#8B949E')),
        yaxis=dict(showgrid=True, gridcolor='#21262D', zeroline=False, tickfont=dict(color='#8B949E')),
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # --- SECCIÓN: DIRECTORIO DE EMERGENCIAS ---
    st.markdown("<br><h4 style='color: #E0E0E0; font-weight: 600; font-size: 1.1rem; border-top: 1px solid #30363D; padding-top: 15px; margin-bottom: 15px;'>📞 Directorio Rápido de Emergencias</h4>", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("<div class='contacto-card'>🚑 <b>Centro de Salud</b><br><span style='color:#8B949E; font-size: 0.8rem;'>Atención 24h</span><br><span style='color:#00E5FF; font-weight: bold;'>[955969319]</span></div>", unsafe_allow_html=True)
    with colB:
        st.markdown("<div class='contacto-card'>🚓 <b>Comisaría PNP</b><br><span style='color:#8B949E; font-size: 0.8rem;'>Apoyo y Rescate</span><br><span style='color:#00E5FF; font-weight: bold;'>[968732294]</span></div>", unsafe_allow_html=True)
    with colC:
        st.markdown("<div class='contacto-card'>🛡️ <b>Defensa Civil</b><br><span style='color:#8B949E; font-size: 0.8rem;'>Municipalidad</span><br><span style='color:#00E5FF; font-weight: bold;'>[928253019]</span></div>", unsafe_allow_html=True)

else:
    st.info("Sincronizando con la estación meteorológica...")