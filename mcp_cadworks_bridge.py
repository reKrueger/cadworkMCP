"""
cadwork_mcp.py  – minimal MCP bridge (v3, proper point_3d conversion, added logging)
"""

import socket, json, threading, traceback
import utility_controller as uc
import element_controller as ec
import geometry_controller as gc
import attribute_controller as ac
import material_controller as mc
import cadwork             
HOST, PORT = "127.0.0.1", 53002          # keep your chosen port

# ───────── helpers ────────────────────────────────────────────────────────────
def to_pt(v):
    """Convert [x,y,z] list/tuple -> cadwork.point_3d"""
    # Add basic type/length checking for robustness
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        raise ValueError(f"Invalid point format: {v}. Expected list/tuple of 3 numbers.")
    try:
        return cadwork.point_3d(float(v[0]), float(v[1]), float(v[2]))
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid coordinate in point {v}: {e}")

def pt_to_list(pt: cadwork.point_3d) -> list[float]:
    """Convert cadwork.point_3d -> [x, y, z] list"""
    if not isinstance(pt, cadwork.point_3d):
        # Return a default or raise error if input is not a point_3d
        print(f"Warning: pt_to_list received non-point_3d: {type(pt)}")
        return [0.0, 0.0, 0.0] # Or raise TypeError
    return [pt.x, pt.y, pt.z]

# ───────── dispatcher ─────────────────────────────────────────────────────────
def handle(msg: dict) -> dict:
    op = msg.get("operation")
    print(f"▶ Dispatcher received operation: {op}") # Log received operation

    if not isinstance(msg, dict):
        print("Error: Invalid message format, expected JSON object")
        return {"status": "error", "message": "Invalid message format, expected JSON object"}

    args = msg.get("args", {}) # Get args, default to empty dict if missing

    if not isinstance(args, dict):
         print("Error: Invalid 'args' format, expected JSON object")
         return {"status": "error", "message": "Invalid 'args' format, expected JSON object"}

    if op == "ping":
        print("Handshake ping received.")
        return {"status": "ok", "message": "pong"}

    if op == "get_version_info": # Example handler for the other tool
        try:
            # --- Attempt to get Cadwork version ---
            cw_version_str = str(uc.get_3d_version())  # Correct API call per docs
            print(f"Successfully retrieved Cadwork version: {cw_version_str}")
            return {"status": "ok", "cw_version": cw_version_str, "plugin_version": "0.1.1_attr"}
        except AttributeError:
            print("Error: utility_controller has no 'get_3d_version'")
            return {"status": "error", "message": "Failed to get version info: Function not found in utility_controller"}
        except Exception as e:
            print(f"Error in get_version_info: {e}")
            traceback.print_exc()
            return {"status": "error", "message": f"Failed to get version info: {e}"}

    if op == "get_model_name":
        try:
            model_name = uc.get_3d_file_name()
            print(f"Retrieved model name: {model_name}")
            return {"status": "ok", "name": model_name or "(unsaved model)"}
        except Exception as e:
            print(f"Error in get_model_name: {e}")
            traceback.print_exc()
            return {"status": "error", "message": f"Failed to get model name: {e}"}

    if op == "create_beam":
        try:
            print(f"Handling 'create_beam' with args: {args}") # Log args received by handler
            # Input validation within the handler
            required_args = ["p1", "p2", "width", "height"]
            if not all(key in args for key in required_args):
                 missing = [key for key in required_args if key not in args]
                 err_msg = f"Missing required arguments for create_beam: {missing}"
                 print(f"Error: {err_msg}")
                 raise ValueError(err_msg)

            p1 = to_pt(args["p1"])
            p2 = to_pt(args["p2"])
            # Use args.get for optional p3, provide default if not present *or* if None
            p3_raw = args.get("p3")
            if p3_raw is None:
                # Default p3 is point vertically above p1 (positive Z)
                p3 = cadwork.point_3d(p1.x, p1.y, p1.z + 1.0) # Use point_3d directly
                print(f"Using default p3 (vertical): {p3.x}, {p3.y}, {p3.z}")
            else:
                p3 = to_pt(p3_raw)
                print(f"Using provided p3: {p3_raw}")

            width = float(args["width"])
            height = float(args["height"])

            if width <= 0 or height <= 0:
                 err_msg = f"Width ({width}) and height ({height}) must be positive numbers."
                 print(f"Error: {err_msg}")
                 raise ValueError(err_msg)

            # Log the final points being used - accessing members ensures they are valid point_3d
            print(f"Calling ec.create_rectangular_beam_points with w={width}, h={height}, "
                  f"p1=({p1.x},{p1.y},{p1.z}), p2=({p2.x},{p2.y},{p2.z}), p3=({p3.x},{p3.y},{p3.z})")

            beam_id = ec.create_rectangular_beam_points(width, height, p1, p2, p3)

            # Check if beam_id seems valid (often > 0 for success)
            if isinstance(beam_id, int) and beam_id >= 0: # Adjust if Cadwork uses different success indicators
                print(f"Beam created successfully, ID: {beam_id}")
                return {"status": "ok", "id": beam_id}
            else:
                # Handle cases where Cadwork might return 0 or negative on failure without exception
                err_msg = f"ec.create_rectangular_beam_points returned unexpected value: {beam_id}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_id": beam_id}

        except (ValueError, TypeError) as e: # Catch specific conversion/validation errors
             print(f"Input Error in create_beam: {e}")
             # traceback.print_exc() # Keep commented unless needed
             return {"status": "error", "message": f"Invalid input for create_beam: {e}"}
        except Exception as e: # Catch other Cadwork API errors
            print(f"Cadwork API Error in create_beam: {e}")
            traceback.print_exc() # Print full traceback for unexpected errors
            # Try to provide a more specific error message if possible
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_element_info":
        try:
            print(f"Handling 'get_element_info' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg) # Ensure it's an integer

            print(f"Retrieving info for element ID: {element_id}")

            # Retrieve geometric information
            p1 = gc.get_p1(element_id)
            p2 = gc.get_p2(element_id)
            p3 = gc.get_p3(element_id)
            vec_x = gc.get_xl(element_id)
            vec_y = gc.get_yl(element_id)
            vec_z = gc.get_zl(element_id)

            # Retrieve attributes with individual error handling
            attributes = {}
            # Standard attributes to fetch for this tool
            standard_attrs_to_get = {
                "name": ac.get_name,
                "group": ac.get_group,
                "subgroup": ac.get_subgroup,
                "comment": ac.get_comment
                # Add others here if needed by this specific tool
            }
            for attr_name, getter_func in standard_attrs_to_get.items():
                try:
                    value = getter_func(element_id)
                    attributes[attr_name] = value
                    print(f"  - Retrieved {attr_name}: {value}")
                except Exception as e:
                    print(f"  - Warning: Could not get {attr_name} for element {element_id}: {e}")
                    attributes[attr_name] = None # Indicate failure to retrieve

            # Get Material (special handling)
            try:
                material_id = ac.get_material(element_id) # Assumed function
                if material_id is not None and material_id > 0: # Check for valid ID
                    material_name = mc.get_name(material_id)
                    attributes['material'] = material_name
                    print(f"  - Retrieved material: {material_name} (ID: {material_id})")
                else:
                    print(f"  - Element {element_id} has no material assigned (ID: {material_id})")
                    attributes['material'] = None
            except AttributeError:
                 print(f"  - Warning: Function ac.get_material or mc.get_name not found.")
                 attributes['material'] = "Error: Function not available" # Specific error message
            except Exception as e:
                print(f"  - Warning: Could not get material for element {element_id}: {e}")
                attributes['material'] = None # Indicate failure to retrieve


            # Construct the full info dictionary
            element_info = {
                "element_id": element_id,
                "geometry": {
                    "p1": pt_to_list(p1),
                    "p2": pt_to_list(p2),
                    "p3": pt_to_list(p3),
                    "vector_x": pt_to_list(vec_x),
                    "vector_y": pt_to_list(vec_y),
                    "vector_z": pt_to_list(vec_z),
                },
                "attributes": attributes # Include fetched attributes
            }
            print(f"Successfully retrieved info for element {element_id}: {element_info}")
            return {"status": "ok", "info": element_info}

        except (ValueError, TypeError) as e:
             print(f"Input Error in get_element_info: {e}")
             return {"status": "error", "message": f"Invalid input for get_element_info: {e}"}
        except Exception as e: # Catch Cadwork API errors (e.g., invalid ID for geometry)
            print(f"Cadwork API Error in get_element_info for ID {args.get('element_id')}: {e}")
            # More robust check for invalid ID errors across different Cadwork versions/contexts
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str or "elementid not valid" in err_str:
                 return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "create_panel":
        try:
            print(f"Handling 'create_panel' with args: {args}") # Log args received by handler
            # Input validation within the handler
            required_args = ["p1", "p2", "width", "thickness"]
            if not all(key in args for key in required_args):
                 missing = [key for key in required_args if key not in args]
                 err_msg = f"Missing required arguments for create_panel: {missing}"
                 print(f"Error: {err_msg}")
                 raise ValueError(err_msg)

            p1 = to_pt(args["p1"])
            p2 = to_pt(args["p2"])
            # Use args.get for optional p3, provide default if not present *or* if None
            p3_raw = args.get("p3")
            if p3_raw is None:
                # Default p3 is point vertically above p1 (positive Z)
                p3 = cadwork.point_3d(p1.x, p1.y, p1.z + 1.0) # Use point_3d directly
                print(f"Using default p3 (vertical): {p3.x}, {p3.y}, {p3.z}")
            else:
                p3 = to_pt(p3_raw)
                print(f"Using provided p3: {p3_raw}")

            width = float(args["width"])
            thickness = float(args["thickness"])

            if width <= 0 or thickness <= 0:
                 err_msg = f"Width ({width}) and thickness ({thickness}) must be positive numbers."
                 print(f"Error: {err_msg}")
                 raise ValueError(err_msg)

            # Log the final points being used - accessing members ensures they are valid point_3d
            print(f"Calling ec.create_rectangular_panel_points with w={width}, t={thickness}, "
                  f"p1=({p1.x},{p1.y},{p1.z}), p2=({p2.x},{p2.y},{p2.z}), p3=({p3.x},{p3.y},{p3.z})")

            panel_id = ec.create_rectangular_panel_points(width, thickness, p1, p2, p3)

            # Check if panel_id seems valid (often > 0 for success)
            if isinstance(panel_id, int) and panel_id >= 0: # Adjust if Cadwork uses different success indicators
                print(f"Panel created successfully, ID: {panel_id}")
                return {"status": "ok", "id": panel_id}
            else:
                # Handle cases where Cadwork might return 0 or negative on failure without exception
                err_msg = f"ec.create_rectangular_panel_points returned unexpected value: {panel_id}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_id": panel_id}

        except (ValueError, TypeError) as e: # Catch specific conversion/validation errors
             print(f"Input Error in create_panel: {e}")
             # traceback.print_exc() # Keep commented unless needed
             return {"status": "error", "message": f"Invalid input for create_panel: {e}"}
        except Exception as e: # Catch other Cadwork API errors
            print(f"Cadwork API Error in create_panel: {e}")
            traceback.print_exc() # Print full traceback for unexpected errors
            # Try to provide a more specific error message if possible
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_active_element_ids":
        try:
            print(f"Handling 'get_active_element_ids' with args: {args}")
            active_element_ids = ec.get_active_identifiable_element_ids()
            print(f"Retrieved active element IDs: {active_element_ids}")
            return {"status": "ok", "element_ids": active_element_ids}
        except AttributeError as ae:
             # Handle case where this guess is also wrong
             print(f"AttributeError in get_active_element_ids: {ae}")
             traceback.print_exc()
             return {"status": "error", "message": f"Failed to find function for getting active elements: {ae}"}
        except Exception as e:
            print(f"Error in get_active_element_ids: {e}")
            traceback.print_exc()
            # Ensure the key is "message" for the error response
            return {"status": "error", "message": f"Failed to get active element IDs: {e}"}

    # --- NEW TOOL HANDLERS --- === START === --- === === === === === === ===

    if op == "get_standard_attributes":
        try:
            print(f"Handling 'get_standard_attributes' with args: {args}")
            element_ids_arg = args.get("element_ids")
            if not isinstance(element_ids_arg, list):
                raise ValueError("'element_ids' must be a list.")

            element_ids = [int(eid) for eid in element_ids_arg] # Validate elements are ints
            results = {}
            # Define which standard attributes to get and their corresponding functions
            standard_attrs_map = {
                "name": ac.get_name,
                "group": ac.get_group,
                "subgroup": ac.get_subgroup,
                "comment": ac.get_comment
            }

            print(f"Processing {len(element_ids)} elements for standard attributes...")
            for eid in element_ids:
                print(f"  Processing element ID: {eid}")
                elem_attrs = {}
                # Get standard named attributes
                for attr_key, getter_func in standard_attrs_map.items():
                    try:
                        value = getter_func(eid)
                        elem_attrs[attr_key] = value
                        # print(f"    - Got {attr_key}: {value}") # Verbose log
                    except Exception as e:
                        print(f"    - ERROR getting {attr_key} for element {eid}: {e}")
                        elem_attrs[attr_key] = f"ERROR: {type(e).__name__}" # Store error marker

                # Get Material (Corrected approach)
                try:
                    material_name = ac.get_element_material_name(eid)
                    elem_attrs['material'] = material_name if material_name else None # Store None if empty name returned
                    # print(f"    - Got material: {material_name}") # Verbose log
                except AttributeError as ae:
                    print(f"    - ERROR getting material name for element {eid}: Function not found ({ae})")
                    elem_attrs['material'] = "ERROR: FunctionNotFound"
                except Exception as e:
                    print(f"    - ERROR getting material name for element {eid}: {e}")
                    elem_attrs['material'] = f"ERROR: {type(e).__name__}"

                results[eid] = elem_attrs # Store attributes for this element ID (using int key)

            print("Finished processing standard attributes.")
            return {"status": "ok", "attributes_by_id": results}

        except (ValueError, TypeError) as e:
             print(f"Input Error in get_standard_attributes: {e}")
             return {"status": "error", "message": f"Invalid input for get_standard_attributes: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_standard_attributes: {e}")
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error in get_standard_attributes: {type(e).__name__} - {e}"}

    if op == "get_user_attributes":
        try:
            print(f"Handling 'get_user_attributes' with args: {args}")
            element_ids_arg = args.get("element_ids")
            attr_numbers_arg = args.get("attribute_numbers")

            if not isinstance(element_ids_arg, list):
                raise ValueError("'element_ids' must be a list.")
            if not isinstance(attr_numbers_arg, list):
                raise ValueError("'attribute_numbers' must be a list.")

            element_ids = [int(eid) for eid in element_ids_arg]
            attribute_numbers = [int(num) for num in attr_numbers_arg]
            if not all(num > 0 for num in attribute_numbers):
                raise ValueError("Attribute numbers must be positive integers.")

            results = {}
            print(f"Processing {len(element_ids)} elements for user attributes {attribute_numbers}...")
            for eid in element_ids:
                print(f"  Processing element ID: {eid}")
                user_attrs = {}
                for num in attribute_numbers:
                    try:
                        value = ac.get_user_attribute(eid, num)
                        user_attrs[num] = value # Store with int key for number
                        # print(f"    - Got user attr {num}: {value}") # Verbose log
                    except Exception as e:
                         print(f"    - ERROR getting user attribute {num} for element {eid}: {e}")
                         user_attrs[num] = f"ERROR: {type(e).__name__}" # Store error marker
                results[eid] = user_attrs # Store with int key for element ID

            print("Finished processing user attributes.")
            return {"status": "ok", "user_attributes_by_id": results}

        except (ValueError, TypeError) as e:
             print(f"Input Error in get_user_attributes: {e}")
             return {"status": "error", "message": f"Invalid input for get_user_attributes: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_user_attributes: {e}")
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error in get_user_attributes: {type(e).__name__} - {e}"}

    if op == "list_defined_user_attributes":
        try:
            print(f"Handling 'list_defined_user_attributes' with args: {args}")
            defined_attributes = {}
            # Loop through a reasonable range, e.g., 1 to 100
            max_check_number = 100
            print(f"Checking user attribute numbers 1 to {max_check_number} for defined names...")
            for i in range(1, max_check_number + 1):
                try:
                    name = ac.get_user_attribute_name(i)
                    # Only add if the name is not None and not an empty string
                    if name:
                        print(f"  - Found definition for {i}: '{name}'")
                        defined_attributes[i] = name # Store with int key
                    # else: # Verbose log
                    #     print(f"  - Attribute {i} is not defined (name: {name})")
                except AttributeError as ae:
                    # This likely means the function itself is missing
                    print(f"ERROR: Function ac.get_user_attribute_name not found. Cannot list definitions. ({ae})")
                    raise # Re-raise to be caught by the outer handler
                except Exception as e:
                    # Log error for this specific number but continue checking others
                    print(f"  - Error checking attribute {i}: {e} - Skipping this number.")

            print(f"Finished listing defined user attributes ({len(defined_attributes)} found).")
            return {"status": "ok", "defined_attributes": defined_attributes}

        except AttributeError as ae:
             # Handle the case where the function doesn't exist at all
             print(f"Input Error in list_defined_user_attributes: {ae}")
             return {"status": "error", "message": f"Function ac.get_user_attribute_name not available in this Cadwork version.", "details": str(ae)}
        except Exception as e:
            print(f"Cadwork API Error in list_defined_user_attributes: {e}")
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error in list_defined_user_attributes: {type(e).__name__} - {e}"}

    # --- NEW TOOL HANDLERS --- === END === === === === === === === === ===

    # --- GEOMETRY TOOL HANDLERS --- === START === === === === === === === ===

    if op == "get_element_width":
        try:
            print(f"Handling 'get_element_width' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg)
            print(f"Retrieving width for element ID: {element_id}")

            # Call the Cadwork geometry controller function
            width = gc.get_width(element_id)
            
            if isinstance(width, (int, float)):
                print(f"Successfully retrieved width for element {element_id}: {width} mm")
                return {"status": "ok", "width": float(width)}
            else:
                err_msg = f"gc.get_width returned unexpected value: {width}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_value": width}

        except (ValueError, TypeError) as e:
            print(f"Input Error in get_element_width: {e}")
            return {"status": "error", "message": f"Invalid input for get_element_width: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_element_width for ID {args.get('element_id')}: {e}")
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str:
                return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_element_height":
        try:
            print(f"Handling 'get_element_height' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg)
            print(f"Retrieving height for element ID: {element_id}")

            # Call the Cadwork geometry controller function
            height = gc.get_height(element_id)
            
            if isinstance(height, (int, float)):
                print(f"Successfully retrieved height for element {element_id}: {height} mm")
                return {"status": "ok", "height": float(height)}
            else:
                err_msg = f"gc.get_height returned unexpected value: {height}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_value": height}

        except (ValueError, TypeError) as e:
            print(f"Input Error in get_element_height: {e}")
            return {"status": "error", "message": f"Invalid input for get_element_height: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_element_height for ID {args.get('element_id')}: {e}")
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str:
                return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_element_length":
        try:
            print(f"Handling 'get_element_length' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg)
            print(f"Retrieving length for element ID: {element_id}")

            # Call the Cadwork geometry controller function
            length = gc.get_length(element_id)
            
            if isinstance(length, (int, float)):
                print(f"Successfully retrieved length for element {element_id}: {length} mm")
                return {"status": "ok", "length": float(length)}
            else:
                err_msg = f"gc.get_length returned unexpected value: {length}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_value": length}

        except (ValueError, TypeError) as e:
            print(f"Input Error in get_element_length: {e}")
            return {"status": "error", "message": f"Invalid input for get_element_length: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_element_length for ID {args.get('element_id')}: {e}")
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str:
                return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_element_volume":
        try:
            print(f"Handling 'get_element_volume' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg)
            print(f"Retrieving volume for element ID: {element_id}")

            # Call the Cadwork geometry controller function
            volume = gc.get_volume(element_id)
            
            if isinstance(volume, (int, float)):
                print(f"Successfully retrieved volume for element {element_id}: {volume} mm³")
                return {"status": "ok", "volume": float(volume)}
            else:
                err_msg = f"gc.get_volume returned unexpected value: {volume}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_value": volume}

        except (ValueError, TypeError) as e:
            print(f"Input Error in get_element_volume: {e}")
            return {"status": "error", "message": f"Invalid input for get_element_volume: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_element_volume for ID {args.get('element_id')}: {e}")
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str:
                return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    if op == "get_element_weight":
        try:
            print(f"Handling 'get_element_weight' with args: {args}")
            element_id_arg = args.get("element_id")
            if element_id_arg is None:
                raise ValueError("Missing required argument: element_id")

            element_id = int(element_id_arg)
            print(f"Retrieving weight for element ID: {element_id}")

            # Call the Cadwork geometry controller function
            weight = gc.get_weight(element_id)
            
            if isinstance(weight, (int, float)):
                print(f"Successfully retrieved weight for element {element_id}: {weight} kg")
                return {"status": "ok", "weight": float(weight)}
            else:
                err_msg = f"gc.get_weight returned unexpected value: {weight}"
                print(f"Error: {err_msg}")
                return {"status": "error", "message": err_msg, "returned_value": weight}

        except (ValueError, TypeError) as e:
            print(f"Input Error in get_element_weight: {e}")
            return {"status": "error", "message": f"Invalid input for get_element_weight: {e}"}
        except Exception as e:
            print(f"Cadwork API Error in get_element_weight for ID {args.get('element_id')}: {e}")
            err_str = str(e).lower()
            if "element not found" in err_str or "invalid element id" in err_str:
                return {"status": "error", "message": f"Element ID {args.get('element_id')} not found or invalid."}
            traceback.print_exc()
            return {"status": "error", "message": f"Cadwork API error: {type(e).__name__} - {e}"}

    # --- GEOMETRY TOOL HANDLERS --- === END === === === === === === === ===

    # Fallback for unknown operations
    print(f"Unknown operation received: {op}")
    return {"status": "error", "message": f"unknown operation '{op}'"}


# ───────── socket thread ──────────────────────────────────────────────────────
def socket_server():
    # Ensure HOST is a string and PORT is an int
    host_str = str(HOST)
    port_int = int(PORT)
    server_address = (host_str, port_int)
    srv = None # Define srv before try block

    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Option to allow reusing the address quickly after script restart
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Attempting to bind to {server_address}...")
        srv.bind(server_address)
        print(f"Socket bound successfully.")
        srv.listen(1) # Listen for only one connection at a time
        print(f"✓ cadwork_mcp listening on {host_str}:{port_int}")
    except Exception as e:
        print(f"!!! Server socket setup failed on {server_address}: {e} !!!")
        traceback.print_exc()
        if srv:
             srv.close() # Clean up socket if partially created
        return # Stop the thread if setup fails

    # --- Main Server Loop ---
    while True:
        conn = None # Ensure conn is defined for finally block
        addr = None
        try:
            print(f"\n[{threading.current_thread().name}] Waiting for incoming connection...") # Log thread name
            conn, addr = srv.accept() # Blocking call
            print(f"[{threading.current_thread().name}] Connection accepted from: {addr}") # Log thread name

            # Set timeout for the accepted connection's operations
            conn.settimeout(20.0) # e.g., 20 seconds timeout for recv/send

            print(f"[{threading.current_thread().name}] Attempting to receive data...")
            # More robust receive loop: read untildelimiter or timeout/error
            raw_chunks = []
            bytes_received = 0
            raw = b'' # Initialize raw
            try:
                while True:
                    # print(f"[{threading.current_thread().name}] Calling conn.recv(4096)...") # Verbose log
                    chunk = conn.recv(4096) # Read in chunks
                    if not chunk:
                        print(f"[{threading.current_thread().name}] Connection closed by client ({addr}) during receive.")
                        break # Client closed connection gracefully
                    # print(f"[{threading.current_thread().name}] Received chunk of size {len(chunk)}.") # Verbose log
                    raw_chunks.append(chunk)
                    bytes_received += len(chunk)

                    # *** Basic JSON Detection Logic ***
                    # Look for balanced braces. This is imperfect but better than nothing.
                    # A better protocol would use length prefixing or a clear delimiter.
                    temp_data = b''.join(raw_chunks).strip()
                    if temp_data.startswith(b'{') and temp_data.endswith(b'}'):
                         try:
                              # Try to parse; if it works, assume we got a full JSON object
                              json.loads(temp_data.decode('utf-8'))
                              print(f"[{threading.current_thread().name}] Received data looks like complete JSON ({bytes_received} bytes).")
                              break
                         except (json.JSONDecodeError, UnicodeDecodeError):
                              # Incomplete JSON or bad encoding, keep receiving
                              # print(f"[{threading.current_thread().name}] Data received but not valid JSON yet, continuing...") # Verbose
                              pass

                    if bytes_received > 65536: # Safety break for large messages
                         print(f"[{threading.current_thread().name}] Warning: Received > 65536 bytes from {addr}, potential issue or large message.")
                         # Decide whether to break or continue based on your expected message sizes
                         break # Breaking for safety here

            except socket.timeout:
                print(f"[{threading.current_thread().name}] Socket timeout ({conn.gettimeout()}s) while receiving data from {addr}. Received {bytes_received} bytes so far.")
                # If we received *some* data before timeout, try processing it
                if not raw_chunks:
                     print(f"[{threading.current_thread().name}] No data received before timeout.")
                     continue # Go back to waiting for connection
            except ConnectionResetError:
                 print(f"[{threading.current_thread().name}] Connection reset by peer ({addr}) during receive.")
                 continue # Go back to waiting for connection
            except Exception as recv_err:
                 print(f"[{threading.current_thread().name}] Error during recv from {addr}: {recv_err}")
                 traceback.print_exc()
                 continue # Go back to waiting for connection

            # --- Process received data ---
            if not raw_chunks:
                print(f"[{threading.current_thread().name}] No data received or connection closed early by {addr}.")
                continue # Go back to waiting for connection

            raw = b''.join(raw_chunks)
            print(f"[{threading.current_thread().name}] Received total {len(raw)} bytes from {addr}.")
            if len(raw) > 0:
                # Log only first few hundred bytes for readability
                log_snippet = raw[:500].decode('utf-8', errors='replace') # Decode safely for logging
                print(f"[{threading.current_thread().name}] Raw data received (first 500 bytes): {log_snippet}")
                decoded_data = None
                response = None # Ensure response is defined
                try:
                    print(f"[{threading.current_thread().name}] Attempting to decode UTF-8...")
                    decoded_data = raw.decode('utf-8')
                    # print(f"[{threading.current_thread().name}] Decoded data: {decoded_data}") # Verbose log
                    print(f"[{threading.current_thread().name}] Attempting to parse JSON...")
                    parsed_msg = json.loads(decoded_data)
                    print(f"[{threading.current_thread().name}] JSON parsed successfully: {parsed_msg}")
                    print(f"[{threading.current_thread().name}] Dispatching to handle function...")
                    # --- Call the actual handler ---
                    response = handle(parsed_msg)
                    # --------------------------------
                    print(f"[{threading.current_thread().name}] Handle function returned: {response}")
                    if response is None:
                         print(f"[{threading.current_thread().name}] !!! Warning: handle function returned None for op {parsed_msg.get('operation')} !!!")
                         response = {"status": "error", "message": "Handler function returned None"}

                    response_bytes = json.dumps(response).encode('utf-8')
                    response_snippet = response_bytes[:500].decode('utf-8', errors='replace')
                    print(f"[{threading.current_thread().name}] Sending response ({len(response_bytes)} bytes): {response_snippet}...")
                    conn.sendall(response_bytes)
                    print(f"[{threading.current_thread().name}] Response sent to {addr}.")

                except UnicodeDecodeError as ude:
                    print(f"[{threading.current_thread().name}] !!! Unicode Decode Error: {ude} !!!")
                    print(f"[{threading.current_thread().name}] Problematic raw data (approx location):", raw[max(0, ude.start-20):ude.end+20])
                    response = {"status": "error", "message": f"Invalid UTF-8 data received: {ude}"}
                except json.JSONDecodeError as jde:
                    print(f"[{threading.current_thread().name}] !!! JSON Decode Error: {jde} !!!")
                    # Log the decoded string if decoding worked, otherwise raw bytes
                    if decoded_data:
                         print(f"[{threading.current_thread().name}] Problematic decoded data: {decoded_data}")
                    else:
                         print(f"[{threading.current_thread().name}] Problematic raw data: {raw}")
                    response = {"status": "error", "message": f"Invalid JSON format received: {jde}"}
                except Exception as handle_err:
                    print(f"[{threading.current_thread().name}] !!! Error during handle/response phase: {handle_err} !!!")
                    traceback.print_exc()
                    response = {"status": "error", "message": f"Internal server error: {type(handle_err).__name__} - {handle_err}"}

                # --- Attempt to send error response if needed ---
                if response and response.get("status") == "error":
                    try:
                        print(f"[{threading.current_thread().name}] Attempting to send error response back to {addr}...")
                        error_bytes = json.dumps(response).encode('utf-8')
                        conn.sendall(error_bytes)
                        print(f"[{threading.current_thread().name}] Error response sent.")
                    except Exception as send_err:
                         print(f"[{threading.current_thread().name}] !!! Failed to send error response to {addr}: {send_err} !!!")

            else:
                print(f"[{threading.current_thread().name}] Received zero bytes after loop from {addr}, closing connection.")

        except socket.timeout:
            # This timeout is for the conn.accept() call if srv.settimeout() was used (it isn't here)
            # Or potentially relates to the conn.settimeout() if error occurs before recv loop
            print(f"[{threading.current_thread().name}] Socket timeout occurred for {addr}. (Timeout: {conn.gettimeout() if conn else 'N/A'}s)")
        except ConnectionResetError:
            # This happens if the client disconnects abruptly *after* accept() but before/during send/recv
            print(f"[{threading.current_thread().name}] Connection reset by peer {addr}.")
        except Exception as e:
            # Catch errors during accept or general connection handling loop
            print(f"[{threading.current_thread().name}] Error in connection handling loop (client: {addr}):")
            traceback.print_exc()
        finally:
             if conn:
                 print(f"[{threading.current_thread().name}] Closing connection to {addr}.")
                 try:
                     conn.shutdown(socket.SHUT_RDWR) # Attempt graceful shutdown
                 except OSError:
                      pass # Ignore if already closed
                 except Exception as shut_err:
                      print(f"[{threading.current_thread().name}] Error during socket shutdown for {addr}: {shut_err}")
                 try:
                      conn.close() # Ensure connection is closed
                 except Exception as close_err:
                      print(f"[{threading.current_thread().name}] Error closing socket for {addr}: {close_err}")
             print(f"[{threading.current_thread().name}] Finished handling connection from {addr}.")
             # Loop continues, waiting for next connection


# ───────── main execution ─────────────────────────────────────────────────────
# Global flag to signal shutdown
shutdown_event = threading.Event()

def signal_handler(signum, frame):
    """Handle signals like Ctrl+C"""
    print(f"\nSignal {signum} received, initiating shutdown...")
    shutdown_event.set()
    # Optionally, try to connect to the server socket to unblock accept()
    try:
        # This might fail if the server socket is already closed
        with socket.create_connection((HOST, PORT), timeout=0.1) as sock:
             print("Connected to self to unblock accept()...")
             # Send a dummy message or just close
             sock.close()
    except Exception as e:
        print(f"Could not connect to self to unblock accept(): {e}")

def main():
    global server_thread # Make thread accessible if needed elsewhere

    # --- Check if already running (simple socket bind check) ---
    try:
        # Try to bind to the *actual* port. If it fails, another instance IS likely running.
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Crucially, DON'T set SO_REUSEADDR here for the check
        test_sock.bind((HOST, PORT))
        test_sock.close()
        print("Port check successful, no other instance detected.")
        can_start = True
    except OSError as e:
         if "already in use" in str(e).lower() or (hasattr(e, 'winerror') and e.winerror == 10048): # winerror 10048 is WSAEADDRINUSE
              print(f"!!! Port {PORT} is already in use. Is another instance of cadwork_mcp.py running? !!!")
              print("!!! If previous run crashed, you might need to wait or manually free the port. !!!")
              can_start = False
         else:
              print(f"!!! Error checking port {PORT}: {e} !!!")
              traceback.print_exc()
              can_start = False # Safer not to start if check failed unexpectedly
    except Exception as e:
         print(f"!!! Unexpected error during port check: {e} !!!")
         traceback.print_exc()
         can_start = False

    if not can_start:
        print("--- Exiting cadwork_mcp.py due to port conflict or check error ---")
        return # Exit main() if cannot start

    # --- Start Server Thread ---
    print("Starting socket server thread...")
    server_thread = threading.Thread(target=socket_server, name="SocketServerThread", daemon=True)
    server_thread.start()
    print("cadwork_mcp main() finished, server thread running in background.")


if __name__ == "__main__":
    print(f"\n--- Running cadwork_mcp.py ({__name__} namespace) ---")
    main()
    print("--- cadwork_mcp.py script execution context finished ---")
