import streamlit as st
import pandas as pd

# Configuración de la página móvil
st.set_page_config(
    page_title="Dine's Arts Club — Verificación",
    page_icon="🎨",
    layout="centered"
)

# Estilos CSS personalizados para la tarjeta
st.markdown("""
    <style>
    /* Ocultar menús nativos de Streamlit para apariencia limpia */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f8f9fa;
    }
    .card {
        background: white;
        max-width: 380px;
        margin: 10px auto;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #1F4E78;
        margin-bottom: 2px;
        letter-spacing: 0.5px;
    }
    .subtitle {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 18px;
    }
    .member-name {
        font-size: 22px;
        font-weight: 700;
        color: #111;
        margin: 10px 0 2px 0;
    }
    .member-id {
        font-size: 13px;
        color: #666;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        color: white;
        margin-bottom: 15px;
    }
    .info-group {
        text-align: left;
        margin-top: 12px;
        border-top: 1px solid #f0f0f0;
        padding-top: 10px;
    }
    .info-label {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .info-value {
        font-size: 14px;
        font-weight: 600;
        color: #222;
        margin-top: 2px;
    }
    .footer-text {
        margin-top: 20px;
        font-size: 10px;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# Capturar el ID desde la URL (?id=DA-M-0001)
query_params = st.query_params
id_buscado = query_params.get("id", None)

# URL pública de tu Google Sheet expuesta en formato CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Whh-Isp3LKYXrcQ467C51XL78P_oySBm5yxd2BVGClI/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception as e:
        return None

df_members = cargar_datos()

if not id_buscado:
    st.markdown("""
        <div class="card" style="border-top: 5px solid #1F4E78;">
            <div class="brand-title">DINE'S ARTS CLUB</div>
            <div class="subtitle">Verificación Oficial</div>
            <p style="color: #666; margin-top: 20px;">⚠️ Por favor, escanea un código QR válido para verificar la membresía.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    id_buscado = str(id_buscado).strip().upper()
    miembro = None
    
    if df_members is not None:
        # Filtrar por ID
        df_members['ID'] = df_members['ID'].astype(str).str.strip().str.upper()
        resultado = df_members[df_members['ID'] == id_buscado]
        
        if not resultado.empty:
            row = resultado.iloc[0]
            miembro = {
                "id": row.get("ID", id_buscado),
                "nombre": f"{row.get('Nombre', '')} {row.get('Apellido', '')}".strip(),
                "descuento": str(row.get("% Descuento", "0%")),
                "limite_actividad": str(row.get("Fecha límite de actividad", "-")),
                "fin_anual": str(row.get("Fin de membresía anual", "-")),
                "estado": str(row.get("Estado", "INACTIVA")).upper()
            }

    if not miembro:
        st.markdown(f"""
            <div class="card" style="border-top: 5px solid #dc3545;">
                <div class="brand-title">DINE'S ARTS CLUB</div>
                <div class="subtitle">Verificación Oficial</div>
                <p style="color: #dc3545; font-weight: bold; margin-top: 20px;">❌ Miembro No Encontrado</p>
                <p style="color: #777; font-size: 13px;">El ID <b>{id_buscado}</b> no está registrado en el sistema.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Determinar colores e iconos según el Estado
        color_map = {
            "ACTIVA": {"bg": "#28a745", "icon": "🟢", "msg": "MEMBRESÍA ACTIVA"},
            "POR VENCER": {"bg": "#ffc107", "icon": "🟡", "msg": "MEMBRESÍA POR VENCER"},
            "INACTIVA": {"bg": "#dc3545", "icon": "🔴", "msg": "MEMBRESÍA INACTIVA"},
            "VENCIDA": {"bg": "#6c757d", "icon": "⚫", "msg": "MEMBRESÍA ANUAL VENCIDA"}
        }
        
        estado_info = color_map.get(miembro["estado"], {"bg": "#dc3545", "icon": "🔴", "msg": "ESTADO DESCONOCIDO"})

        # Renderizar la tarjeta
        st.markdown(f"""
            <div class="card" style="border-top: 6px solid {estado_info['bg']};">
                <div class="brand-title">DINE'S ARTS CLUB</div>
                <div class="subtitle">Verificación Oficial</div>
                
                <div class="member-name">{miembro['nombre']}</div>
                <div class="member-id">ID: {miembro['id']}</div>
                
                <div class="badge" style="background-color: {estado_info['bg']};">
                    {estado_info['icon']} {estado_info['msg']}
                </div>
                
                <div class="info-group">
                    <div class="info-label">Descuento Autorizado</div>
                    <div class="info-value">{miembro['descuento']}</div>
                </div>
                
                <div class="info-group">
                    <div class="info-label">Límite de Actividad Trimestral</div>
                    <div class="info-value">{miembro['limite_actividad']}</div>
                </div>
                
                <div class="info-group">
                    <div class="info-label">Vencimiento Membresía Anual</div>
                    <div class="info-value">{miembro['fin_anual']}</div>
                </div>
                
                <div class="footer-text">Sistema de Control de Membresías — Dine's Arts</div>
            </div>
        """, unsafe_allow_html=True)
