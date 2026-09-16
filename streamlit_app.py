import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración básica de la página
st.set_page_config(
    page_title="Dine's Arts Club - Verificación",
    page_icon="🎨",
    layout="centered"
)

# Enlace CSV directo a la pestaña MEMBERS (gid=0)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yUYGtwk4GhyQ7fTkeUFvl4g87xtMmI_X2Fr2OudHWDw/export?format=csv&gid=0"

@st.cache_data(ttl=15)
def load_data():
    try:
        # Cargar ignorando la Fila 1 si está vacía o es título, usando la Fila 2 como encabezado (header=1)
        df = pd.read_csv(SHEET_CSV_URL, header=1)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

df_members = load_data()

# Leer ID desde la URL (?id=DA-M-0001)
query_params = st.query_params
target_id = query_params.get("id", None)

if df_members is not None:
    if 'ID' not in df_members.columns:
        st.error("No se encontró la columna 'ID'. Revisa que la fila 2 contenga los nombres de los encabezados.")
    elif not target_id:
        st.info("⚠️ Por favor, escanea un código QR válido para verificar la membresía.")
    else:
        # Normalizar ID
        df_members['ID_CLEAN'] = df_members['ID'].astype(str).str.strip().str.upper()
        search_id = str(target_id).strip().upper()
        
        member_data = df_members[df_members['ID_CLEAN'] == search_id]
        
        if member_data.empty:
            st.error(f"❌ Miembro no encontrado con el ID: {search_id}")
        else:
            row = member_data.iloc[0]
            
            # Datos principales
            nombre_completo = f"{row.get('Nombre', '')} {row.get('Apellido', '')}".strip()
            estado = str(row.get('Estado', 'INACTIVA')).strip().upper()
            
            # Descuento
            desc_val = row.get('% Descuento', row.get('Descuento', '0%'))
            if pd.notna(desc_val):
                try:
                    num_desc = float(str(desc_val).replace('%', '').strip())
                    descuento = f"{int(num_desc * 100)}%" if num_desc < 1 else f"{int(num_desc)}%"
                except:
                    descuento = str(desc_val)
            else:
                descuento = "0%"

            # Fechas
            limite_actividad = str(row.get('Fecha límite de actividad', '-'))
            fin_anual = str(row.get('Fin de membresía anual', '-'))

            # Configurar diseño según el Estado
            if estado == "ACTIVA":
                color_estado = "#28a745"
                icono = "🟢"
                mensaje_estado = "MEMBRESÍA ACTIVA"
            elif estado == "POR VENCER":
                color_estado = "#ffc107"
                icono = "🟡"
                mensaje_estado = "MEMBRESÍA POR VENCER"
            elif estado == "INACTIVA":
                color_estado = "#dc3545"
                icono = "🔴"
                mensaje_estado = "MEMBRESÍA INACTIVA"
            elif estado == "VENCIDA":
                color_estado = "#6c757d"
                icono = "⚫"
                mensaje_estado = "MEMBRESÍA ANUAL VENCIDA"
            else:
                color_estado = "#17a2b8"
                icono = "🔵"
                mensaje_estado = f"ESTADO: {estado}"

            # HTML y CSS idénticos al diseño visual de la muestra
            html_content = f"""
            <style>
                #MainMenu {{visibility: hidden;}}
                footer {{visibility: hidden;}}
                header {{visibility: hidden;}}
                .stApp {{ background-color: #f4f6f8; }}
                .card {{
                    background: white;
                    max-width: 400px;
                    margin: 10px auto;
                    padding: 25px;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
                    border-top: 6px solid {color_estado};
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                }}
                .brand-title {{ color: #1a3b5d; font-size: 20px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2px; text-transform: uppercase; }}
                .brand-subtitle {{ color: #7f8c8d; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px; }}
                .member-name {{ color: #111111; font-size: 24px; font-weight: 700; margin-bottom: 2px; }}
                .member-id {{ color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }}
                .badge {{
                    display: inline-block;
                    background-color: {color_estado};
                    color: white;
                    padding: 8px 22px;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.5px;
                    margin-bottom: 20px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
                }}
                .info-group {{ text-align: left; padding: 12px 0; border-top: 1px solid #eaeaea; }}
                .info-label {{ color: #8c98a4; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
                .info-value {{ color: #212529; font-size: 14px; font-weight: 600; }}
                .card-footer {{ margin-top: 25px; color: #adb5bd; font-size: 11px; text-align: center; }}
            </style>

            <div class="card">
                <div class="brand-title">Dine's Arts Club</div>
                <div class="brand-subtitle">Verificación Oficial</div>
                
                <div class="member-name">{nombre_completo}</div>
                <div class="member-id">ID: {search_id}</div>
                
                <div>
                    <span class="badge">{icono} {mensaje_estado}</span>
                </div>
                
                <div class="info-group">
                    <div class="info-label">Descuento Autorizado:</div>
                    <div class="info-value">{descuento}</div>
                </div>
                
                <div class="info-group">
                    <div class="info-label">Límite de Actividad Trimestral:</div>
                    <div class="info-value">{limite_actividad}</div>
                </div>

                <div class="info-group">
                    <div class="info-label">Vencimiento Membresía Anual:</div>
                    <div class="info-value">{fin_anual}</div>
                </div>
                
                <div class="card-footer">
                    Sistema de Control de Membresías — Dine's Arts
                </div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
