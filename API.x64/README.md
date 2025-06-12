# 📋 Cadwork MCP Bridge - Manuell kopieren

Hier ist das **fertige Plugin** zum manuellen Kopieren nach Cadwork.

## 📁 Plugin-Struktur
```
API.x64\
└── MCPBridge\
    ├── MCPBridge.py          ← Hauptplugin mit GUI
    ├── bridge_server.py      ← Eingebetteter Bridge Server
    ├── plugin_info.xml       ← Plugin-Metadaten (mehrsprachig)
    └── README.md             ← Installationsanleitung
```

## 🎯 Installation (3 Schritte)

### 1. Cadwork Plugin-Verzeichnis finden:
**Cadwork 3D → Help → Info → "Userprofile" → 3d\API.x64**

### 2. MCPBridge Ordner kopieren:
Den kompletten **`MCPBridge`** Ordner nach **`API.x64`** kopieren

### 3. Cadwork neu starten:
**Window → Plugins → MCP Bridge** klicken

## ✨ Features

- **🎮 GUI-Kontrolle** - Einfache Bridge-Steuerung
- **🔄 Auto-Start** - Bridge automatisch aktivieren  
- **🔍 Connection Test** - Verbindung testen
- **🌐 Mehrsprachig** - DE/EN/FR/IT/ES Support
- **⚡ Embedded Server** - Läuft direkt im Plugin
- **📊 Status Monitor** - Echtzeit Bridge-Status

## 🚀 Nach Installation

```bash
# MCP Server starten
cd C:\cadworkMCP
python main.py
```

**Jetzt können externe Tools Cadwork steuern!** 🎉

## 📞 Support

Das Plugin ist **production-ready** und verbindet:
- **Cadwork** ↔ **MCP Bridge** ↔ **External Tools** (Claude, etc.)

**Ready to copy & use!** 📦✅
