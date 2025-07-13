# Cadwork MCP - Simple Test Runner

## Überblick

Ein einfaches, aufgeräumtes Test-System für alle Cadwork MCP Server Funktionen.

## Nutzung

### Einfacher Start
```python
from tests.clean.run_test import runTest

# Führe alle Tests aus
runTest()
```

### Direkter Aufruf
```bash
cd C:\cadworkMCP\tests\clean
python run_test.py
```

## Features

- ✅ **Einfach**: Nur eine Funktion aufrufen - `runTest()`
- 🧹 **Aufgeräumt**: Klare Struktur nach C++ Coding Standards
- 📊 **Übersichtlich**: Schöne Zusammenfassung mit Emojis und Tabellen
- 🚀 **Schnell**: Effiziente Ausführung aller Tests
- 🔧 **Flexibel**: Leicht erweiterbar für neue Tests

## Test Suites

1. **Element Controller** - Beam/Panel Erstellung, Element-Verwaltung
2. **Geometry Controller** - Geometrie-Informationen, Volumen-Berechnungen  
3. **Attribute Controller** - Material-Einstellungen, Standard-Attribute
4. **Visualization Controller** - Sichtbarkeit, Display-Funktionen
5. **System Tests** - Verbindung, Projekt-Info, Version

## Architektur

- `CTestSuite` - Basis-Klasse für alle Test-Suites
- `CTestResult` - Container für Test-Ergebnisse
- `CTestStatus` - Enum für Test-Status (PASSED/FAILED/SKIPPED/ERROR)
- Automatische Element-Verfolgung für Cleanup
- Verbindungstest vor jedem Test-Suite

## Coding Standards

Verwendet deine bevorzugten C++ Naming Conventions:
- Lokale Variablen: `l` + UpperCamelCase (z.B. `lResult`)
- Member Variablen: `m_` + UpperCamelCase (z.B. `m_aName`)
- Parameter: `a` + UpperCamelCase (z.B. `aTestName`)
- Klassen: `C` + Name (z.B. `CTestSuite`)

## Beispiel Output

```
================================================================================
                    CADWORK MCP SERVER - SIMPLE TEST RUNNER                    
================================================================================

📦 Element Controller Tests
==================================================
  🔍 Get All Elements
    PASSED (0.05s) - ✅ Successful
  🔍 Create Beam
    PASSED (0.12s) - ✅ Successful

================================================================================
                                TEST SUMMARY                                  
================================================================================
Suite                     Total  ✅     ❌     ⚠️     ⏭️     Success  Time    
--------------------------------------------------------------------------------
Element Controller        5      5      0      0      0       100.0%     0.45s
Geometry Controller       2      2      0      0      0       100.0%     0.23s
...
================================================================================

🎉 [SUCCESS] ALL TESTS PASSED! 🎉
```

## Erweiterung

Um neue Tests hinzuzufügen:

1. Erstelle eine neue Test-Klasse, die von `CTestSuite` erbt
2. Implementiere Test-Methoden
3. Füge die Klasse zur `lTestSuites` Liste in `runTest()` hinzu

```python
class CMeinNeuerTest(CTestSuite):
    def __init__(self):
        super().__init__("Mein Neuer Test")
    
    def testMeineFunktion(self) -> Dict[str, Any]:
        # Test Implementation
        return {"status": "ok"}
    
    def runAllTests(self) -> Dict[str, Any]:
        if not self.checkConnection():
            return {"status": "error", "message": "Connection failed"}
        
        self.runTest(self.testMeineFunktion, "Meine Funktion")
        return self.getSummary()
```
