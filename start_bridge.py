#!/usr/bin/env python3
"""
Startskript für die Cadwork MCP Bridge
"""

import os
import sys

# Stelle sicher, dass wir im richtigen Verzeichnis sind
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Füge das Verzeichnis zum Python-Pfad hinzu
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Importiere und starte die Bridge
try:
    from cadwork_bridge import main
    main()
    
    # Halte das Programm am Laufen
    input("Drücke Enter um die Bridge zu stoppen...")
    
except KeyboardInterrupt:
    print("\nBridge gestoppt.")
except ImportError as e:
    print(f"Import-Fehler: {e}")
    print("Stelle sicher, dass alle Abhängigkeiten installiert sind.")
except Exception as e:
    print(f"Fehler beim Starten der Bridge: {e}")
    import traceback
    traceback.print_exc()
