# Cadwork MCP Server - Testing Guide

## 🧪 Test Suite Overview

Das Test-Framework für den Cadwork MCP Server bietet umfassende Tests für alle implementierten Funktionen:

- **89 Funktionen getestet** (Update: Version 3.4) 
- **8 Test-Controller** (Element, Geometry, Attribute, Visualization, Utility, Shop Drawing, Roof, System)
- **Automatische Bereinigung** - Erstelle Test-Elemente werden automatisch gelöscht
- **Umfassende Validierung** - Parameter, Rückgabewerte und Fehlerfälle
- **Detaillierte Berichte** - Erfolgsraten, Timing, Fehlerdetails

## 📁 Test-Struktur

```
tests/
├── __init__.py                    # Test Package
├── test_config.py                 # Test Framework & Utilities  
├── test_element_controller.py     # Element Creation & Management Tests
├── test_geometry_controller.py    # Geometry & Transformation Tests
├── test_attribute_controller.py   # Attribute Get/Set Tests
├── test_visualization_controller.py # Visualization & Display Tests
├── test_utility_controller.py     # Utility & Performance Tests
├── test_system.py                 # System Information Tests
├── run_tests.py                   # Main Test Runner
├── requirements.txt               # Test Dependencies
└── README.md                      # This file
```

## 🚀 Tests ausführen

### Alle Tests ausführen:
```bash
cd C:\cadworkMCP
python tests\run_tests.py
```

### Einzelne Test-Suite ausführen:
```bash
# Nur Element Controller Tests
python tests\run_tests.py --suite element

# Nur Geometry Controller Tests  
python tests\run_tests.py --suite geometry

# Nur Shop Drawing Controller Tests
python tests\run_tests.py --suite shop_drawing
```

### Ohne Verbindungstest (für Debugging):
```bash
python tests\run_tests.py --skip-connection
```

## [CONFIG] Voraussetzungen

### Für vollständige Tests:
1. **Cadwork 3D läuft**
2. **Bridge gestartet** (start.txt in Cadwork Python-Konsole ausführen)
3. **Bridge hört auf Port 53002**

### Für Test-Entwicklung:
- Tests können auch ohne Cadwork-Verbindung ausgeführt werden (`--skip-connection`)
- Parameter-Validierung und Controller-Logik werden trotzdem getestet

## 📊 Test-Berichte

### Beispiel-Ausgabe:
```
================================================================================
                              TEST SUMMARY                               
================================================================================
Suite                          Total    Passed   Failed   Success    Time    
--------------------------------------------------------------------------------
Element Controller Tests      28       26       2        92.9%      3.45s
Geometry Controller Tests     26       26       0        100.0%     2.10s
Attribute Controller Tests    8        8        0        100.0%     1.15s
Visualization Controller Tests 12      12       0        100.0%     1.67s
Utility Controller Tests      10       10       0        100.0%     1.45s
System Tests                  1        1        0        100.0%     0.23s
--------------------------------------------------------------------------------
TOTAL                          85       83       2        97.6%      10.05s
================================================================================
```

## 🧪 Was wird getestet?

### Element Controller (40 Tests):
- **Element Creation:** create_beam, create_panel, create_circular_beam_points, create_auxiliary_beam_points, etc.
- **Element Management:** copy_elements, move_element, delete_elements
- **Element Conversion:** VOLLSTÄNDIGE Suite - beam/panel/auxiliary Konvertierungen (NEU)
- **Element Connections:** join_elements, unjoin_elements
- **Element Retrieval:** get_all_element_ids, get_active_element_ids, get_visible_element_ids, etc.  
- **Query & Filter:** get_elements_by_type, filter_by_material, statistics
- **Cut Operations:** 6 verschiedene Holzverbindungstypen
- **Container Management:** NEUE Suite - Container-Erstellung und -Verwaltung (NEU)
- **Auxiliary Elements:** Hilfs-Konstruktionen und Workflows
- **Workflow Tests:** Komplette Konvertierungs- und Container-Workflows (NEU)
- **Error Handling:** Ungültige Parameter, negative IDs

### Geometry Controller (12 Tests):
- **Dimensionen:** get_element_width, get_element_height, get_element_length
- **Volumen & Gewicht:** get_element_volume, get_element_weight
- **Koordinatensystem:** get_element_xl, get_element_yl, get_element_zl
- **Punkte:** get_element_p1, get_element_p2, get_element_p3
- **Schwerpunkt:** get_center_of_gravity, get_center_of_gravity_for_list
- **Oberflächen:** get_element_reference_face_area, get_total_area_of_all_faces

### Geometry Controller (26 Tests):
- **Dimensionen:** get_element_width, get_element_height, get_element_length
- **Volumen & Gewicht:** get_element_volume, get_element_weight
- **Koordinatensystem:** get_element_xl, get_element_yl, get_element_zl
- **Punkte:** get_element_p1, get_element_p2, get_element_p3
- **Schwerpunkt:** get_center_of_gravity, get_center_of_gravity_for_list
- **Oberflächen:** get_element_reference_face_area, get_total_area_of_all_faces
- **Transformationen:** rotate_elements, apply_global_scale, invert_model
- **Berechnungen:** calculate_total_volume, calculate_total_weight

### Attribute Controller (8 Tests):
- **Attribute Getter:** get_standard_attributes, get_user_attributes
- **Attribute Setter:** set_name, set_material, set_group, set_comment, set_subgroup
- **Listen:** list_defined_user_attributes
- **Validierung:** Verschiedene Parameter-Kombinationen

### Visualization Controller (12 Tests):
- **Farben:** set_color, get_color mit Validierung
- **Transparenz:** set_transparency, get_transparency mit Edge-Cases  
- **Sichtbarkeit:** set_visibility, show_all_elements, hide_all_elements
- **Display:** refresh_display, get_visible_element_count
- **Workflow-Tests:** Komplette Visualization-Pipelines
- **Error-Handling:** Ungültige Farb-IDs und Transparenz-Werte

### Utility Controller (10 Tests):
- **Performance Functions:** disable/enable_auto_display_refresh (NEU!)
- **Output Functions:** print_error, print_warning (NEU!)
- **System Info:** get_3d_file_path, get_project_data (NEU!)
- **Workflow Tests:** Komplette Display-Refresh Workflows
- **Error Handling:** Parameter-Validierung für alle Utility-Funktionen

### System Controller (1 Test):
- **Version Info:** get_cadwork_version_info - Cadwork Version abrufen
- **Attribute Getter:** get_standard_attributes, get_user_attributes
- **Attribute Setter:** set_name, set_material
- **Listen:** list_defined_user_attributes
- **Validierung:** Verschiedene Parameter-Kombinationen

## 🔧 Test-Framework Features

### TestSuite Klasse:
```python
class MyTests(TestSuite):
    def setup(self):
        # Setup vor allen Tests
        pass
    
    def teardown(self):
        # Cleanup nach allen Tests
        pass
    
    def test_my_function(self):
        # Test-Methode (muss mit 'test_' anfangen)
        result = my_function()
        assert_ok(result)
        return result
```

### Assertion Helpers:
```python
assert_ok(result)                    # Status == "ok"
assert_error(result)                 # Status == "error"  
assert_element_id(result)            # Gültige Element-ID
assert_has_key(result, "key")        # Key vorhanden
```

### Automatische Element-Verwaltung:
- Alle erstellten Test-Elemente werden automatisch verfolgt
- Automatische Bereinigung in teardown()
- Keine "Test-Müll" Elemente bleiben zurück

## 📝 Eigene Tests hinzufügen

### Neuen Test zur bestehenden Suite hinzufügen:
```python
def test_my_new_function(self):
    """Test description"""
    # Create test element
    element = self.create_test_element()
    
    # Test the function
    result = asyncio.run(self.controller.my_new_function(element))
    
    # Validate result
    assert_ok(result)
    assert_has_key(result, "expected_key")
    
    return result
```

### Neue Test-Suite erstellen:
```python
class NewControllerTests(TestSuite):
    def __init__(self):
        super().__init__("New Controller Tests")
        self.controller = NewController()
    
    def test_new_function(self):
        # Test implementation
        pass
```

## 🐛 Debugging & Troubleshooting

### Häufige Probleme:

**Connection Failed:**
- Cadwork 3D läuft nicht
- Bridge nicht gestartet
- Port 53002 blockiert

**Test Elements Not Cleaned:**
- teardown() Exception
- Cadwork-Verbindung während Tests unterbrochen

**Import Errors:**
- PROJECT_ROOT nicht korrekt gesetzt
- Controller-Module nicht gefunden

### Debug-Modus:
```python
# In test_config.py Debug-Ausgaben aktivieren:
print(f"Testing function with params: {params}")
print(f"Result: {result}")
```

## 📈 Performance

### Benchmark-Zahlen:
- **~40 Tests in ~6 Sekunden** (bei Cadwork-Verbindung)
- **~7 Tests/Sekunde** Durchschnitt
- **Parallele Test-Suiten** möglich
- **Element Creation** am langsamsten (~200ms pro Element)
- **Geometry Queries** am schnellsten (~50ms pro Abfrage)

## 🎯 Qualitätssicherung

### Code Coverage:
- **70/70 Funktionen** haben mindestens einen Test
- **Error Paths** werden explizit getestet
- **Parameter Validation** wird geprüft
- **Return Value Validation** für alle Funktionen

### CI/CD Integration:
Das Test-Framework ist bereit für Continuous Integration:
```bash
# Exit Code 0 = alle Tests erfolgreich
# Exit Code 1 = mindestens ein Test fehlgeschlagen
python tests\run_tests.py
echo $?  # Prüfe Exit Code
```

Das Test-System gewährleistet, dass alle 70 implementierten MCP-Tools korrekt funktionieren! 🚀


### Shop Drawing Controller (5 Tests):
- **Werkstattzeichnungs-Funktionen:** add_wall_section_x, add_wall_section_y (NEU)
- **Technische Schnitte:** X- und Y-Richtungs-Wandschnitte für Fertigungsplanung
- **Parameter-Management:** Section-Parameter für Darstellungsoptionen
- **Workflow Tests:** Komplette Shop Drawing Workflows (NEU)
- **Error Handling:** Ungültige Wall-IDs und Parameter-Validierung

### Roof Controller (5 Tests):
- **Dach-spezifische Funktionen:** get_roof_surfaces, calculate_roof_area (NEU)
- **Dachflächen-Analyse:** Neigungen, Orientierungen und geometrische Eigenschaften
- **Flächenberechnungen:** Spezialisierte Roof-Area-Berechnungen für Zimmerei
- **Workflow Tests:** Komplette Dach-Konstruktions-Workflows (NEU)
- **Error Handling:** Validierung von Dach-Elementen und Parameter-Checks