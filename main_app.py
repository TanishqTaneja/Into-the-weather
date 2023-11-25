import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit as st
import plotly.express as px
import geopandas as gpd
import os
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Weather!!!", page_icon=":bar_chart:", layout="wide")



# Sidebar for navigation

st.sidebar.header("Weather Dashboard")
selected_page = st.sidebar.radio("Select a Page", ["Forcast", "Weather Analytics", "Extreme"])

if selected_page == "Forcast":
        

        ot = pd.read_csv("/Users/princegill/Documents/VSCode/AIP/comox pred full.csv")
        ot['Date/Time'] = pd.to_datetime(ot['Date/Time'], format="%d-%m-%Y")

        st.title('Into The Weather &nbsp;&nbsp;🌦️')
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        option = st.selectbox('Select Your City', ('No City Selected', ot["Station Name"].unique()))
        st.write('You selected:', option)
        st.write(" ")
        st.write(" ")
        st.write(" ")

        if option != 'No City Selected':
            # Replace with actual data retrieval
            temperature_data = '☀️'  # Replace with actual temperature data
            snow_data = '❄️'  # Replace with actual snow data
            rain_data = '⛈️' # Replace with actual rain data

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temperature_data} °F", "☀️ °F")
            col2.metric("Snow", f"{snow_data}%", "❄️%")
            col3.metric("Rain", f"{rain_data}%", "⛈️%")

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

        d1 = st.date_input("Select the Date", value=None)
        st.write("Start Date:", d1) 

        ot1 = ot[ot['Date/Time'] == str(d1)]
       
        st.write(" ")

        st.write(" ")

        max_temp = str( [ot1["Mean Temp (°C)"]])
        print(max_temp)

        if st.button('SUBMIT'):
            
            temperature_data = ot1["Mean Temp (°C)"].tolist()[0]
            snow_data = ot1["Total Snow (cm)"].tolist()[0]   #    Replace with actual snow data
            rain_data = ot1["Total Rain (mm)"].tolist()[0] # Replace with actual rain data

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temperature_data:.1f} °F", "☀️")
            col2.metric("Snow", f"{snow_data:.1f}%", "❄️")
            col3.metric("Rain", f"{rain_data:.1f}%", "⛈️")



            start_date = pd.to_datetime(d1)  # Replace with your desired start date

# Calculate the end date as the start date plus 15 days
            end_date = start_date + pd.Timedelta(days=15)

            

# Filter the DataFrame based on the date range
            filtered_df = ot[(ot['Date/Time'] >= start_date) & (ot['Date/Time'] <= end_date)]
            
            #st.write(filtered_df)

            fig = go.Figure()

            fig.add_trace(go.Scatter(
            x=filtered_df["Date/Time"],
            y=filtered_df["Max Temp (°C)"],
            line=dict(color='firebrick', dash='dash'),
            name='Max Temp'
            
        ))
            fig.update_layout(
            title='Average High and Low Temperatures Over Years',
            xaxis_title='Year',
            yaxis_title='Temperature (°C)'
        )

        # Display the figure using Streamlit
            st.plotly_chart(fig,use_container_width=True)

        
# Page 2            

elif selected_page == "Weather Analytics":
     
    


        st.title("Dashboard")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


        df = pd.read_csv("/Users/princegill/Documents/VSCode/AIP/Data and other/Daily dataset/daily_weather_data_v6.csv")


        df['size_mean'] = (df['Mean Temp (°C)'].abs().round().astype(int))



        #df['Spd of Max Gust (km/h)'] = pd.to_numeric(df['Spd of Max Gust (km/h)'], errors='coerce')

        region = st.selectbox("Pick your Region", df["Station Name"].unique())

        if not region:
            # If no region is selected, use data for the first station
            df1 = df[df["Station Name"] == df["Station Name"].iloc[0]]
        else:
            # Filter the DataFrame based on the selected region
            df1 = df[df["Station Name"].isin([region])]


        df_mean_temp_by_year = df1.groupby(df1["Year"])["Mean Temp (°C)"].mean().reset_index()

        df_max_temp_by_year = df1.groupby(df1["Year"])["Max Temp (°C)"].max().reset_index()

        df_min_temp_by_year = df1.groupby(df1["Year"])["Min Temp (°C)"].min().reset_index()


        df_mean_precip_by_year = df1.groupby(df1["Year"])["Total Precip (mm)"].mean().reset_index()
        df_mean_snow_by_year = df1.groupby(df1["Year"])["Total Snow (cm)"].mean().reset_index()


        st.subheader("Mean Temp vs Year ")



        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_max_temp_by_year["Year"],
            y=df_max_temp_by_year["Max Temp (°C)"],
            line=dict(color='firebrick', dash='dash'),
            name='Max Temp'
            
        ))

        fig.add_trace(go.Scatter(
            x=df_mean_temp_by_year["Year"],
            y=df_mean_temp_by_year["Mean Temp (°C)"],
            line=dict(color='#F7DC6F', dash='solid',),
            
            name='Mean Temp'
        ))

        fig.add_trace(go.Scatter(
            x=df_min_temp_by_year["Year"],
            y=df_min_temp_by_year["Min Temp (°C)"],
            line=dict(color='lightblue', dash='dash'),
            name='Min Temp'
        ))

        # Update layout
        fig.update_layout(
            title='Average High and Low Temperatures Over Years',
            xaxis_title='Year',
            yaxis_title='Temperature (°C)'
        )

        # Display the figure using Streamlit
        st.plotly_chart(fig,use_container_width=True)


        col1, col2 = st.columns((2))


        with col1:

                    st.subheader("Mean Rain vs Year ")
                    fig = px.line(df_mean_precip_by_year, x = "Year", y = "Total Precip (mm)", color_discrete_sequence=["#2C479D"],
                                    template = "seaborn",markers=True)
                    

                    fig.update_xaxes(
                    tick0=df_mean_temp_by_year["Year"].min(),
                    dtick=5,  # Adjust based on your preferences

                    )
                    st.plotly_chart(fig,use_container_width=True)
                        
                            
        with col2:
                        

                    st.subheader("Mean Snow vs Year ")
                    fig = px.line(df_mean_snow_by_year, x = "Year", y = "Total Snow (cm)", color_discrete_sequence=["white"],
                                    template = "seaborn",markers=True)

                    
                    fig.update_xaxes(
                    tick0=df_mean_temp_by_year["Year"].min(),
                    dtick=5,  # Adjust based on your preferences

                    )
                    st.plotly_chart(fig,use_container_width=True)

        st.map(df,
            latitude='Latitude',
            longitude='Longitude',
            size='size_mean'*100,
            #color='size_mean'
            )
                    

        col1, col2 = st.columns((2))

        with col1:

            # Identify top five years with the highest mean temperature
            top_five_years = df_mean_precip_by_year.nlargest(5, "Total Precip (mm)")

            bottom_five_years = df_mean_precip_by_year.nsmallest(5, "Total Precip (mm)")

            # Assign colors to differentiate between top and bottom years
            top_color = "highest"
            bottom_color = "lowest"

            # Combine both top and bottom five years with assigned colors
            top_five_years["Color"] = top_color
            bottom_five_years["Color"] = bottom_color
            combined_years = pd.concat([top_five_years, bottom_five_years], ignore_index=True)

            combined_years['Year'] = combined_years['Year'].astype(str)

            st.subheader("Years with Highest And Lowest Mean Percipitation ")
            fig = px.bar(combined_years,
                        x = "Year", 
                        y = "Total Precip (mm)",
                        color="Color", 
                        template = "seaborn",
                        color_discrete_map={"highest": "#FF9633", "lowest": "#3371FF"}, 

                        )
            
            fig.update_traces(marker=dict(line=dict(width=0.2)))
            st.plotly_chart(fig,use_container_width=True,height=400)

        with col2:   


            # Identify top five years with the highest mean temperature
            top_five_years = df_mean_snow_by_year.nlargest(5, "Total Snow (cm)")

            bottom_five_years = df_mean_snow_by_year.nsmallest(5, "Total Snow (cm)")

            # Assign colors to differentiate between top and bottom years
            top_color = "highest"
            bottom_color = "lowest"

            # Combine both top and bottom five years with assigned colors
            top_five_years["Color"] = top_color
            bottom_five_years["Color"] = bottom_color
            combined_years = pd.concat([top_five_years, bottom_five_years], ignore_index=True)

            combined_years['Year'] = combined_years['Year'].astype(str)

            st.subheader("Years with Highest And Lowest Mean Snow Fall ")
            fig = px.bar(combined_years,
                        x = "Year", 
                        y = "Total Snow (cm)",
                        color="Color", 
                        template = "seaborn",
                        color_discrete_map={"highest": "#FF9633", "lowest": "#3371FF"}, 

                        )
            
            fig.update_traces(marker=dict(line=dict(width=0.2)))
            st.plotly_chart(fig,use_container_width=True,height=400)

# Page 3

elif selected_page == "Extreme":  

     st.title('❄️ Extreme Weather Analysis &nbsp;&nbsp;🌊')
     
