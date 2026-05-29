import requests
import json
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from estadisticas import exportar_stats_a_xlsx


def main():
    headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://tracker.gg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    }
    
    # Crear carpeta para los stats si no existe
    carpeta = 'stats'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Leer los nombres del archivo
    try:
        with open('nombres.txt', 'r') as f:
            nombres = f.read().strip().split('\n')
    except FileNotFoundError:
        print("Error: No se encontró el archivo nombres.txt")
        return
    
    # Iterar sobre cada nombre
    for nombre_completo in nombres:
        nombre_completo = nombre_completo.strip()
        if not nombre_completo:
            continue
        
        # Extraer nombre e id
        partes = nombre_completo.split('#')
        nombre = partes[0].strip()
        
        # Construir la URL con encoding
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}'
        
        print(f"\nObteniendo datos de {nombre}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Buscar el ACT actual competitivo
                if 'data' in data and 'segments' in data['data']:
                    acto_actual = None
                    stats_v26 = None
                    
                    # Buscar el segment de tipo "season" y competitivo más reciente
                    for segment in data['data']['segments']:
                        if (segment.get('type') == 'season' and 
                            segment.get('metadata', {}).get('playlist') == 'competitive'):
                            acto_actual = segment['metadata']['name']
                            stats_v26 = segment['stats']
                            break
                    
                    if acto_actual and stats_v26:
                        # Extraer solo los datos principales
                        datos_principales = {
                            'Jugador': nombre,
                            'Acto': acto_actual,
                            'Damage/Round': stats_v26.get('damagePerRound', {}).get('displayValue'),
                            'K/D Ratio': stats_v26.get('kDRatio', {}).get('displayValue'),
                            'Headshot %': stats_v26.get('headshotsPercentage', {}).get('displayValue'),
                            'Win %': stats_v26.get('matchesWinPct', {}).get('displayValue'),
                            'Wins': stats_v26.get('matchesWon', {}).get('displayValue'),
                            'KAST': stats_v26.get('kAST', {}).get('displayValue'),
                            'DDA/Round': stats_v26.get('damageDeltaPerRound', {}).get('displayValue'),
                            'Kills': stats_v26.get('kills', {}).get('displayValue'),
                            'Deaths': stats_v26.get('deaths', {}).get('displayValue'),
                            'Assists': stats_v26.get('assists', {}).get('displayValue'),
                            'ACS': stats_v26.get('score', {}).get('displayValue'),
                            'KAD Ratio': stats_v26.get('kADRatio', {}).get('displayValue'),
                            'Kills/Round': stats_v26.get('killsPerRound', {}).get('displayValue'),
                            'First Bloods': stats_v26.get('firstBloods', {}).get('displayValue'),
                            'Flawless Rounds': stats_v26.get('flawless', {}).get('displayValue'),
                            'Aces': stats_v26.get('aces', {}).get('displayValue')
                        }
                        
                        # Guardar en un archivo con el nombre de la persona dentro de la carpeta
                        archivo_nombre = os.path.join(carpeta, f"{nombre}.json")
                        with open(archivo_nombre, 'w') as f:
                            json.dump(datos_principales, f, indent=4)
                            print(f"Stats guardados en {archivo_nombre}")
                    else:
                        print(f"No se encontró acto competitivo actual para {nombre}")
                else:
                    print(f"No se encontró la estructura esperada para {nombre}")

            except ValueError:
                print(f"Error al procesar JSON para {nombre}")
        else:
            print(f"Error en la petición para {nombre}. Código de estado: {response.status_code}")
    
    # Exportar todos los stats a XLSX
    print("\n" + "="*50)
    exportar_stats_a_xlsx()

if __name__ == '__main__':
    main()