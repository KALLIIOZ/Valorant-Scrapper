import requests
import json
import os
from urllib.parse import quote


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
    carpeta = 'stats_premier'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Leer nombres desde nombres.txt
    try:
        with open('nombres.txt', 'r') as f:
            nombres = f.read().strip().split('\n')
    except FileNotFoundError:
        print("Error: No se encontró nombres.txt")
        return
    
    print("Obteniendo estadísticas de Premier...\n")
    
    for nombre_completo in nombres:
        nombre_completo = nombre_completo.strip()
        if not nombre_completo:
            continue
        
        # Extraer nombre del jugador (parte antes del #)
        jugador = nombre_completo.split('#')[0]
        
        print(f"Obteniendo datos de {jugador}...")
        
        # Hacer petición a /segments/season
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}/segments/season'
        
        params = {
            'playlist': 'premier',
            'seasonId': 'ce2783e8-44fc-dd48-3da3-33b5ba6c4a22',
            'source': 'web',
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # data es un array, no un dict
                if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                    segment = data['data'][0]
                    
                    # Las stats están dentro del objeto del segment
                    if 'stats' in segment:
                        stats_premier = segment['stats']
                    else:
                        print(f"  ⚠ {jugador} - No tiene stats en segment")
                        continue
                    
                    # Extraer las mismas stats que en Competitivo
                    datos_principales = {
                        'Jugador': jugador,
                        'Damage/Round': stats_premier.get('damagePerRound', {}).get('displayValue'),
                        'K/D Ratio': stats_premier.get('kDRatio', {}).get('displayValue'),
                        'Headshot %': stats_premier.get('headshotsPercentage', {}).get('displayValue'),
                        'Win %': stats_premier.get('matchesWinPct', {}).get('displayValue'),
                        'Wins': stats_premier.get('matchesWon', {}).get('displayValue'),
                        'KAST': stats_premier.get('kAST', {}).get('displayValue'),
                        'DDA/Round': stats_premier.get('damageDeltaPerRound', {}).get('displayValue'),
                        'Kills': stats_premier.get('kills', {}).get('displayValue'),
                        'Deaths': stats_premier.get('deaths', {}).get('displayValue'),
                        'Assists': stats_premier.get('assists', {}).get('displayValue'),
                        'ACS': stats_premier.get('score', {}).get('displayValue'),
                        'KAD Ratio': stats_premier.get('kADRatio', {}).get('displayValue'),
                        'Kills/Round': stats_premier.get('killsPerRound', {}).get('displayValue'),
                        'First Bloods': stats_premier.get('firstBloods', {}).get('displayValue'),
                        'Flawless Rounds': stats_premier.get('flawless', {}).get('displayValue'),
                        'Aces': stats_premier.get('aces', {}).get('displayValue')
                    }
                    
                    # Guardar JSON
                    archivo_nombre = os.path.join(carpeta, f"{jugador}.json")
                    with open(archivo_nombre, 'w') as f:
                        json.dump(datos_principales, f, indent=4)
                    
                    print(f"  ✓ {jugador}")
            
            except Exception as e:
                print(f"  ✗ {jugador} - Error: {e}")
        else:
            print(f"  ✗ {jugador} - Error {response.status_code}")


if __name__ == '__main__':
    main()