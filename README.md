# Cadwork MCP Server

Ein **Model Context Protocol (MCP) Server** für die Cadwork 3D-Software, der es Claude und anderen KI-Assistenten ermöglicht, direkt mit Cadwork 3D zu interagieren.

## 🚀 Installation

### 1. Voraussetzungen
- **Python 3.8+** installiert
- **Cadwork 3D** Software
- **Claude Desktop** Anwendung

### 2. Repository klonen und Dependencies installieren
```bash
git clone <repository-url>
cd cadworkMCP
pip install -r requirements.txt
```

### 3. Cadwork Bridge einrichten
Kopiere den `bridge` Ordner in das Cadwork API-Verzeichnis:
```
C:\Program Files\cadwork\<version>\API.x64\
```

### 4. Claude Desktop konfigurieren

Die MCP-Konfiguration muss in der Claude Desktop config.json hinzugefügt werden:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Füge folgende Konfiguration hinzu:
```json
{
  "mcpServers": {
    "cadwork": {
      "command": "python",
      "args": ["C:\\pfad\\zu\\cadworkMCP\\main.py"],
      "env": {}
    }
  }
}
```

### 5. Server starten
```bash
python main.py
```

## 📋 Verfügbare Funktionen

### ✅ Element-Operationen (38 Funktionen)
- **Erstellung:** `create_beam`, `create_panel`, `create_circular_beam_points`, `create_square_beam_points`, `create_standard_beam_points`, `create_standard_panel_points`, `create_drilling_points`, `create_polygon_beam`, `create_auxiliary_beam_points`
- **Abfragen:** `get_active_element_ids`, `get_all_element_ids`, `get_visible_element_ids`, `get_element_info`, `get_user_element_ids`
- **Bearbeitung:** `delete_elements`, `copy_elements`, `move_element`, `duplicate_elements`
- **Filterung:** `get_elements_by_type`, `filter_elements_by_material`, `get_elements_in_group`
- **Statistiken:** `get_element_count_by_type`, `get_material_statistics`, `get_group_statistics`
- **Verbindungen:** `join_elements`, `unjoin_elements`
- **Holzverbindungen:** `cut_corner_lap`, `cut_cross_lap`, `cut_half_lap`, `cut_double_tenon`, `cut_scarf_joint`, `cut_shoulder`
- **Konvertierung:** `convert_beam_to_panel`, `convert_panel_to_beam`, `convert_auxiliary_to_beam`
- **Container:** `create_auto_container_from_standard`, `get_container_content_elements`

### ✅ Geometrie-Operationen (24 Funktionen)
- **Abmessungen:** `get_element_width`, `get_element_height`, `get_element_length`, `get_element_volume`, `get_element_weight`
- **Vektoren & Punkte:** `get_element_xl`, `get_element_yl`, `get_element_zl`, `get_element_p1`, `get_element_p2`, `get_element_p3`
- **Schwerpunkt:** `get_center_of_gravity`, `get_center_of_gravity_for_list`
- **Vertices & Flächen:** `get_element_vertices`, `get_element_facets`, `get_element_reference_face_area`, `get_total_area_of_all_faces`
- **Analyse:** `get_minimum_distance_between_elements`, `get_element_type`
- **Transformationen:** `rotate_elements`, `apply_global_scale`, `invert_model`, `rotate_height_axis_90`, `rotate_length_axis_90`
- **Berechnungen:** `calculate_total_volume`, `calculate_total_weight`

### ✅ Attribut-Management (8 Funktionen)
- **Abfragen:** `get_standard_attributes`, `get_user_attributes`, `list_defined_user_attributes`
- **Setzen:** `set_name`, `set_material`, `set_group`, `set_comment`, `set_subgroup`

### ✅ Visualisierung (10 Funktionen)
- **Eigenschaften:** `set_color`, `set_visibility`, `set_transparency`, `get_color`, `get_transparency`
- **Globale Steuerung:** `show_all_elements`, `hide_all_elements`, `refresh_display`, `get_visible_element_count`, `get_visible_element_count`

### ✅ Utility-Funktionen (6 Funktionen)
- **Display:** `disable_auto_display_refresh`, `enable_auto_display_refresh`
- **Nachrichten:** `print_error`, `print_warning`
- **Projekt:** `get_3d_file_path`, `get_project_data`, `get_cadwork_version_info`

### ✅ Spezielle Module
- **Werkstattzeichnungen (2):** `add_wall_section_x`, `add_wall_section_y`
- **Dach-Analysen (2):** `get_roof_surfaces`, `calculate_roof_area`
- **Maschinen-Integration (1):** `check_production_list_discrepancies`

**Gesamt: 91 verfügbare Funktionen**

## 🏗️ Projekt-Struktur

```
cadworkMCP/
├── main.py                 # Haupt-MCP-Server mit allen Tool-Definitionen
├── requirements.txt        # Python-Dependencies
├── mypy.ini               # Mypy-Konfiguration für Typsicherheit
├── cadwork_bridge.py      # Legacy Bridge (wird ersetzt)
├── claude_desktop_config.json  # Beispiel-Konfiguration
│
├── core/                  # Kernfunktionalitäten
│   ├── server.py          # MCP-Server Setup
│   ├── connection.py      # Cadwork-Verbindungsmanagement
│   └── logging.py         # Logging-Konfiguration
│
├── controllers/           # Funktionsgruppen (Controller-Pattern)
│   ├── base_controller.py        # Basis-Controller
│   ├── element_controller.py     # Element-Operationen
│   ├── geometry_controller.py    # Geometrie-Operationen
│   ├── attribute_controller.py   # Attribut-Management
│   ├── visualization_controller.py # Visualisierung
│   ├── utility_controller.py     # Utility-Funktionen
│   ├── shop_drawing_controller.py # Werkstattzeichnungen
│   ├── roof_controller.py        # Dach-Analysen
│   └── machine_controller.py     # Maschinen-Integration
│
├── bridge/                # Cadwork-Bridge (in API.x64 kopieren)
│   ├── dispatcher.py      # Command-Dispatcher
│   ├── helpers.py         # Hilfsfunktionen
│   └── handlers/          # Spezifische Handler
│
└── API.x64/              # Cadwork API-Dateien (für Entwicklung)
```

## 📝 Code Guidelines

### Konventionen
- **Async/Await:** Alle MCP-Tools sind asynchron
- **Typsicherheit:** Vollständige mypy-Kompatibilität mit `Dict[str, Any]` Return-Typen
- **Parameter-Typen:** Spezifische List-Typen (`List[int]`, `List[float]`)
- **Englische Kommentare:** Alle Code-Kommentare auf Englisch
- **Controller-Pattern:** Funktionen nach Bereichen gruppiert

### Neue Funktionen hinzufügen
1. **Controller erweitern** oder neuen erstellen
2. **Typen spezifizieren** (`List[int]`, `Dict[str, Any]`)
3. **MCP-Tool in main.py** registrieren
4. **Tests hinzufügen** (falls vorhanden)

### Debugging
- Logs in `core/logging.py` konfiguriert
- Debug-Modus über Umgebungsvariablen
- Cadwork-Verbindung über `core/connection.py` überwachen

---

*Letztes Update: Juli 2025 - 91 Funktionen verfügbar*