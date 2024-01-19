import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#df = pd.read_csv()

st.title("A DATA ANALYSIS OF THE CYCLING TRAFFIC IN PARIS")
st.header("From October 2022 to November 2023")
st.sidebar.title("Table of contents")
pages=["Summary", "Cycling Traffic", "Weather & Traffic", "Interview / Barometer", "Machine Learning"]
page=st.sidebar.radio("Go to", pages)

st.sidebar.header("About")
st.sidebar.write("Authors: Martin Kruse, Andy Soydt, Marine Bajard-Malfondet")
st.sidebar.write("Data sources: ")


if page == pages[0]:
    st.write("### Summary")
    st.dataframe()

if page == pages[1]:
    st.write("### Cycling Traffic")
  
if page == pages[2] : 
  st.write("### Weather & Traffic")
    
if page == pages[3] : 
  st.write("### Interview & Barometer")

if page == pages[4] : 
  st.write("### Machine Learning")
    
