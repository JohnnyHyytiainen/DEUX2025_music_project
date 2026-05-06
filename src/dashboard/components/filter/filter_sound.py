import streamlit as st
import streamlit_vertical_slider as svs

def bpm_slider():
    return st.slider("Choose BPM:", 60, 200, (60, 200))

def procent_slider(name:str):
    return st.slider(label=name,
                     min_value=0.01, 
                     max_value=1.00, 
                     value=(0.01, 1.00), 
                     format="percent", 
                     step=0.01)

def vertical_procent_slider(name:str):
    return svs.vertical_slider(label=name, 
                               thumb_shape="square",
                               height=100, 
                               min_value=1, 
                               max_value=100,
                               default_value=100,
                               step=1,
                               slider_color="#7B7B7B",
                               thumb_color="#000000",
                               track_color="#7B7B7B"
                               )

def vertical_bpm_slider(name:str):
    return svs.vertical_slider(label=name, 
                               thumb_shape="square",
                               height=100, 
                               min_value=0, 
                               max_value=236,
                               default_value=236,
                               step=1,
                               slider_color="#7B7B7B",
                               thumb_color="#000000",
                               track_color="#7B7B7B"
                               )

def vertical_loudness_slider(name:str):
    return svs.vertical_slider(label=name, 
                               thumb_shape="square",
                               height=100, 
                               min_value=-50, 
                               max_value=3,
                               default_value=3,
                               step=1,
                               slider_color="#7B7B7B",
                               thumb_color="#000000",
                               track_color="#7B7B7B"
                               )

def fifty_slider(name:str):
    return st.slider(name, 0, 1, (0, 100))

def explicit_chooser():
    return st.segmented_control(
        label="Explicit",
        options=["NO", "YES"],
        selection_mode="single",
        default="NO",
        required=True
        )

def mode_chooser():
    return st.segmented_control(label="Mode", options=["Major", "Minor"], selection_mode="single", default="Major", required=True)



