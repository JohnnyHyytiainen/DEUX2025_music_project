import streamlit as st
import streamlit_vertical_slider as svs

def vertical_procent_slider(name:str)-> int:
    """
    Creates a custom vertical slider for selecting a percentage value.

    Args:
        name (str): The label displayed above the slider.

    Returns:
        int: The selected percentage value (ranging from 1 to 100).
    """
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

def vertical_bpm_slider(name:str)-> int:
    """
    Creates a custom vertical slider for selecting a maximum BPM value.

    Args:
        name (str): The label displayed above the slider.

    Returns:
        int: The selected maximum BPM value (ranging from 0 to 236).
    """
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

def vertical_loudness_slider(name:str)-> int:
    """
    Creates a custom vertical slider for selecting a maximum loudness value.

    Args:
        name (str): The label displayed above the slider.

    Returns:
        int: The selected maximum loudness value in dBFS (ranging from -50 to 3).
    """
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

def explicit_chooser()-> str:
    """
    Creates a segmented control button group to toggle explicit content filtering.

    Returns:
        str: The selected censorship setting ("NO" or "YES").
    """
    return st.segmented_control(
        label="Uncensorded",
        options=["NO", "YES"],
        selection_mode="single",
        default="NO",
        required=True
        )

def mode_chooser()-> str:
    """
    Creates a segmented control button group to select the musical mode.

    Returns:
        str: The selected musical mode ("Major" or "Minor").
    """
    return st.segmented_control(label="Mode", options=["Major", "Minor"], selection_mode="single", default="Major", required=True)



