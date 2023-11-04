import json

def bedroom(id, state, homeware):
    if id == "27":
        current_state = homeware.get("rgb003","on")
        if not current_state == state["presence"]:
            homeware.execute("rgb003","on",state["presence"])



      
             