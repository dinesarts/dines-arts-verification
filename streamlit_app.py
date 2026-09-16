if df_members is not None:
    # Limpiar espacios invisibles en los nombres de las columnas
    df_members.columns = df_members.columns.str.strip()
    
    # Verificar si la columna ID existe
    if 'ID' in df_members.columns:
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
