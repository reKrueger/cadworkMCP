"""
Cadwork MCP Bridge Plugin - Simple Start/Stop GUI
Executes the MCP bridge start script with simple controls
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Cadwork imports
import utility_controller as uc

# Global variables
bridge_running = False

def start_bridge() -> bool:
    """Start the MCP bridge by executing start.txt"""
    global bridge_running
    
    if bridge_running:
        return False
    
    try:
        # Change to the MCP directory and set up environment like in console
        original_dir = os.getcwd()
        bridge_dir = r'C:\cadworkMCP'
        
        try:
            # Set working directory
            os.chdir(bridge_dir)
            
            # Add to Python path if not already there
            if bridge_dir not in sys.path:
                sys.path.insert(0, bridge_dir)
            
            # Read and execute the start script
            with open(os.path.join(bridge_dir, 'start.txt'), 'r') as f:
                script_content = f.read()
            
            # Execute in global namespace like console does
            exec(script_content, globals())
            
            bridge_running = True
            uc.print_to_console("MCP Bridge started successfully")
            return True
            
        finally:
            # Restore original directory
            os.chdir(original_dir)
        
    except Exception as e:
        uc.print_to_console(f"Failed to start bridge: {e}")
        return False

def stop_bridge() -> None:
    """Stop the MCP bridge"""
    global bridge_running
    
    bridge_running = False
    uc.print_to_console("MCP Bridge stopped")

class BridgeGUI:
    """Simple GUI for bridge control"""
    
    def __init__(self) -> None:
        self.root = None
        self.status_label = None
        self.start_btn = None
        self.stop_btn = None
    
    def create_gui(self) -> None:
        """Create the GUI"""
        self.root = tk.Tk()
        self.root.title("MCP Bridge Control")
        self.root.geometry("350x200")
        self.root.resizable(False, False)
        
        # Title
        title_label = ttk.Label(self.root, text="Cadwork MCP Bridge", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=15)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Status: Stopped", 
                                     font=("Arial", 11), foreground="red")
        self.status_label.pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="Start Bridge", 
                                   command=self.on_start, width=12)
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Bridge", 
                                  command=self.on_stop, width=12, state="disabled")
        self.stop_btn.pack(side="left", padx=10)
        
        # Info
        info_label = ttk.Label(self.root, text="Port: 53002", 
                              font=("Arial", 9), foreground="gray")
        info_label.pack(pady=5)
        
        # Center window
        self.center_window()
    
    def center_window(self) -> None:
        """Center window on screen"""
        self.root.update_idletasks()
        width, height = 350, 200
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_start(self) -> None:
        """Handle start button"""
        success = start_bridge()
        if success:
            messagebox.showinfo("Bridge", "MCP Bridge started!")
        else:
            messagebox.showerror("Error", "Failed to start bridge!")
        self.update_status()
    
    def on_stop(self) -> None:
        """Handle stop button"""
        stop_bridge()
        messagebox.showinfo("Bridge", "MCP Bridge stopped!")
        self.update_status()
    
    def update_status(self) -> None:
        """Update status display"""
        if bridge_running:
            self.status_label.config(text="Status: Running", foreground="green")
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.status_label.config(text="Status: Stopped", foreground="red")
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
    
    def show(self) -> None:
        """Show the GUI"""
        self.create_gui()
        self.root.mainloop()

def main() -> None:
    """Main plugin entry point"""
    try:
        uc.print_to_console("Starting MCP Bridge Plugin...")
        gui = BridgeGUI()
        gui.show()
    except Exception as e:
        uc.print_to_console(f"Plugin error: {e}")
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
