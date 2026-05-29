import os
import json
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment


def exportar_stats_a_xlsx(carpeta='stats', archivo_salida='estadisticas.xlsx'):
    """
    Lee todos los archivos JSON de la carpeta de stats y los exporta a un archivo XLSX.
    Los datos se organizan por fecha sin sobrescribir información anterior.
    Incluye comparación de rendimiento con respecto a la fecha anterior.
    
    Args:
        carpeta (str): Ruta de la carpeta donde están los JSON
        archivo_salida (str): Nombre del archivo XLSX de salida
    """
    
    # Verificar si la carpeta existe
    if not os.path.exists(carpeta):
        print(f"Error: La carpeta {carpeta} no existe")
        return False
    
    # Leer todos los JSON
    datos = []
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.json'):
            ruta_archivo = os.path.join(carpeta, archivo)
            try:
                with open(ruta_archivo, 'r') as f:
                    contenido = json.load(f)
                    contenido['Fecha'] = fecha_actual
                    datos.append(contenido)
            except Exception as e:
                print(f"Error al leer {archivo}: {e}")
    
    if not datos:
        print("No se encontraron archivos JSON en la carpeta")
        return False
    
    # Convertir a DataFrame
    df_nuevo = pd.DataFrame(datos)
    
    # Columnas numéricas para comparar (excluyendo Jugador y Fecha)
    columnas_numericas = [col for col in df_nuevo.columns 
                         if col not in ['Jugador', 'Fecha'] and col != 'Comparación']
    
    # Si el archivo ya existe, leer los datos anteriores y hacer comparación
    if os.path.exists(archivo_salida):
        try:
            df_existente = pd.read_excel(archivo_salida, sheet_name='Stats')
            
            # Crear columnas de comparación para datos nuevos
            for col in columnas_numericas:
                df_nuevo[f'{col}_Cambio'] = ''
                
                for idx, row in df_nuevo.iterrows():
                    jugador = row['Jugador']
                    valor_nuevo = row[col]
                    
                    # Buscar el registro anterior más reciente de este jugador
                    registros_anteriores = df_existente[df_existente['Jugador'] == jugador]
                    
                    if not registros_anteriores.empty:
                        # Tomar el último registro (más reciente)
                        valor_anterior = registros_anteriores.iloc[-1][col]
                        
                        # Convertir a float para comparación
                        try:
                            valor_nuevo_float = float(str(valor_nuevo).replace('%', ''))
                            valor_anterior_float = float(str(valor_anterior).replace('%', ''))
                            
                            diferencia = valor_nuevo_float - valor_anterior_float
                            
                            # Determinar si es mejora o bajón (considerar que % mayor es mejor, números como K/D también)
                            if diferencia > 0:
                                df_nuevo.at[idx, f'{col}_Cambio'] = f'+{diferencia:.2f}'
                            elif diferencia < 0:
                                df_nuevo.at[idx, f'{col}_Cambio'] = f'{diferencia:.2f}'
                            else:
                                df_nuevo.at[idx, f'{col}_Cambio'] = '0'
                        except:
                            df_nuevo.at[idx, f'{col}_Cambio'] = 'N/A'
                    # Si no hay registro anterior, dejar vacío
            
            # Concatenar datos nuevos con los existentes
            df = pd.concat([df_existente, df_nuevo], ignore_index=True)
            print(f"Datos agregados al archivo existente {archivo_salida}")
        except Exception as e:
            print(f"Error al leer archivo existente: {e}. Creando nuevo archivo...")
            df = df_nuevo
    else:
        # Si es el primer archivo, no hay comparación
        df = df_nuevo
    
    # Exportar a XLSX
    try:
        df.to_excel(archivo_salida, index=False, sheet_name='Stats')
        
        # Aplicar formato condicional
        aplicar_formato_condicional(archivo_salida, df, columnas_numericas)
        
        print(f"Estadísticas exportadas a {archivo_salida}")
        return True
    except Exception as e:
        print(f"Error al exportar a XLSX: {e}")
        return False


def aplicar_formato_condicional(archivo_salida, df, columnas_numericas):
    """
    Aplica formato condicional de colores a las columnas de cambio.
    Rojo para bajón de rendimiento, verde para mejora.
    También embellece el Excel con colores atractivos.
    """
    try:
        wb = load_workbook(archivo_salida)
        ws = wb.active
        
        # Definir colores
        color_header = '4472C4'  # Azul oscuro para encabezados
        color_jugador = 'FFE699'  # Naranja claro
        color_fecha = 'C6EFCE'    # Verde claro
        color_columnas = 'D9E8F5' # Azul medio claro
        
        # Colorear encabezados y datos según columna
        for col_idx, col_name in enumerate(ws[1], 1): # type: ignore
            columna_actual = col_name.value
            
            # Colorear encabezado
            celda_header = ws.cell(row=1, column=col_idx) # type: ignore
            celda_header.fill = PatternFill(start_color=color_header, end_color=color_header, fill_type='solid')
            celda_header.font = Font(bold=True, color='FFFFFF', size=11)
            celda_header.alignment = Alignment(horizontal='center', vertical='center')
            
            # Colorear datos según tipo de columna
            for row_idx in range(2, ws.max_row + 1): # type: ignore
                celda = ws.cell(row=row_idx, column=col_idx) # type: ignore
                
                if columna_actual == 'Jugador':
                    # Naranja claro para nombres
                    celda.fill = PatternFill(start_color=color_jugador, end_color=color_jugador, fill_type='solid')
                    celda.font = Font(bold=True, size=10)
                elif columna_actual == 'Fecha':
                    # Verde claro para fechas
                    celda.fill = PatternFill(start_color=color_fecha, end_color=color_fecha, fill_type='solid')
                    celda.font = Font(size=10)
                elif '_Cambio' in str(columna_actual):
                    # Ya tiene formato condicional de colores rojo/verde
                    valor = celda.value
                    if valor and valor != 'N/A':
                        try:
                            numero = float(str(valor).replace('+', ''))
                            
                            if numero > 0:
                                # Verde para mejora
                                celda.fill = PatternFill(start_color='00B050', end_color='00B050', fill_type='solid')
                                celda.font = Font(bold=True, color='FFFFFF')
                            elif numero < 0:
                                # Rojo para bajón
                                celda.fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
                                celda.font = Font(bold=True, color='FFFFFF')
                            else:
                                # Gris para sin cambios
                                celda.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                                celda.font = Font(bold=True)
                            
                            celda.alignment = Alignment(horizontal='center', vertical='center')
                        except:
                            pass
                else:
                    # Azul medio claro para otras columnas
                    celda.fill = PatternFill(start_color=color_columnas, end_color=color_columnas, fill_type='solid')
                    celda.font = Font(size=10)
                
                # Alinear al centro si no es la columna de nombre
                if columna_actual != 'Jugador':
                    celda.alignment = Alignment(horizontal='center', vertical='center')
                else:
                    celda.alignment = Alignment(horizontal='left', vertical='center')
        
        # Ajustar ancho de columnas
        for column in ws.columns: # type: ignore
            max_length = 0
            column_letter = column[0].column_letter # type: ignore
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width # type: ignore
        
        # Congelar encabezados
        ws.freeze_panes = 'A2' # type: ignore
        
        wb.save(archivo_salida)
        print("Formato embellecido aplicado correctamente")
    except Exception as e:
        print(f"Error al aplicar formato: {e}")
