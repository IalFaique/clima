import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# 1. Configuración de página ancha
st.set_page_config(page_title="Alerta Temprana | El Faique", layout="wide", page_icon="🏛️")

# --- MOTOR DE ADAPTACIÓN PARA EL FONDO BASE DE STREAMLIT ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    iframe { border: none !important; }
    
    /* Adaptación automática del fondo exterior según el dispositivo */
    @media (prefers-color-scheme: light) { .stApp { background-color: #ffffff !important; } }
    @media (prefers-color-scheme: dark) { .stApp { background-color: #0a0e1a !important; } }
</style>
""", unsafe_allow_html=True)

# 2. Lógica de lectura de datos (Del CSV a Python)
try:
    df = pd.read_csv("historial_clima.csv")
    ultimos_datos = df.tail(24)
    if 'Hora' in ultimos_datos.columns:
        labels = ultimos_datos['Hora'].tolist()
    else:
        labels = ultimos_datos['Fecha y Hora'].apply(lambda x: str(x).split(' ')[-1]).tolist()
    temps = ultimos_datos['Temperatura (°C)'].tolist()
    hums = ultimos_datos['Humedad (%)'].tolist()
    condicion_actual = str(ultimos_datos['Condición'].iloc[-1]).lower() if 'Condición' in df.columns else str(ultimos_datos['Estado'].iloc[-1]).lower()
    is_rain = "true" if "lluvia" in condicion_actual else "false"
except Exception as e:
    labels = ["08:00", "09:00", "10:00", "11:00", "12:00"]
    temps = [20.1, 21.0, 22.5, 23.1, 22.8]
    hums = [60, 62, 65, 70, 85]
    is_rain = "true"

js_labels = json.dumps(labels)
js_temps = json.dumps(temps)
js_hums = json.dumps(hums)

# 3. Diseño HTML/JS (Con Motor de Modo Oscuro/Claro Automático)
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alerta Temprana — San Miguel de El Faique</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Sora:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
/* ─── VARIABLES POR DEFECTO (MODO CLARO) ─── */
:root {
  --bg-main: #ffffff;
  --bg-sub: #f8f9fa;
  --text-main: #0a0e1a;
  --text-muted: rgba(10,14,26,0.5);
  --border: rgba(10,14,26,0.1);
  --inst-blue: #1A2980; 
  --accent-teal: #14b8a6; 
  --status-sky: #0ea5e9;
  --status-amber: #f59e0b;
  --status-green: #10b981;
  
  --alert-rain-bg: #fffcf0;
  --alert-rain-text: #856404;
  --alert-norm-bg: #f0faff;
  --alert-norm-text: #0c5460;
}

/* ─── VARIABLES INTELIGENTES (SE ACTIVAN SI EL DISPOSITIVO ESTÁ EN MODO OSCURO) ─── */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-main: #0a0e1a;
    --bg-sub: #111827;
    --text-main: #f9fafb;
    --text-muted: rgba(255,255,255,0.5);
    --border: rgba(255,255,255,0.1);
    --inst-blue: #60a5fa; 
    --accent-teal: #2dd4bf;
    
    --alert-rain-bg: rgba(245, 158, 11, 0.1);
    --alert-rain-text: #fcd34d;
    --alert-norm-bg: rgba(14, 165, 233, 0.1);
    --alert-norm-text: #7dd3fc;
  }
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Sora', sans-serif;
  background: var(--bg-main);
  color: var(--text-main);
  min-height: 100vh;
  overflow-x: hidden;
  transition: background 0.3s, color 0.3s; 
}

.container { max-width: 100%; margin: 0 auto; padding: 2rem 4vw 4rem; background: var(--bg-main); }

.hero { display: flex; gap: 1.5rem; align-items: center; padding: 1rem 0; border-bottom: 2px solid var(--border); margin-bottom: 1rem; }
.hero-escudo img { width: 72px; }
.hero-overline { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.2rem; }
.hero-title { font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 800; color: var(--inst-blue); margin-bottom: 0.1rem; }
.hero-subtitle { font-size: 0.8rem; color: var(--accent-teal); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600;}

.status-bar { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 0; font-size: 0.82rem; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--status-green); flex-shrink: 0; }
.status-text { color: var(--text-main); }

.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; margin-bottom: 1.5rem; }
.metric-item { text-align: center; padding: 1.5rem 1rem; position: relative; }
.metric-item:not(:last-child)::after { content: ''; position: absolute; top: 20%; right: 0; height: 60%; width: 1px; background: var(--border); }
.metric-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.8rem; }
.metric-icon { font-size: 1.6rem; margin-bottom: 0.6rem; display: block; color: var(--accent-teal); }
.metric-value { font-size: 2.2rem; font-weight: 700; line-height: 1; color: var(--text-main); }
.metric-value.lluvia { color: var(--status-amber); }
.metric-value.normal { color: var(--status-sky); }
.metric-value.temp { color: var(--status-sky); }
.metric-value.hum { color: var(--status-green); }
.metric-sub { font-size: 0.7rem; color: var(--text-muted); margin-top: 0.5rem; font-family: 'IBM Plex Mono', monospace; }

.alert-banner { border-radius: 8px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-size: 0.85rem; line-height: 1.65; color: var(--text-main); }
.alert-banner.lluvia { background: var(--alert-rain-bg); border-left: 5px solid var(--status-amber); color: var(--alert-rain-text); }
.alert-banner.normal { background: var(--alert-norm-bg); border-left: 5px solid var(--status-sky); color: var(--alert-norm-text); }
.alert-title { font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }

.chart-section { padding: 1rem 0; margin-bottom: 1rem; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.section-title { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--inst-blue); }
.chart-tabs { display: flex; gap: 0.5rem; }
.chart-tab { font-size: 0.68rem; font-weight: 600; text-transform: uppercase; padding: 0.4rem 0.8rem; border-radius: 20px; border: 1px solid var(--border); cursor: pointer; transition: all 0.2s; font-family: 'IBM Plex Mono', monospace; background: var(--bg-main); color: var(--text-muted); }
.chart-tab.active { background: var(--inst-blue); color: #ffffff; border-color: var(--inst-blue); }
.chart-wrap { position: relative; height: 260px; }

.directory-section { margin-bottom: 1.5rem; }
.directory-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; }
.dir-item { text-align: left; padding: 1.1rem; flex: 1 1 220px; background: var(--bg-sub); border-radius: 8px; cursor: pointer; text-decoration: none; display: flex; align-items: center; gap: 15px; border: 1px solid var(--border); }
.dir-item:hover { background: var(--bg-main); border-color: var(--inst-blue); }
.dir-icon { font-size: 1.6rem; color: var(--accent-teal); }
.dir-name { font-size: 0.85rem; font-weight: 700; color: var(--inst-blue); margin-bottom: 0.1rem; }
.dir-role { font-size: 0.7rem; color: var(--text-muted); margin-bottom: 0.3rem; }
.dir-phone { font-family: 'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 600; color: var(--accent-teal); }

.footer { text-align: center; font-size: 0.7rem; color: var(--text-muted); padding-top: 1rem; border-top: 1px solid var(--border); font-family: 'IBM Plex Mono', monospace; }

@media (max-width: 640px) {
  .metrics-grid { grid-template-columns: 1fr; }
  .hero { flex-direction: column; text-align: center; gap: 1rem;}
  .directory-grid { flex-direction: column; gap: 0.7rem; }
  .metric-value { font-size: 1.8rem; }
  .hero-title { font-size: 1.35rem; }
  .metric-item::after { display: none; }
  .metric-item { border-bottom: 1px solid var(--border); }
  .container { padding: 1rem 1.5rem 3rem; }
}
</style>
</head>
<body>
<div class="container">
  <header class="hero">
    <div class="hero-escudo">
      <img src="https://upload.wikimedia.org/wikipedia/commons/d/d6/Escudo_san_miguel_de_el_faique.png" alt="Escudo de San Miguel de El Faique">
    </div>
    <div>
      <div class="hero-overline">Municipalidad Distrital</div>
      <h1 class="hero-title">San Miguel de El Faique</h1>
      <div class="hero-subtitle">Portal Oficial · Alerta Temprana Meteorológica</div>
    </div>
  </header>
  
  <div class="status-bar">
    <div class="status-dot"></div>
    <span class="status-text">Estación activa —</span>
    <span id="last-update">Actualizado...</span>
    <span style="margin-left:auto; opacity:0.7;">Distrito de San Miguel de El Faique, Piura</span>
  </div>
  
  <div class="metrics-grid">
    <div class="metric-item">
      <div class="metric-label">Estado actual</div>
      <span class="metric-icon" id="estado-icon">☁️</span>
      <div class="metric-value" id="estado-val">—</div>
      <div class="metric-sub" id="estado-sub">Sincronizando...</div>
    </div>
    <div class="metric-item">
      <div class="metric-label">Temperatura local</div>
      <span class="metric-icon">🌡️</span>
      <div class="metric-value temp" id="temp-val">—</div>
      <div class="metric-sub" id="temp-sub">°C — Sierra de Piura</div>
    </div>
    <div class="metric-item">
      <div class="metric-label">Humedad rel.</div>
      <span class="metric-icon">💧</span>
      <div class="metric-value hum" id="hum-val">—</div>
      <div class="metric-sub" id="hum-sub">% — Humedad relativa</div>
    </div>
  </div>
  
  <div class="alert-banner" id="alert-banner">
    <div class="alert-title" id="alert-title">⏳ Sincronizando datos...</div>
    <div id="alert-body">Conectando con la estación meteorológica.</div>
  </div>
  
  <div class="chart-section">
    <div class="section-header">
      <div class="section-title">📊 Comportamiento de las últimas 24h</div>
      <div class="chart-tabs">
        <button class="chart-tab active" onclick="switchChart('temp', this)">Temp.</button>
        <button class="chart-tab" onclick="switchChart('hum', this)">Humedad</button>
      </div>
    </div>
    <div class="chart-wrap">
      <canvas id="mainChart"></canvas>
    </div>
  </div>
  
  <div class="directory-section">
    <div class="section-title" style="margin-bottom:0">📞 Directorio de emergencias</div>
    <div class="directory-grid">
      <a class="dir-item" href="tel:955969319">
        <span class="dir-icon">🚑</span>
        <div>
          <div class="dir-name">Centro de Salud</div>
          <div class="dir-role">Atención 24h</div>
          <div class="dir-phone">955 969 319</div>
        </div>
      </a>
      <a class="dir-item" href="tel:968732294">
        <span class="dir-icon">🚓</span>
        <div>
          <div class="dir-name">Comisaría PNP</div>
          <div class="dir-role">Apoyo y rescate</div>
          <div class="dir-phone">968 732 294</div>
        </div>
      </a>
      <a class="dir-item" href="tel:928253019">
        <span class="dir-icon">🛡️</span>
        <div>
          <div class="dir-name">Defensa Civil</div>
          <div class="dir-role">Municipalidad</div>
          <div class="dir-phone">928 253 019</div>
        </div>
      </a>
    </div>
  </div>
  
  <div class="footer">
    GERENCIA DE DESARROLLO SOCIAL Y SERVICIOS MUNICIPALES · SISTEMA DE ALERTA TEMPRANA v2.0 · PIURA, PERÚ
  </div>
</div>

<script>
const data = {
  labels: /*PY_LABELS*/,
  temps: /*PY_TEMPS*/,
  hums: /*PY_HUMS*/
};
const latestTemp = data.temps[data.temps.length - 1];
const latestHum  = data.hums[data.hums.length - 1];
const isRain     = /*PY_IS_RAIN*/;

function updateCards() {
  const now = new Date();
  document.getElementById('last-update').textContent = 'Hoy a las ' + data.labels[data.labels.length - 1];
  document.getElementById('temp-val').textContent = latestTemp + '°C';
  document.getElementById('hum-val').textContent  = latestHum + '%';

  if (isRain) {
    document.getElementById('estado-icon').textContent = '⚠️';
    document.getElementById('estado-val').textContent  = 'Lluvia';
    document.getElementById('estado-val').className    = 'metric-value lluvia';
    document.getElementById('estado-sub').textContent  = 'Condición de alerta activa';
    
    const banner = document.getElementById('alert-banner');
    banner.className = 'alert-banner lluvia';
    document.getElementById('alert-title').className = 'alert-title lluvia';
    document.getElementById('alert-title').innerHTML = '⚠️ Directivas de Defensa Civil';
    
    document.getElementById('alert-body').innerHTML = `
      <ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; line-height: 1.6;">
        <li>Evite cruzar quebradas o badenes con caudal incrementado.</li>
        <li style="margin-top: 4px;">Asegure techos de calamina y aléjese de laderas inestables o trochas con riesgo de deslizamientos.</li>
        <li style="margin-top: 4px;">Comuníquese de inmediato con las autoridades locales.</li>
      </ul>
    `;
  } else {
    document.getElementById('estado-icon').textContent = '✅';
    document.getElementById('estado-val').textContent  = 'Estable';
    document.getElementById('estado-val').className    = 'metric-value normal';
    document.getElementById('estado-sub').textContent  = 'Condiciones normales';
    
    const banner = document.getElementById('alert-banner');
    banner.className = 'alert-banner normal';
    document.getElementById('alert-title').className = 'alert-title normal';
    document.getElementById('alert-title').innerHTML = '✅ Condiciones Estables';
    
    document.getElementById('alert-body').innerHTML = `
      <ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; line-height: 1.6;">
        <li>Vías y trochas carrozables operando en condiciones normales.</li>
        <li style="margin-top: 4px;">Manténgase hidratado y proteja a niños y adultos mayores ante cambios de temperatura en la sierra piurana.</li>
      </ul>
    `;
  }
}

let chart;

function buildChart() {
  const ctx = document.getElementById('mainChart').getContext('2d');
  const lineBlue = '#0ea5e9'; 
  const gridColor = 'rgba(150, 150, 150, 0.15)'; 
  const textColor = 'rgba(150, 150, 150, 0.6)'; 
  
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Temperatura (°C)', data: data.temps, borderColor: lineBlue,
        borderWidth: 2, pointRadius: 3, pointBackgroundColor: '#ffffff', pointBorderColor: lineBlue,
        pointBorderWidth: 2, tension: 0.4, fill: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: { duration: 600 },
      plugins: { 
          legend: { display: false }, 
          tooltip: { backgroundColor: 'rgba(50, 50, 50, 0.95)', titleColor: '#ffffff', bodyColor: '#ffffff', bodyFont: { family: "'IBM Plex Mono', monospace", size: 13 }, padding: 10, cornerRadius: 8, displayColors: false } 
      },
      scales: {
        x: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: "'IBM Plex Mono', monospace", size: 11 }, maxTicksLimit: 12 }, border: { color: gridColor } },
        y: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: "'IBM Plex Mono', monospace", size: 11 }, maxTicksLimit: 5 }, border: { color: gridColor } }
      }
    }
  });
}

function switchChart(type, btn) {
  document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  const lineBlue = '#0ea5e9';
  const lineGreen = '#10b981';
  
  if (type === 'temp') {
    chart.data.datasets[0].data = data.temps; chart.data.datasets[0].label = 'Temperatura (°C)'; chart.data.datasets[0].borderColor = lineBlue; chart.data.datasets[0].pointBorderColor = lineBlue;
  } else {
    chart.data.datasets[0].data = data.hums; chart.data.datasets[0].label = 'Humedad (%)'; chart.data.datasets[0].borderColor = lineGreen; chart.data.datasets[0].pointBorderColor = lineGreen;
  }
  chart.update();
}

updateCards();
buildChart();
</script>
</body>
</html>
"""

html_final = html_code.replace("/*PY_LABELS*/", js_labels)
html_final = html_final.replace("/*PY_TEMPS*/", js_temps)
html_final = html_final.replace("/*PY_HUMS*/", js_hums)
html_final = html_final.replace("/*PY_IS_RAIN*/", is_rain)

# Renderizado final a 1400px
components.html(html_final, height=2200, scrolling=False)
