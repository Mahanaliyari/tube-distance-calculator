import  streamlit as st 
import pandas as pd  
import networkx as nx 
import pickle

# Loading the graph and dictionaries 
with open("graph.pkl", "rb") as f:
    G = pickle.load(f)
with open("id_to_name.pkl", "rb") as f:
    id_to_name = pickle.load(f)
with open("name_to_id.pkl", "rb") as f:
    name_to_id = pickle.load(f)

st.set_page_config(page_title="Tube Distance Calculator")
st.title("London Underground Distance Tool")
st.markdown("A tool that calculates station-to-station distance in london underground")
st.divider()
 
col1,col2 = st.columns(2)
with col1: 
    start_name = st.selectbox("From",sorted(name_to_id.keys()))
with col2:
    end_name = st.selectbox("To",sorted(name_to_id.keys()))


# If the button is clicked
if st.button("Calculate Distance"):
    if start_name == end_name: 
        st.warning("Please select two different stations")
    else:
        start_id = name_to_id[start_name]
        end_id = name_to_id[end_name] 
        
        try:
        
            distance_km = nx.dijkstra_path_length(G,source = start_id, target = end_id, weight = "weight")
            path_ids = nx.dijkstra_path(G, source = start_id, target = end_id, weight = "weight")
            path_names = [id_to_name[i] for i in path_ids]
            num_stops = len(path_names)-2
            st.success(f"Distance: {distance_km:.2f} km")
            st.write(f"There are {num_stops} stops from ({path_names[0]}) to ({path_names[-1]})") 
            st.write(" → ".join(path_names))
            st.divider()
            st.subheader("Break down of the path and their line")
            
            for i in range(len(path_ids)-1): 
                edge_data = G.get_edge_data(path_ids[i],path_ids[i+1])
                line = edge_data.get("line")
                st.write(f"{id_to_name[path_ids[i]]} → {id_to_name[path_ids[i+1]]}, Line: {line}")
            
            
        
        except nx.NetworkXNoPath:
            st.write("No path found between these two stations")
    
    
    
    
    
