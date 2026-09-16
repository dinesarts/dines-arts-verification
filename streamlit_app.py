import streamlit as st
import pandas as pd

# Configuración básica de la página
st.set_page_config(
    page_title="Dine's Arts Club - Verificación",
    page_icon="🧁",
    layout="centered"
)

# Enlace CSV con exportación directa de la pestaña MEMBERS (gid=0)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yUYGtwk4GhyQ7fTkeUFvl4g87xtMmI_X2Fr2OudHWDw/export?format=csv&gid=0"

@st.cache_data(ttl=30)
def load_data():
    try:
        # Cargar CSV sin encabezados automáticos para guiarnos por índice exacto de columna
        df = pd.read_csv(SHEET_CSV_URL, header=None, skiprows=1)
        return df
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

df_raw = load_data()

# Leer el ID desde la URL (?id=DA-M-0001)
query_params = st.query_params
target_id = query_params.get("id", None)

if df_raw is not None:
    if not target_id:
        st.info("⚠️ Por favor, escanea un código QR válido.")
    else:
        # Columna 0 es la Columna A (ID)
        df_raw[0] = df_raw[0].astype(str).str.strip().str.upper()
        search_id = str(target_id).strip().upper()
        
        # Buscar la fila correspondiente
        member_row = df_raw[df_raw[0] == search_id]
        
        if member_row.empty:
            st.error("❌ Miembro no encontrado.")
        else:
            row = member_row.iloc[0]
            
            # Mapeo idéntico a tu función Apps Script
            id_miembro = row[0]
            nombre_completo = f"{row[1]} {row[2]}".strip()
            limite_actividad = row[8] if pd.notna(row[8]) else "-"
            fin_anual = row[9] if pd.notna(row[9]) else "-"
            
            # Formato de Descuento
            descuento_raw = row[11] if pd.notna(row[11]) else 0
            try:
                descuento_val = float(str(descuento_raw).replace('%', ''))
                descuento = f"{int(descuento_val * 100)}%" if descuento_val < 1 else f"{int(descuento_val)}%"
            except:
                descuento = str(descuento_raw)
                
            estado = str(row[12]).strip().upper() if pd.notna(row[12]) else "INACTIVA"

            # Definir colores e íconos según los 4 estados de tu script original
            if estado == "ACTIVA":
                color_estado = "#28a745"
                icono = "🟢"
                mensaje_estado = "MEMBRESÍA ACTIVA"
            elif estado == "INACTIVA":
                color_estado = "#dc3545"
                icono = "🔴"
                mensaje_estado = "MEMBRESÍA INACTIVA (Requiere Reactivación)"
            elif estado == "POR VENCER":
                color_estado = "#ffc107"
                icono = "🟡"
                mensaje_estado = "MEMBRESÍA POR VENCER"
            elif estado == "VENCIDA":
                color_estado = "#6c757d"
                icono = "⚫"
                mensaje_estado = "MEMBRESÍA ANUAL VENCIDA"
            else:
                color_estado = "#6c757d"
                icono = "⚪"
                mensaje_estado = f"ESTADO: {estado}"

            # Estilos CSS y Renderizado HTML
            html_content = f"""
            <style>
                #MainMenu {{visibility: hidden;}}
                footer {{visibility: hidden;}}
                header {{visibility: hidden;}}
                .stApp {{ background-color: #f8f9fa; }}
                .card {{
                    background: white;
                    max-width: 380px;
                    margin: 20px auto;
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border-top: 6px solid {color_estado};
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    color: #333;
                }}
                h1 {{ font-size: 20px; color: #1F4E78; margin-bottom: 5px; margin-top: 0; }}
                .subtitle {{ font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; }}
                .member-name {{ font-size: 22px; font-weight: bold; margin: 10px 0 5px 0; color: #222; }}
                .member-id {{ font-size: 14px; color: #777; margin-bottom: 20px; }}
                .badge {{ display: inline-block; background-color: {color_estado}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 13px; margin-bottom: 20px; }}
                .info-group {{ text-align: left; margin-top: 15px; border-top: 1px solid #eee; padding-top: 12px; font-size: 14px; }}
                .info-label {{ font-size: 11px; color: #888; text-transform: uppercase; }}
                .info-value {{ font-weight: 600; color: #333; margin-top: 2px; }}
                .footer {{ margin-top: 25px; font-size: 11px; color: #aaa; }}
            </style>

            <div class="card">
                <h1>DINE'S ARTS CLUB</h1>
                <div class="subtitle">Verificación Oficial</div>
                
                <div class="member-name">{nombre_completo}</div>
                <div class="member-id">ID: {id_miembro}</div>
                
                <div class="badge">{icono} {mensaje_estado}</div>
                
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
                    <div class="info-value">{finAnual}</div>
                </div>
                
                <div class="footer">Sistema de Control de Membresías — Dine's Arts</div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
