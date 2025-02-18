import streamlit as st

st.title("Hello World")

st.write("Hello World")

st.header("Hello World")

st.subheader("Hello World")

st.markdown("Hello World")

st.code("Hello World")

st.checkbox("Hello World")

name = 'Sultan'
age = 28

st.write(f"Name: {name},  Age: {age}")

# 1. Displaying text
st.text("This is a simple text")

# 2. Displaying data
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'], 'Age': [28, 24, 35, 32]}
st.dataframe(data)

# 3. Displaying charts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# 4. Displaying maps
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

# 5. Adding widgets
if st.button('Say hello'):
    st.write('Hello!')

# 6. Adding sliders
x = st.slider('Select a value')
st.write(f'Selected: {x}')

# 7. Adding input fields
name = st.text_input('Enter your name')
st.write(f'Hello, {name}!')

# 8. Adding file uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully")

# 9. Adding sidebar
st.sidebar.write("This is the sidebar")

# 10. Adding progress bar
import time

progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

st.write("Progress completed!")









