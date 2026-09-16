import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="Dine's Arts Club - Verificación",
    page_icon="🟢",
    layout="centered"
)

# Estilos CSS personalizados para replicar el diseño exacto de la imagen
st.markdown("""
    <style>
        /* Ocultar elementos predeterminados de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Fondo general */
        .stApp {
            background-color: #f4f6f8;
        }

        /* Contenedor tipo Tarjeta */
        .card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 30px 25px;
            max-width: 450px;
            margin: 20px auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            border-top: 6px solid #1e7e34;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
        }

        .brand-title {
            color: #1a3b5d;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
            text-transform: uppercase;
        }

        .brand-subtitle {
            color: #7f8c8d;
            font-size: 11px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .member-name {
            color: #111111;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 2px;
        }

        .member-id {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 20px;
        }

        /* Badge de Estado */
        .status-badge-active {
            background-color: #28a745;
            color: white;
            font-weight: 700;
            padding: 8px 22px;
            border-radius: 20px;
            display: inline-block;
            font-size: 14px;
            letter-spacing: 0.5px;
            margin-bottom: 25px;
            box-shadow: 0 3px 8px rgba(40, 167, 69, 0.3);
        }

        .status-badge-inactive {
            background-color: #dc3545;
            color: white;
            font-weight: 700;
            padding: 8px 22px;
            border-radius: 20px;
            display: inline-block;
            font-size: 14px;
            letter-spacing: 0.5px;
            margin-bottom: 25px;
            box-shadow: 0 3px 8px rgba(220, 53, 69, 0.3);
        }

        /* Secciones de Información */
        .info-group {
            text-align: left;
            padding: 12px 0;
            border-top: 1px solid #eaeaea;
        }

        .info-label {
            color: #8c98a4;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .info-value {
            color: #212529;
            font-size: 14px;
            font-weight: 600;
        }

        .card-footer {
            margin-top: 25px;
            color: #adb5bd;
            font-size: 11px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# URL del CSV de Google Sheets (Reemplaza esta URL con la tuya con el gid correcto)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yUYGtwk4GhyQ7fTkeUFvl4g87xtMmI_X2Fr2OudHWDw/export?format=csv&gid=0"
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Limpiar espacios en blanco al inicio o final de los nombres de las columnas
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

df_members = load_data()

# Obtener ID desde los parámetros de la URL (?id=DA-M-0001)
query_params = st.query_params
target_id = query_params.get("id", None)

if df_members is not None:
    # Verificar si existe la columna ID
    if 'ID' not in df_members.columns:
        st.error("No se encontró la columna 'ID' en la hoja de datos. Verifica que el enlace CSV apunte a la pestaña 'MEMBERS'.")
        st.write("Columnas detectadas:", list(df_members.columns))
    elif not target_id:
        st.info("Por favor, escanea un código QR válido o especifica un ID en la URL.")
    else:
        # Normalizar la columna ID y la búsqueda
        df_members['ID_CLEAN'] = df_members['ID'].astype(str).str.strip().str.upper()
        search_id = str(target_id).strip().upper()
        
        member_data = df_members[df_members['ID_CLEAN'] == search_id]
        
        if member_data.empty:
            st.warning(f"No se encontró ningún miembro registrado con el ID: {target_id}")
        else:
            row = member_data.iloc[0]
            
            # Obtener variables con valores por defecto si no existen
            nombre = f"{row.get('Nombre', '')} {row.get('Apellido', '')}".strip()
            if not nombre:
                nombre = row.get('Nombre', 'Socio Registrado')
                
            estado = str(row.get('Estado', 'INACTIVA')).strip().upper()
            descuento = row.get('Descuento', 'N/A')
            
            # Ajusta estos nombres según los encabezados exactos de tus fechas en Sheets
            limite_actividad = row.get('Fecha Limite', row.get('Próxima Fecha Límite', 'N/A'))
            vencimiento_anual = row.get('Fecha Vencimiento', row.get('Membresía Válida Hasta', 'N/A'))
            
            is_active = estado == "ACTIVA"
            badge_class = "status-badge-active" if is_active else "status-badge-inactive"
            badge_icon = "🟢" if is_active else "🔴"

            # Renderizado de la tarjeta en HTML
            card_html = f"""
            <div class="card">
                <div class="brand-title">Dine's Arts Club</div>
                <div class="brand-subtitle">Verificación Oficial</div>
                
                <div class="member-name">{nombre}</div>
                <div class="member-id">ID: {search_id}</div>
                
                <div>
                    <span class="{badge_class}">{badge_icon} MEMBRESÍA {estado}</span>
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
                    <div class="info-value">{vencimiento_anual}</div>
                </div>
                
                <div class="card-footer">
                    Sistema de Control de Membresías — Dine's Arts
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
