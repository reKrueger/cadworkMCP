# 📋 Manuelle Installation - Cadwork MCP Bridge Plugin

## 🎯 Einfache Kopier-Anleitung

### Schritt 1: Cadwork Plugin-Verzeichnis finden
1. **Cadwork 3D** öffnen
2. **Help → Info** klicken  
3. **"Userprofile"** Ordner öffnen
4. Zu **`3d\API.x64`** navigieren

**Typischer Pfad:**
```
C:\Users\Public\Documents\cadwork\userprofil_xx\3d\API.x64
```

### Schritt 2: Plugin kopieren
1. **Diesen kompletten `MCPBridge` Ordner** kopieren:
```
C:\cadworkMCP\API.x64\MCPBridge\
```

2. **Einfügen** in Cadwork's API.x64 Verzeichnis:
```
[CADWORK_USERPROFILE]\3d\API.x64\MCPBridge\
```

### Schritt 3: Struktur prüfen
Nach dem Kopieren sollte die Struktur so aussehen:
```
[CADWORK_USERPROFILE]\3d\API.x64\
└── MCPBridge\
    ├── MCPBridge.py          ← Hauptplugin
    ├── bridge_server.py      ← Bridge Server  
    ├── plugin_info.xml       ← Plugin Info
    └── README.md             ← Diese Anleitung
```

## 🚀 Plugin verwenden

### 1. Cadwork neu starten
- **Cadwork 3D** schließen und neu öffnen

### 2. Plugin aktivieren
- **Window → Plugins** (Plugin-Leiste anzeigen)
- **MCP Bridge** Button erscheint
- Button **klicken** um Plugin zu starten

### 3. Bridge starten
- **GUI öffnet sich** automatisch
- **"Start Bridge"** Button klicken
- Status zeigt **"Running"** an
- **"Test Connection"** für Verbindungstest

## 🔗 MCP Server verbinden

Nach erfolgreichem Plugin-Start:

```bash
cd C:\cadworkMCP
python main.py
```

Jetzt können externe Tools (wie Claude) Cadwork steuern!

## ⚙️ Plugin-Features

- ✅ **Ein-Klick Bridge Start**
- ✅ **Status-Monitoring** 
- ✅ **Connection Testing**
- ✅ **GUI-Kontrolle**
- ✅ **Embedded Server**

## 🛠️ Troubleshooting

### Plugin erscheint nicht
- **Cadwork neu starten**
- **Plugin-Leiste prüfen**: Window → Plugins  
- **Ordnername prüfen**: Muss exakt `MCPBridge` heißen

### Bridge startet nicht
- **Port 53002** frei? (andere Programme prüfen)
- **Python-Pfade** korrekt?
- **Cadwork Console** für Fehlermeldungen prüfen

### Verbindung fehlgeschlagen
- **"Test Connection"** im Plugin verwenden
- **Firewall-Einstellungen** prüfen
- Nur **localhost/127.0.0.1** verwenden

## 🎯 Das wars!

**3 einfache Schritte:**
1. **Ordner kopieren**
2. **Plugin starten** 
3. **Bridge aktivieren**

Ihr Cadwork ist jetzt bereit für externe Tool-Integration! 🎉
