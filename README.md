# Northeastern University Campus Map - Shortest Path Finder

This project aims to help users find the shortest path between any two buildings on the Northeastern University Boston campus using Dijkstra’s Algorithm. The application provides a visual representation of the campus map, highlights the shortest path between selected buildings, and allows users to interact with the map through a Streamlit-based web interface.

## Features

* Interactive web application built with Streamlit.
* Utilizes Dijkstra's Algorithm to find the shortest path.
* Visual representation of the campus map using NetworkX and Matplotlib.
* Allows users to select start and end buildings to find the shortest path.
* Highlights the shortest path on the map.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `networkx` library
- `matplotlib` library
- `streamlit` library

Install the required libraries using pip:

```bash
pip install networkx matplotlib streamlit
```

### Installation:

1. Clone the repository:
```bash
git clone https://github.com/partheshp/SignLanguageConverter.git
cd SignLanguageConverter
```

2. Ensure you have the necessary data files (graph.txt and mappings.txt) in the project directory. The format of these files is as follows:
**graph.txt:**
```php
<number_of_vertices>
<vertex1> <vertex2> <distance>
...
```

**mappings.txt:**
```php
<number_of_buildings>
<vertex_number> <building_code>
...
```
### Usage:

Run the Streamlit application:
```bash
streamlit run app.py
```
