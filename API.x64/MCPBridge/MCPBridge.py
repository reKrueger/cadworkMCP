"""
Cadwork MCP Bridge Plugin
Auto-starts the MCP bridge server for external tool integration
"""

import sys
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# Add cadwork modules
import cadwork
import utility_controller as uc

# Add the main project to path (adjust if needed)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, "..", "..", "..", "cadworkMCP")
if os.path.exists(project_dir):
    sys.path.insert(0, project_dir)

# Bridge server state
bridge_thread = None
bridge_running = False

def start_bridge():
    """Start the MCP bridge server"""
    global bridge_thread, bridge_running
    
    if bridge_running:
        uc.print_to_console("MCP Bridge is already running!")
        return
    
    try:
        def run_bridge():
            global bridge_running
            bridge_running = True
            uc.print_to_console("Starting MCP Bridge on port 53002...")
            
            try:
                # Try to import and run the main bridge
                try:
                    from cadwork_bridge import socket_server
                    uc.print_to_console("MCP Bridge started successfully!")
                    socket_server()  # This will block until bridge is stopped
                except ImportError:
                    # Fallback: use embedded bridge
                    from bridge_server import socket_server
                    uc.print_to_console("MCP Bridge started (embedded mode)!")
                    socket_server()
                    
            except Exception as e:
                uc.print_to_console(f"Bridge error: {e}")
            finally:
                bridge_running = False
                uc.print_to_console("MCP Bridge stopped.")
        
        # Start bridge in separate thread
        bridge_thread = threading.Thread(target=run_bridge, daemon=True)
        bridge_thread.start()
        
        # Give it a moment to start
        time.sleep(1)
        
        if bridge_running:
            messagebox.showinfo("MCP Bridge", "Bridge started successfully!\nListening on port 53002")
        
    except Exception as e:
        uc.print_to_console(f"Failed to start bridge: {e}")
        messagebox.showerror("Error", f"Failed to start MCP Bridge:\n{e}")

def stop_bridge():
    """Stop the MCP bridge server"""
    global bridge_running
    
    if not bridge_running:
        uc.print_to_console("MCP Bridge is not running!")
        return
    
    bridge_running = False
    uc.print_to_console("Stopping MCP Bridge...")
    messagebox.showinfo("MCP Bridge", "Bridge stop requested.\nIt may take a moment to fully stop.")

def show_bridge_gui():
    """Show the bridge control GUI"""
    
    def on_start():
        start_bridge()
        update_status()
    
    def on_stop():
        stop_bridge()
        update_status()
    
    def update_status():
        if bridge_running:
            status_label.config(text="Status: Running", foreground="green")
            start_btn.config(state="disabled")
            stop_btn.config(state="normal")
        else:
            status_label.config(text="Status: Stopped", foreground="red")
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
    
    def on_test():
        """Test bridge connection"""
        if not bridge_running:
            messagebox.showwarning("Test", "Bridge is not running!")
            return
        
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(("127.0.0.1", 53002))
            sock.close()
            
            if result == 0:
                messagebox.showinfo("Test", "Bridge connection successful!")
            else:
                messagebox.showwarning("Test", "Bridge not responding on port 53002")
        except Exception as e:
            messagebox.showerror("Test", f"Connection test failed:\n{e}")
    
    # Create GUI window
    root = tk.Tk()
    root.title("Cadwork MCP Bridge Control")
    root.geometry("400x300")
    root.resizable(False, False)
    
    # Header
    header_frame = ttk.Frame(root)
    header_frame.pack(fill="x", padx=10, pady=10)
    
    title_label = ttk.Label(header_frame, text="MCP Bridge Control", font=("Arial", 16, "bold"))
    title_label.pack()
    
    subtitle_label = ttk.Label(header_frame, text="External Tool Integration for Cadwork")
    subtitle_label.pack()
    
    # Status frame
    status_frame = ttk.LabelFrame(root, text="Bridge Status", padding=10)
    status_frame.pack(fill="x", padx=10, pady=5)
    
    status_label = ttk.Label(status_frame, text="Status: Unknown", font=("Arial", 12))
    status_label.pack()
    
    port_label = ttk.Label(status_frame, text="Port: 53002")
    port_label.pack()
    
    # Control frame
    control_frame = ttk.LabelFrame(root, text="Controls", padding=10)
    control_frame.pack(fill="x", padx=10, pady=5)
    
    button_frame = ttk.Frame(control_frame)
    button_frame.pack()
    
    start_btn = ttk.Button(button_frame, text="Start Bridge", command=on_start, width=12)
    start_btn.pack(side="left", padx=5)
    
    stop_btn = ttk.Button(button_frame, text="Stop Bridge", command=on_stop, width=12)
    stop_btn.pack(side="left", padx=5)
    
    test_btn = ttk.Button(button_frame, text="Test Connection", command=on_test, width=15)
    test_btn.pack(side="left", padx=5)
    
    # Info frame
    info_frame = ttk.LabelFrame(root, text="Information", padding=10)
    info_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    info_text = tk.Text(info_frame, height=6, wrap="word", state="disabled")
    info_text.pack(fill="both", expand=True)
    
    # Add info content
    info_content = """The MCP Bridge enables external tools like Claude to interact with Cadwork through a standardized interface.

When running:
• External tools can create and modify elements
• Automated workflows become possible
• AI assistants can help with design tasks

The bridge runs on localhost port 53002 and is only accessible from your computer."""
    
    info_text.config(state="normal")
    info_text.insert("1.0", info_content)
    info_text.config(state="disabled")
    
    # Update initial status
    update_status()
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"400x300+{x}+{y}")
    
    root.mainloop()

def main():
    """Main plugin entry point"""
    
    # Show welcome message
    result = uc.get_user_bool("Start MCP Bridge Control GUI?", True)
    
    if result:
        show_bridge_gui()
    else:
        # Quick start option
        quick_start = uc.get_user_bool("Start MCP Bridge directly (no GUI)?", False)
        if quick_start:
            start_bridge()

# Entry point for the plugin
if __name__ == "__main__":
    main()
