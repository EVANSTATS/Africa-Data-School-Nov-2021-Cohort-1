import streamlit as st
import pandas as pd
import numpy as np

# Writing Data
st.title('This is a title')
st.header('This is a header')
st.subheader('My subheader')
st.text('My text')
numbers = [n for n in range(1, 11)]
squares = [n**2 for n in numbers]
df = pd.DataFrame({'numbers': numbers, 'squares': squares})
st.write(df)

# Input Text
num=st.text_input(label='Number', value=1)
st.write('Square: ', int(num)**2)

# Text Area
st.text_area('Enter Sentiment', max_chars=200)

# Line Charts
chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])
st.line_chart(chart_data)

# Maps
map_data = pd.DataFrame(
      np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
      columns=['lat', 'lon'])
st.map(map_data)

# Checkbox
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
    st.write(chart_data)

# Select box
option = st.selectbox(
          'Which number do you like best?',
           [10, 20, 30, 40])
st.write('You selected: ', option)

# Radio Button
cars=st.radio(
    'Favourite Car', ['BMW', 'Audi', 'Mercedes', 'VW']
)
st.write(cars)

# Date Picker
bday = st.date_input('Enter your birthday')
st.write(bday)

# APP LAYOUT
#  Sidebar
option = st.sidebar.selectbox(
      'Your favourite holiday destination',
       ['Maldives', 'Bali', 'Dubai', 'Namibia'])
'You selected:', option

# Columns
left_column, right_column = st.columns(2)
pressed = left_column.button('Press me!')
if pressed:
    right_column.write("You are a Genius")

# Expander
expander = st.expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

# Progress
import time

'Starting a long computation...'
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'...and now we\'re done!'

#Cache
@st.cache
def numberGenerator(square):
    num = np.sqrt(square)
    return num
numberGenerator(25)

# LaTeX
st.latex(r'''
a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
\sum_{k=0}^{n-1} ar^k =
a \left(\frac{1-r^{n}}{1-r}\right)
''')
