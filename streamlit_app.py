import streamlit as st
import pandas as pd

# Configuración de la página
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

            # Configurar colores e íconos según Estado
            if estado == "ACTIVA":
                color_estado = "#2e7d32"
                icono = "🟢"
                mensaje_estado = "MEMBRESÍA ACTIVA"
            elif estado == "POR VENCER":
                color_estado = "#d97706"
                icono = "🟡"
                mensaje_estado = "MEMBRESÍA POR VENCER"
            elif estado == "INACTIVA":
                color_estado = "#c62828"
                icono = "🔴"
                mensaje_estado = "MEMBRESÍA INACTIVA"
            elif estado == "VENCIDA":
                color_estado = "#616161"
                icono = "⚫"
                mensaje_estado = "MEMBRESÍA ANUAL VENCIDA"
            else:
                color_estado = "#1565c0"
                icono = "🔵"
                mensaje_estado = f"ESTADO: {estado}"

            # Estilos con la identidad de marca Dine's Arts
            css_styles = f"""
            <style>
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            .stApp {{ background-color: #f7efe9; }}
            .card {{
                background: #ffffff;
                max-width: 380px;
                margin: 0 auto;
                padding: 28px 24px;
                border-radius: 20px;
                box-shadow: 0 12px 28px rgba(43, 20, 8, 0.08);
                border-top: 6px solid #c15428;
                font-family: 'Segoe UI', Georgia, serif;
                text-align: center;
            }}
            .brand-title {{ color: #2b1408; font-size: 22px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2px; text-transform: uppercase; }}
            .brand-subtitle {{ color: #856859; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px; font-style: italic; }}
            .member-name {{ color: #2b1408; font-size: 24px; font-weight: 700; margin-bottom: 2px; font-family: 'Georgia', serif; }}
            .member-id {{ color: #c15428; font-size: 14px; font-weight: 700; margin-bottom: 18px; }}
            .badge {{
                display: inline-block;
                background-color: {color_estado};
                color: white;
                padding: 7px 20px;
                border-radius: 20px;
                font-weight: 700;
                font-size: 13px;
                letter-spacing: 0.5px;
                margin-bottom: 20px;
            }}
            .info-group {{ text-align: left; padding: 12px 0; border-top: 1px solid #f2e6dd; }}
            .info-label {{ color: #856859; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 3px; }}
            .info-value {{ color: #2b1408; font-size: 15px; font-weight: 600; }}
            .card-footer {{ margin-top: 22px; color: #856859; font-size: 12px; text-align: center; font-style: italic; }}
            </style>
            """
            st.html(css_styles)

            # Estructura de la tarjeta visual
            card_html = f"""
            <div class="card">
                <div class="brand-title">Dine's Arts Club</div>
                <div class="brand-subtitle">Centro de Formación Culinaria</div>
                
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
                    
                    <div class="card-footer">
                   Aprende, Crea y Disfruta
                </div>
            </div>
            """
            st.html(card_html)
