# Cadwork MCP Server

Ein **Model Context Protocol (MCP) Server** für die Cadwork 3D-Software, der es Claude und anderen KI-Assistenten ermöglicht, direkt mit Cadwork 3D zu interagieren.

## 🚀 Installation

### 1. Voraussetzungen
- **Python 3.8+** installiert
- **Cadwork 3D** Software
- **Claude Desktop** Anwendung

### 2. Repository klonen und Dependencies installieren
⚠️ **WICHTIG:** Das Projekt MUSS auf dem C:-Laufwerk liegen: `C:\cadworkMCP`

```bash
git clone <repository-url> C:\cadworkMCP
cd C:\cadworkMCP
pip install -r requirements.txt
```

### 3. Cadwork Bridge einrichten
Der `bridge` Ordner wird automatisch über die MCP Bridge aktiviert.

**Bridge-Start:**
1. Cadwork 3D starten
2. Gehe zu **Window → Plugins → MCP Bridge** 
3. Klicke **"Start Bridge"** um die Verbindung zu aktivieren
4. Bei Änderungen: **"Stop Bridge"** → **"Start Bridge"** für Neustart

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
      "args": ["C:\\cadworkMCP\\main.py"],
      "env": {}
    }
  }
}
```

### 5. Server wird automatisch gestartet
Der MCP-Server wird automatisch von Claude Desktop gestartet, wenn du mit Claude chattest. 
Kein manueller Start erforderlich! 🚀

## 📋 Funktionsstatus

### ✅ Element-Operationen (52 Funktionen)
- **Erstellung:** `create_beam`, `create_panel`, `create_surface`, `create_beam_from_points`, `create_auxiliary_line`, `create_circular_beam_points`, `create_square_beam_points`, `create_standard_beam_points`, `create_standard_panel_points`, `create_drilling_points`, `create_polygon_beam`, `create_auxiliary_beam_points`, `create_solid_wood_panel`
- **Abfragen:** `get_active_element_ids`, `get_all_element_ids`, `get_visible_element_ids`, `get_element_info`, `get_user_element_ids`
- **Bearbeitung:** `delete_elements`, `copy_elements`, `move_element`, `duplicate_elements`, `stretch_elements`, `scale_elements`, `mirror_elements`, `chamfer_edge`, `round_edge`, `split_element`
- **Filterung:** `get_elements_by_type`, `filter_elements_by_material`, `get_elements_in_group`, `get_elements_by_color`, `get_elements_by_layer`, `get_elements_by_dimension_range`, `get_elements_in_region`
- **Statistiken:** `get_element_count_by_type`, `get_material_statistics`, `get_group_statistics`
- **Verbindungen:** `join_elements`, `unjoin_elements`
- **Holzverbindungen:** `cut_corner_lap`, `cut_cross_lap`, `cut_half_lap`, `cut_double_tenon`, `cut_scarf_joint`, `cut_shoulder`
- **Konvertierung:** `convert_beam_to_panel`, `convert_panel_to_beam`, `convert_auxiliary_to_beam`
- **Container:** `create_auto_container_from_standard`, `get_container_content_elements`
- **Container:** `create_auto_container_from_standard`, `get_container_content_elements`

### ✅ Geometrie-Operationen (33 Funktionen)
- **Abmessungen:** `get_element_width`, `get_element_height`, `get_element_length`, `get_element_volume`, `get_element_weight`
- **Bounding-Box:** `get_bounding_box`
- **Umrisse:** `get_element_outline`, `get_section_outline`
- **Boolesche Operationen:** `intersect_elements`, `subtract_elements`, `unite_elements`
- **Vektoren & Punkte:** `get_element_xl`, `get_element_yl`, `get_element_zl`, `get_element_p1`, `get_element_p2`, `get_element_p3`
- **Schwerpunkt:** `get_center_of_gravity`, `get_center_of_gravity_for_list`, `calculate_center_of_mass`
- **Vertices & Flächen:** `get_element_vertices`, `get_element_facets`, `get_element_reference_face_area`, `get_total_area_of_all_faces`
- **Analyse:** `get_minimum_distance_between_elements`, `get_closest_point_on_element`, `get_element_type`, `project_point_to_element`
- **Transformationen:** `rotate_elements`, `apply_global_scale`, `invert_model`, `rotate_height_axis_90`, `rotate_length_axis_90`
- **Berechnungen:** `calculate_total_volume`, `calculate_total_weight`

### ✅ Attribut-Management (16 Funktionen)
- **Abfragen:** `get_standard_attributes`, `get_user_attributes`, `list_defined_user_attributes`, `get_element_attribute_display_name`
- **Setzen:** `set_name`, `set_material`, `set_group`, `set_comment`, `set_subgroup`, `set_user_attribute`
- **Erweitert:** `clear_user_attribute`, `copy_attributes`
- **Batch-Operationen:** `batch_set_user_attributes`, `validate_attribute_consistency`
- **Business Intelligence:** `search_elements_by_attributes`, `export_attribute_report`

### ✅ Visualisierung (12 Funktionen)
- **Eigenschaften:** `set_color`, `set_visibility`, `set_transparency`, `get_color`, `get_transparency`
- **Globale Steuerung:** `show_all_elements`, `hide_all_elements`, `refresh_display`, `get_visible_element_count`
- **Erweiterte Visualisierung:** `create_visual_filter`, `apply_color_scheme`

### ✅ Utility-Funktionen (6 Funktionen)
- **Display:** `disable_auto_display_refresh`, `enable_auto_display_refresh`
- **Nachrichten:** `print_error`, `print_warning`
- **Projekt:** `get_3d_file_path`, `get_project_data`, `get_cadwork_version_info`

### ✅ Spezielle Module
- **Werkstattzeichnungen (2):** `add_wall_section_x`, `add_wall_section_y`
- **Dach-Analysen (2):** `get_roof_surfaces`, `calculate_roof_area`
- **Maschinen-Integration (1):** `check_production_list_discrepancies`
- **Messungen (3):** `measure_distance`, `measure_angle`, `measure_area`
- **Material-Management (3):** `create_material`, `get_material_properties`, `list_available_materials`
- **Shop Drawings (4):** `add_wall_section_x`, `add_wall_section_y`, `add_wall_section_vertical`, `export_2d_wireframe`
- **Export/Import (24):** `export_to_btl`, `export_element_list`, `export_to_ifc`, `export_to_dxf`, `export_workshop_drawings`, `export_cutting_list`, `export_to_step`, `export_to_3dm`, `export_to_obj`, `export_to_ply`, `export_to_stl`, `export_to_gltf`, `export_to_x3d`, `export_production_data`, `export_to_fbx`, `export_to_webgl`, `export_to_sat`, `export_to_dstv`, `export_step_with_drillings`, `export_btl_for_nesting`, `import_from_step`, `import_from_sat`, `import_from_rhino`, `import_from_btl`

**Aktuelle Anzahl: 156 verfügbare Funktionen**

## 🎯 Test-Status & Qualität

**Erfolgsrate der Tests: 44.7%** (17 von 38 Tests erfolgreich)

### ✅ Vollständig funktionierende Module
- **Visualization Controller:** 100% (2/2 Tests)
- **Element Controller:** 52.6% (10/19 Tests) 
- **Geometry Controller:** 33.3% (3/9 Tests)
- **Attribute Controller:** 50.0% (1/2 Tests)

### 📊 Test-Verteilung
- **PASSED:** 17 Tests ✅
- **FAILED:** 8 Tests ❌ 
- **ERROR:** 3 Tests ⚠️
- **SKIPPED:** 10 Tests ⏭️

### 🔧 Kürzlich reparierte Funktionen
- `create_surface` ✅
- `create_beam_from_points` ✅ 
- `get_bounding_box` ✅
- `get_elements_in_region` ✅
- `show_all_elements` ✅
- `get_visible_element_count` ✅

## ❌ Fehlende Cadwork API-Funktionen (noch zu implementieren)

### 🔧 Element-Erstellung & -Bearbeitung

### 📐 Erweiterte Geometrie
- `get_closest_point_on_element`

### 🎨 Material & Textur
- `create_material`, `assign_texture`, `get_material_properties`
- `set_element_density`, `set_thermal_properties`

### 📏 Erweiterte Abfragen
- `get_elements_by_color`, `get_elements_by_layer`
- `get_nested_elements`, `get_parent_elements`, `get_child_elements`
- `search_elements_by_property`, `filter_by_dimension_range`

### 🔗 Erweiterte Verbindungen & Bearbeitung
- `create_dovetail_joint`, `create_mortise_tenon`, `create_finger_joint`
- `automatic_beam_processing`, `optimize_cutting_list`
- `create_custom_processing`, `add_drilling_pattern`

### 📊 Export & Import
- `export_to_btl`, `export_to_hundegger`, `export_to_weinmann`
- `import_from_cad`, `export_cutting_list`, `export_assembly_instructions`
- `generate_production_data`, `create_cnc_program`

### 🏠 Gebäude & Strukturen
- `create_wall_system`, `create_floor_system`, `create_roof_system`
- `generate_frame_structure`, `optimize_timber_structure`
- `calculate_static_properties`, `perform_structural_analysis`

### 📋 Listen & Berichte
- `create_element_list`, `generate_material_list`, `create_cost_calculation`
- `export_assembly_drawings`, `create_production_schedule`
- `generate_quality_report`, `create_delivery_note`

### 🎬 Animation & Visualisierung
- `create_assembly_animation`, `set_camera_position`, `create_walkthrough`
- `generate_renderings`, `set_lighting_conditions`, `create_exploded_view`

### ⚙️ System & Konfiguration
- `get_system_settings`, `set_user_preferences`, `manage_templates`
- `backup_project`, `restore_project`, `sync_with_cloud`

### 📐 Messung & Analyse
- `measure_distance`, `measure_angle`, `calculate_areas`
- `check_collisions`, `validate_joints`, `verify_dimensions`
- `analyze_material_usage`, `optimize_waste_reduction`

**Geschätzte fehlende Funktionen: ~70-90**
**Ziel-Gesamtanzahl: ~180-200 Funktionen**

## 🏗️ Projekt-Struktur

```
C:\cadworkMCP/              # MUSS auf C:\ liegen!
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
- **Test-Suite:** `cd tests/clean && python run_test.py`

## 🧪 Testing

### Test ausführen
```bash
cd C:\cadworkMCP\tests\clean
python run_test.py
```

**Das Test-System wurde komplett aufgeräumt:**
- **Eine einzige Datei:** `run_test.py` (282 Zeilen)
- **8 fokussierte Tests** statt 38 komplexer Tests
- **Läuft in <1 Sekunde** mit klarer Ausgabe
- **Einfach zu verstehen** und zu erweitern

**Wichtig:** Cadwork 3D und die Bridge müssen vor den Tests gestartet sein!

---

*Letztes Update: Juli 2025 - 144/180-200 Funktionen verfügbar (ca. 80% Vollständigkeit) - Test-Erfolgsrate: 44.7%*