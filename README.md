# 📊 Valorant Stats Automation

Una herramienta para automatizar la recopilación y análisis de estadísticas de Valorant de múltiples jugadores.

## 📋 Requisitos

### Instalación de dependencias

Antes de ejecutar el script, instala las siguientes librerías de Python:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### Archivos requeridos

- `nombres.txt` - Archivo de texto con los IDs de Valorant (formato: `Nombre#ID`)

**Ejemplo de `nombres.txt`:**
```
Lord Bane#Sith
Jokker898#LAN
Lord Bane#P4DME
```

## 🚀 Cómo usar

### Paso 1: Preparar los nombres
Edita el archivo `nombres.txt` y agrega los jugadores que deseas monitorear en formato `Nombre#ID`.

### Paso 2: Ejecutar el script
```bash
python main.py
```

El script:
1. Lee los nombres del archivo `nombres.txt`
2. Hace una petición a la API de Valorant Tracker para cada jugador
3. Extrae las estadísticas de **V26: ACT III Competitive**
4. Guarda un JSON individual para cada jugador en la carpeta `stats/`
5. Genera un archivo `estadisticas.xlsx` con todas las estadísticas consolidadas

## 📁 Estructura de carpetas generada

```
Automation/
├── main.py
├── estadisticas.py
├── nombres.txt
├── estadisticas.xlsx
└── stats/
    ├── Quesitoo.json
    ├── Nabi.json
    ├── Arrocito salado.json
    └── ... (un JSON por jugador)
```

## 📄 Contenido de cada JSON

Cada archivo JSON en la carpeta `stats/` contiene las siguientes estadísticas del jugador:

```json
{
  "Jugador": "Nombre del jugador",
  "Damage/Round": "145.6",
  "K/D Ratio": "1.09",
  "Headshot %": "35.1%",
  "KAST": "73.0%",
  "ACS": "214.7",
  "KAD Ratio": "1.49",
}
```

### Descripción de estadísticas:
- **Damage/Round**: Daño promedio por ronda
- **K/D Ratio**: Proporción de asesinatos / muertes
- **Headshot %**: Porcentaje de asesinatos con headshot
- **KAST**: Porcentaje de rondas con Kill, Assist, Survival o Trade
- **ACS**: Average Combat Score (puntuación promedio de combate)
- **KAD Ratio**: Proporción de (Kills + Assists) / Deaths

## 📊 Contenido del archivo XLSX (`estadisticas.xlsx`)

### Características principales:

1. **Consolidación de datos**
   - Todas las estadísticas de todos los jugadores en un solo archivo
   - Una fila por jugador por ejecución del script

2. **Historial por fecha**
   - Columna `Fecha` que registra cuándo se ejecutó la recopilación
   - Los datos se acumulan sin sobrescribirse
   - Permite ver la evolución en el tiempo

3. **Análisis de rendimiento**
   - Columnas adicionales `{Stat}_Cambio` para cada estadística
   - Compara el rendimiento actual con la ejecución anterior
   - **Color verde**: Mejora de rendimiento
   - **Color rojo**: Bajón de rendimiento
   - **Color gris**: Sin cambios

4. **Diseño visual**
   - Encabezados en **azul oscuro**
   - Nombres de jugadores en **naranja claro**
   - Fechas en **verde claro**
   - Otras estadísticas en **azul medio claro**
   - Encabezados congelados para fácil desplazamiento

### Ejemplo de estructura del XLSX:

| Jugador | Fecha | Damage/Round | K/D Ratio | ... | Damage/Round_Cambio | K/D Ratio_Cambio | ... |
|---------|-------|--------------|-----------|-----|---------------------|------------------|-----|
| Lord Bane | 2026-05-28 10:30:00 | 145.6 | 1.09 | ... | | | |
| Jokker898 | 2026-05-28 10:30:00 | 142.3 | 1.15 | ... | | | |

## 🔄 Ejecución periódica

Para monitorear el progreso de tus compañeros en el tiempo, ejecuta el script regularmente:
- **Diariamente** para ver cambios día a día
- **Semanalmente** para análisis de rendimiento
- Los datos se acumularán automáticamente en el Excel

## 📝 Notas

- La API utilizada es `https://api.tracker.gg/` (Tracker.gg)
- Extrae estadísticas del acto mas reciente
- Si un jugador no existe o no tiene datos disponibles, aparecerá un error en la consola
- Los JSONs se guardan con el nombre del jugador (sin el ID)

## 🐛 Troubleshooting

### Error "No se encontró el archivo nombres.txt"
- Asegúrate de que el archivo `nombres.txt` existe en la misma carpeta que `main.py`

### Error de conexión a la API
- Verifica tu conexión a internet
- La API de Tracker.gg podría estar temporalmente no disponible

### El Excel no se genera
- Asegúrate de que `openpyxl` está instalado: `pip install openpyxl`
- Verifica que tengas permisos de escritura en la carpeta

---

**¡Listo!** Ya sabes cómo usar la herramienta. 🎮📈
