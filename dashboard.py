import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


# Sidebar for navigation
st.sidebar.header("Weather Dashboard")
selected_page = st.sidebar.radio("Select a Page", ["Current Weather", "Weather Charts", "Historical Data"])

if selected_page == "Current Weather":

        st.title('Into The Weather &nbsp;&nbsp;🌦️')
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        option = st.selectbox('Select Your City', ('No City Selected', 'Toronto', 'Mississauga', 'Brampton', 'Malton'))
        st.write('You selected:', option)
        st.write(" ")
        st.write(" ")
        st.write(" ")

        if option != 'No City Selected':
            # Replace with actual data retrieval
            temperature_data = 23  # Replace with actual temperature data
            snow_data = 2  # Replace with actual snow data
            rain_data = 55  # Replace with actual rain data

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temperature_data} °F", "1.2 °F")
            col2.metric("Snow", f"{snow_data}%", "-8%")
            col3.metric("Rain", f"{rain_data}%", "4%")

        else:
            temperature_data = 'NULL'  # Replace with actual temperature data
            snow_data = 'NULL'  # Replace with actual snow data
            rain_data = 'NULL'  # Replace with actual rain data

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temperature_data} °F", "Null")
            col2.metric("Snow", f"{snow_data}%", "Null")
            col3.metric("Rain", f"{rain_data}%", "Null")

        st.write(" ")
        st.write(" ")
        st.write(" ")

        d1 = st.date_input("Select the Start Date", value=None)
        st.write("Start Date:", d1)

        d2 = st.date_input("Select the End Date", value=None)
        st.write("End Date:", d2)

        def generate_dummy_data(d1, d2):
            # Generate a date range between start and end dates
            date_range = pd.date_range(start=d1, end=d2, freq='D')

            # Generate synthetic data for temperature, snow, and rain
            temperature = [20 + np.random.normal(0, 2) for _ in range(len(date_range))]
            snow = [0.5 + np.random.normal(0, 5) for _ in range(len(date_range))]
            rain = [0.3 + np.random.normal(0, 5) for _ in range(len(date_range))]

            # Create a DataFrame to store the data
            df = pd.DataFrame({
                'Date': date_range,
                'Temperature': temperature,
                'Snow': snow,
                'Rain': rain
            })

            return df

        st.write(" ")
        st.write(" ")

        if st.button('SUBMIT'):
            chart_data = generate_dummy_data(d1, d2)

            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")

            st.subheader("Line Chart")
            fig_line = px.line(chart_data, x='Date', y=['Temperature', 'Snow', 'Rain'], 
                            title="Weather Data Over Time")
            st.plotly_chart(fig_line)

            st.write('Data Fetched')
        else:
            st.write('Submit to Get chart analysis')


if selected_page == "Weather Charts":
     
     st.title('Weather Charts &nbsp;&nbsp;📈')
     
if selected_page == "Historical Data":  

     st.title('Historical Analysis &nbsp;&nbsp;🌪️')


     # commit