"""
Embedded Bridge Server for the Cadwork Plugin
Simplified version that runs within the plugin environment
"""

import socket
import json
import sys
import os

# Basic command dispatcher for plugin mode
def dispatch_command(operation, args):
    """Basic dispatcher for essential operations in plugin mode"""
    try:
        if operation == "ping":
            return {"status": "ok", "message": "pong"}
        elif operation == "get_version_info":
            return {
                "status": "ok", 
                "version": "Cadwork MCP Bridge v1.0",
                "mode": "plugin",
                "port": 53002
            }
        elif operation == "get_all_element_ids":
            try:
                import element_controller as ec
                element_ids = ec.get_all_identifiable_element_ids()
                return {"status": "ok", "element_ids": element_ids}
            except Exception as e:
                return {"status": "error", "message": f"Element controller error: {e}"}
        elif operation == "create_beam":
            try:
                import element_controller as ec
                import cadwork
                
                p1 = cadwork.point_3d(args["p1"][0], args["p1"][1], args["p1"][2])
                p2 = cadwork.point_3d(args["p2"][0], args["p2"][1], args["p2"][2])
                p3 = None
                if args.get("p3"):
                    p3 = cadwork.point_3d(args["p3"][0], args["p3"][1], args["p3"][2])
                
                if p3:
                    element_id = ec.create_rectangular_beam_points(
                        args["width"], args["height"], p1, p2, p3
                    )
                else:
                    element_id = ec.create_rectangular_beam_points(
                        args["width"], args["height"], p1, p2
                    )
                
                return {"status": "ok", "element_id": element_id}
            except Exception as e:
                return {"status": "error", "message": f"Create beam error: {e}"}
        else:
            return {
                "status": "error", 
                "message": f"Operation '{operation}' not available in plugin mode. Use full bridge for complete functionality."
            }
    except Exception as e:
        return {"status": "error", "message": f"Dispatcher error: {str(e)}"}

HOST, PORT = "127.0.0.1", 53002

def socket_server():
    """Simplified socket server for plugin mode"""
    server_address = (str(HOST), int(PORT))
    srv = None
    
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(server_address)
        srv.listen(1)
        print(f"Plugin Bridge listening on {HOST}:{PORT}")
    except Exception as e:
        print(f"Bridge setup failed: {e}")
        if srv:
            srv.close()
        return
    
    # Main server loop
    while True:
        conn = None
        try:
            conn, addr = srv.accept()
            conn.settimeout(20.0)
            
            # Receive data
            raw_chunks = []
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                raw_chunks.append(chunk)
                
                # Check for complete JSON
                temp_data = b''.join(raw_chunks).strip()
                if temp_data.endswith(b'}'):
                    try:
                        json.loads(temp_data.decode('utf-8'))
                        break  # Complete JSON received
                    except json.JSONDecodeError:
                        continue  # Not complete yet
            
            if not raw_chunks:
                continue
                
            data = b''.join(raw_chunks)
            
            # Parse and process request
            try:
                request = json.loads(data.decode('utf-8'))
                operation = request.get("operation", "unknown")
                args = request.get("args", {})
                
                # Dispatch command
                response = dispatch_command(operation, args)
                
            except json.JSONDecodeError as e:
                response = {"status": "error", "message": f"Invalid JSON: {e}"}
            except Exception as e:
                response = {"status": "error", "message": f"Processing error: {e}"}
            
            # Send response
            response_json = json.dumps(response)
            conn.sendall(response_json.encode('utf-8'))
            
        except socket.timeout:
            print("Bridge connection timeout")
        except Exception as e:
            print(f"Bridge connection error: {e}")
            # Send error response if possible
            try:
                if conn:
                    error_response = {"status": "error", "message": f"Server error: {e}"}
                    conn.sendall(json.dumps(error_response).encode('utf-8'))
            except:
                pass
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

if __name__ == "__main__":
    socket_server()
