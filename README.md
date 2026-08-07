# London Underground Distance Tool

A web app that calculates the shortest travel distance between any two London Underground stations, showing the full route, number of stops, and which line to take for each leg.

>[Live demo](https://tube-distance-calculator.streamlit.app/)


## Features

- Pick a start and end station from dropdown menus
- Calculates the shortest path by distance (km) using Dijkstra's algorithm
- Displays the full route as a station-by-station chain
- Shows the number of stops on the journey
- Breaks down each leg of the route with the line to use

## How it works

The app is built on a graph of the Underground network, where each station is a node and each connection between adjacent stations is a weighted edge (weight = distance in km). This graph is precomputed and saved to disk, so the app itself only has to load it and run a shortest-path search — it does no data processing at runtime.

The project has three stages:

1. **Data cleaning** (`Data_Cleaning.ipynb`)
   Loads the raw station, line, and inter-station distance data and cleans it up: strips whitespace, standardises line names (e.g. removing "Line" suffixes, renaming "H & C" to "Hammersmith & City"), removes decommissioned lines, drops unused columns, and lowercases station names for consistent matching. Outputs cleaned CSVs.

2. **Data merging** (`Data_Merge.ipynb`)
   Reconciles station names between the distance dataset and the stations dataset, which used different spellings and conventions (e.g. "kings cross" vs "king's cross st. pancras", "regents park" vs "regent's park"). Also disambiguates stations that share a name but are physically separate platforms on different lines (e.g. the two Edgware Road stations, the two Shepherd's Bush stations), adds missing stations/edges (e.g. the Northern line extension to Battersea Power Station), and merges everything into a single edge list with station IDs attached.

3. **Graph building** (`graph.ipynb`)
   Deduplicates station pairs, builds an undirected weighted graph with `networkx` (edge weight = distance, edge attribute = line), and saves the graph plus lookup dictionaries (`id_to_name`, `name_to_id`) as pickle files for the app to load.

4. **App** (`app.py`)
   Loads the precomputed graph and dictionaries, then uses `nx.dijkstra_path_length` and `nx.dijkstra_path` to find the shortest route between the selected stations and render the results.

## Project structure

```
.
├── app.py                  # Streamlit app
├── Data_Cleaning.ipynb     # Stage 1: clean raw datasets
├── Data_Merge.ipynb        # Stage 2: reconcile & merge into one edge list
├── graph.ipynb             # Stage 3: build & pickle the graph
├── graph.pkl               # Precomputed network graph (generated)
├── id_to_name.pkl          # Station ID → name lookup (generated)
├── name_to_id.pkl          # Station name → ID lookup (generated)
└── README.md
```

## Setup

**Requirements:**
- Python 3.12+
- streamlit
- pandas
- networkx
- openpyxl (for reading the raw `.xlsx` distance file, if re-running the cleaning notebook)

Install dependencies:

```bash
pip install streamlit pandas networkx openpyxl
```

## Usage

Make sure `graph.pkl`, `id_to_name.pkl`, and `name_to_id.pkl` are in the same directory as `app.py` (run the three notebooks in order — cleaning → merge → graph — to regenerate them if needed), then run:

```bash
streamlit run app.py
```

Select a "From" and "To" station and click **Calculate Distance** to see the route.

## Data sources

- London Underground station and line reference data
- Inter-station distance database (`Inter_station_database.xlsx`)

*(Update this section with the specific source/attribution for your raw datasets.)*

## Notes & limitations

- Distances are based on the published inter-station distance data, not real-time travel times.
- Some historically renamed or decommissioned stations/lines (e.g. East London Line, Docklands Light Railway) are excluded.
