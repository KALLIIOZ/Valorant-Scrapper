# 📊 Valorant Stats Automation

An automated tool for collecting and analyzing Valorant statistics from multiple players.

## 📋 Requirements

### Installing dependencies

Before running the script, install the following Python libraries:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### Required files

- `nombres.txt` - Text file with Valorant IDs (format: `Name#ID`)

**Example `nombres.txt`:**
```
Lord Bane#Sith
Jokker898#LAN
Lord Bane#P4DME
```

## 🚀 How to use

### Step 1: Prepare player names
Edit the `nombres.txt` file and add the players you want to monitor in the format `Name#ID`.

### Step 2: Run the script
```bash
python main.py
```

The script will:
1. Read player names from `nombres.txt`
2. Make requests to the Valorant Tracker API for each player
3. Extract statistics from the **most recent competitive act**
4. Save individual JSON files for each player in the `stats/` folder
5. Generate an `estadisticas.xlsx` file with all consolidated statistics

## 📁 Generated folder structure

```
Automation/
├── main.py
├── estadisticas.py
├── premier.py
├── nombres.txt
├── requirements.txt
├── estadisticas.xlsx
├── stats/
│   ├── Lord Bane.json
│   ├── Jokker.json
│   ├── Lord.json
│   └── ... (one JSON per player)
└── stats_premier/
    ├── Lord Bane.json
    ├── Jokker.json
    ├── Lord.json
    └── ... (one JSON per player - Premier stats)
```

## 📄 Content of each JSON file

Each JSON file in the `stats/` folder contains the following player statistics:

```json
{
  "Jugador": "Player Name",
  "Damage/Round": "145.6",
  "K/D Ratio": "1.09",
  "Headshot %": "35.1%",
  "KAST": "73.0%",
  "ACS": "214.7",
  "KAD Ratio": "1.49"
}
```

### Statistics description:
- **Damage/Round**: Average damage per round
- **K/D Ratio**: Kills to deaths ratio
- **Headshot %**: Percentage of kills that are headshots
- **KAST**: Percentage of rounds with Kill, Assist, Survival, or Trade
- **ACS**: Average Combat Score (average combat score)
- **KAD Ratio**: Ratio of (Kills + Assists) / Deaths

## 📊 XLSX file content (`estadisticas.xlsx`)

### Main features:

1. **Data consolidation**
   - All statistics from all players in a single file
   - One row per player per script execution

2. **Date history**
   - `Fecha` (Date) column recording when data was collected
   - Data accumulates without being overwritten
   - Track performance evolution over time

3. **Performance analysis**
   - Additional `{Stat}_Cambio` (Change) columns for each statistic
   - Compares current performance with previous execution
   - **Green color**: Performance improvement
   - **Red color**: Performance decline
   - **Gray color**: No change

4. **Visual design**
   - Headers in **dark blue**
   - Player names in **light orange**
   - Dates in **light green**
   - Other statistics in **light blue**
   - Frozen headers for easy scrolling

### Example XLSX structure:

| Jugador | Fecha | Damage/Round | K/D Ratio | ... | Damage/Round_Cambio | K/D Ratio_Cambio | ... |
|---------|-------|--------------|-----------|-----|---------------------|------------------|-----|
| Lord Bane | 2026-06-01 10:30:00 | 145.6 | 1.09 | ... | | | |
| Jokker898 | 2026-06-01 10:30:00 | 142.3 | 1.15 | ... | | | |

## 🔄 Periodic execution

To monitor your teammates' progress over time, run the script regularly:
- **Daily** for day-to-day changes
- **Weekly** for performance analysis
- Data will accumulate automatically in the Excel file

## 📝 Notes

- API used: `https://api.tracker.gg/` (Tracker.gg)
- Extracts statistics from the most recent competitive act
- If a player doesn't exist or has no available data, an error will appear in the console
- JSON files are saved with the player name (without the ID)

## 🐛 Troubleshooting

### Error "File nombres.txt not found"
- Make sure the `nombres.txt` file exists in the same folder as `main.py`

### API connection error
- Verify your internet connection
- Tracker.gg API might be temporarily unavailable

### Excel file is not generated
- Make sure `openpyxl` is installed: `pip install openpyxl`
- Verify that you have write permissions in the folder

---

**You're all set!** Now you know how to use the tool. 🎮📈
