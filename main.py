import requests
import json
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from estadisticas import exportar_stats_a_xlsx
import premier


def main():
    headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://tracker.gg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    }  

    carpeta = 'stats'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    try:
        with open('nombres.txt', 'r') as f:
            nombres = f.read().strip().split('\n')
    except FileNotFoundError:
        print("Error: No se encontró el archivo nombres.txt")
        return
    
    print("\nObteniendo estadísticas...\n")
    for nombre_completo in nombres:
        nombre_completo = nombre_completo.strip()
        if not nombre_completo:
            continue
        
        partes = nombre_completo.split('#')
        nombre = partes[0].strip()
        
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}'
        
        print(f"\nObteniendo datos de {nombre}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                if 'data' in data and 'segments' in data['data']:
                    segments = data['data']['segments']
                    
                    acto_actual = None
                    stats_v26 = None
                    season_id_premier = None
                    
                    # Extraer season_id_premier del metadata principal (data['metadata']['seasons'])
                    if 'metadata' in data['data'] and 'seasons' in data['data']['metadata']:
                        seasons = data['data']['metadata']['seasons']
                        if seasons:
                            season_id_premier = seasons[0].get('id')
                    
                    # Buscar Competitivo en los segments
                    for segment in data['data']['segments']:
                        segment_name = segment.get('metadata', {}).get('name', '')
                        
                        # Competitivo: primer segment de tipo season
                        if segment.get('type') == 'season' and acto_actual is None:
                            acto_actual = segment_name
                            stats_v26 = segment['stats']
                            break
                    
                    if acto_actual and stats_v26:
                        datos_principales = {
                            'Jugador': nombre,
                            'Acto': acto_actual,
                            'SeasonIdPremier': season_id_premier,
                            'Damage/Round': stats_v26.get('damagePerRound', {}).get('displayValue'),
                            'K/D Ratio': stats_v26.get('kDRatio', {}).get('displayValue'),
                            'Headshot %': stats_v26.get('headshotsPercentage', {}).get('displayValue'),
                            'KAST': stats_v26.get('kAST', {}).get('displayValue'),
                            'ACS': stats_v26.get('score', {}).get('displayValue'),
                            'KAD Ratio': stats_v26.get('kADRatio', {}).get('displayValue'),
                        }
                        
                        archivo_nombre = os.path.join(carpeta, f"{nombre}.json")
                        with open(archivo_nombre, 'w') as f:
                            json.dump(datos_principales, f, indent=4)
                            print(f"  ✓ {nombre}")
                    else:
                        print(f"  ⚠ {nombre} - No se encontró el ACT actual")
                else:
                    print(f"  ⚠ {nombre} - Estructura de datos no válida")

            except ValueError:
                print(f"  ✗ {nombre} - Error al procesar JSON")
            except Exception as e:
                print(f"  ✗ {nombre} - {type(e).__name__}")
        else:
            print(f"  ✗ {nombre} - Error {response.status_code}")
    
    # Procesar Premier
    print("\n" + "="*50)
    premier.main()
    
    # Exportar estadísticas combinadas
    print("\n" + "="*50)
    exportar_stats_a_xlsx()

if __name__ == '__main__':
    main()