from datetime import datetime
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
import folium
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Weather!!!", page_icon=":bar_chart:", layout="wide")



# Sidebar for navigation

st.sidebar.header("Weather Dashboard")
selected_page = st.sidebar.radio("Select a Page", ["Forecast", "Weather Analytics","Extreme Weather Analytics","About"])

if selected_page == "Forecast":
        

        ot = pd.read_csv("prediction.csv")
        ot['Date/Time'] = pd.to_datetime(ot['Date/Time'], format="%d-%m-%Y")

        st.title('Into The Weather &nbsp;&nbsp;🌦️')
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")



        #station_names = ['No City Selected'] + ot["Station Name"].unique().tolist()

        canada_provinces = {
                "Ontario": ["Armstrong","Mud River","Ferland", "Willet","Sidney","Quinte West","Belleville"],
                "Northwest Territories": ["Letty Harbour","Paulatuk","Cape Parry"],
                "Alberta": ["Cold Lake","Bonnyville","La Corey","Ardmore"],
                "Saskatchewan": ["Pierceland"],
                "British Columbia": ["Comox","Courtenay","Balmoral Beach", "Royston"],
                "Nova Scotia": ["Kingston", "Greenwood"],
                "Yukon": ["Kloo","Haines Junction","Bear Creek"],
                "Newfoundland and Labrador": ["Hopedale"],
                "Manitoba": ["Pilot Mound", "Crystal City", "Clearwater", "Wood Bay"],
            }
        
        prov_list = list(canada_provinces.keys())

        option1 = st.selectbox('Select Province', prov_list)

        locations = canada_provinces[option1]

        # Create a select box with options for each station name
        option = st.selectbox('Select Your City', locations)


        location_data = {
            

                "ARMSTRONG (AUT)":["Armstrong","Mud River","Ferland", "Willet"],
                "CAPE PARRY A":["Letty Harbour","Paulatuk","Cape Parry"],
                "COLD LAKE A":["Cold Lake","Bonnyville","La Corey","Ardmore","Pierceland"],
                "COMOX A":["Comox","Courtenay","Balmoral Beach", "Royston"],      
                "GREENWOOD A":["Kingston","Greenwood"],
                "HAINES JUNCTION":["Kloo","Haines Junction","Bear Creek"], 
                "HOPEDALE (AUT)	":["Hopedale",],
                "PILOT MOUND (AUT)":["Pilot Mound","Crystal City","Clearwater", "Wood Bay"],
                "TRENTON A":[ "Sidney","Quinte West", "Belleville"]     
                
        }

        city_to_find = option

        # Finding the key for the specified city
        found_keys = [key for key, cities in location_data.items() if city_to_find in cities]

        # Displaying the result
        if found_keys:
            print(f"The city '{city_to_find}' is in the location(s): {', '.join(found_keys)}")
        else:
            print(f"The city '{city_to_find}' was not found in any location.")

            
        option = found_keys[0]

        #st.write(found_keys[0])
        st.write(" ")

        if option == 'No City Selected':
              st.warning(" PLease select the valid city first ")

        else :
                

               # st.write('You selected:', option)

                ot = ot[ot["Station Name"]== option]
                
                 

                d1 = st.date_input("Select the Date", value=None)
                st.write("Start Date:", d1) 

                if d1 is None:
                    st.warning(" PLease select the valid date first ")
                    
                else:
                    
                        d2 = datetime.strptime("2024-12-01", "%Y-%m-%d").date()

                        if(d1 < d2):
                            

                                ot1 = ot[ot['Date/Time'] == str(d1)]
                            
                                st.write(" ")

                                st.write(" ")

                                max_temp = str( [ot1["Mean Temp (°C)"]])
                                print(max_temp)


                                
                                st.write(" ")
                                st.write(" ")

                                if st.button('SUBMIT'):

                                    st.write(" ")
                                    st.write(" ")
                                    st.write(" ")

                                    st.subheader ('Weather Predictions 🌥️')

                                    st.write(" ")
                                    st.write(" ")
                                    st.write(" ")
                                    st.write(" ")
                                    
                                    temperature_data = ot1["Mean Temp (°C)"].tolist()[0]
                                    maximum_temp = ot1["Max Temp (°C)"].tolist()[0]  
                                    minimum_temp = ot1["Min Temp (°C)"].tolist()[0]
                                    rain_data = ot1["Total Rain (mm)"].tolist()[0]
                                    extreme_data = ot1["Extreme_Weather_Condition"].tolist()[0]

                                    col1, col2, col3, col4 = st.columns(4)
                                    col1.metric("Average Temperature", f"{temperature_data:.1f} °C", "☀️")
                                    col2.metric("Maximum Temperature", f"{maximum_temp:.1f}°C", "🌞")
                                    col3.metric("Minimum Temperature", f"{minimum_temp:.1f}°C", "🌞")
                                    col4.metric("Rain", f"{rain_data:.1f} mm", "⛈️")

                                    st.write(" ")
                                    st.write(" ")
                                    st.write(" ")

                                    # Display weather-related information
                                    if temperature_data > 30:
                                        st.warning("🔥 High temperature alert! It's going to be a hot day.")
                                        if extreme_data == "Freezing Rain":
                                          st.warning(f"🚨🚨⚠️ Urgent Weather ALERT: FREEZING RAIN ADVISORY ⚠️ 🚨🚨")
                                    elif 10 <= temperature_data <= 30:
                                        st.info("☀️ Moderate temperature. Enjoy the pleasant weather.")
                                    else:
                                        st.info("❄️ Cooler temperatures expected. Don't forget your jacket.")

                                    # Check for rain conditions
                                    if rain_data > 0:
                                        st.info(f"☔ Rainfall expected: {rain_data:.1f} mm. Don't forget your umbrella!")
                                    else:
                                        st.info("🌧️ No rain expected. Enjoy a dry day!")

                                    
                                    if extreme_data == "Extreme Cold":
                                          st.warning(f"🚨🚨⚠️ Urgent Weather ALERT: EXTREME COLD WARNING ⚠️ 🚨🚨")
                                    if extreme_data == "Snow Storm":
                                          st.warning(f"🚨🚨⚠️ Urgent Weather ALERT: SNOW STORM WARNING ⚠️🚨🚨")
                        
                                    if extreme_data == "Heavy Rainfall":
                                          st.warning(f"🚨🚨⚠️ Urgent Weather ALERT: HEAVY RAINFALL WARNING ⚠️🚨🚨")
                                    if extreme_data == "Heavy Snowfall":
                                          st.warning(f"🚨🚨⚠️ Urgent Weather ALERT: HEAVY SNOWFALL WARNING ⚠️🚨🚨")



                                    start_date = pd.to_datetime(d1)  


                        # Calculate the end date as the start date plus 15 days
                                    end_date = start_date + pd.Timedelta(days=15)

                                    

                        # Filter the DataFrame based on the date range
                                    filtered_df = ot[(ot['Date/Time'] >= start_date) & (ot['Date/Time'] <= end_date)]
                                    
                                    st.write(" ")
                                    st.write(" ")
                        
                                    fig = go.Figure()

                                    fig.add_trace(go.Scatter(
                                    x=filtered_df["Date/Time"],
                                    y=filtered_df["Max Temp (°C)"],
                                    line=dict(color='#DE3163', dash='dot'),
                                    name='Max Temp'
                                    
                                ))

                                    fig.add_trace(go.Scatter(
                                    x=filtered_df["Date/Time"],
                                    y=filtered_df["Mean Temp (°C)"],
                                    line=dict(color='#FF7F50', dash='solid'),
                                    name='Mean Temp'
                                    
                                ))
                                    

                                    fig.add_trace(go.Scatter(
                                    x=filtered_df["Date/Time"],
                                    y=filtered_df["Min Temp (°C)"],
                                    line=dict(color='#5DADE2', dash='dot'),
                                    name='Min Temp'
                                    
                                ))
                                    st.write(" ")
                                    st.write(" ")
                                    st.write(" ")
                            
                                    st.subheader ('Temperature Prediction Chart')
                                    fig.update_layout(
                                    #st.subheader ('Temperature Predictions'),
                                    xaxis_title='Year',
                                    yaxis_title='Temperature (°C)'
                                )

                                # Display the figure using Streamlit
                                    st.plotly_chart(fig,use_container_width=True)



                                    st.subheader(" Rain Prediction Chart ")
                                    fig = px.line(filtered_df, x = "Date/Time", y = "Total Rain (mm)", color_discrete_sequence=["#2C479D"],
                                                    template = "seaborn",markers=True)
                                    

                                    fig.update_xaxes(
                                    tick0=filtered_df["Date/Time"].min(),
                                    #dtick=5,  # Adjust based on your preferences

                                    )
                                    st.plotly_chart(fig,use_container_width=True)

                        else:

                            st.warning("Please note that our forecast model has limitations, and predictions beyond one year may not be accurate. We recommend using short-term forecasts for better reliability.")
                    
        
# Page 2            

elif selected_page == "Weather Analytics":
     
    


        st.title("Weather analytics Dashboard")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)





        df = pd.read_csv("weather_data.csv")


        canada_provinces = {
                        "Ontario": ["Armstrong","Mud River","Ferland", "Willet","Sidney","Quinte West","Belleville"],
                        "Northwest Territories": ["Letty Harbour","Paulatuk","Cape Parry"],
                        "Alberta": ["Cold Lake","Bonnyville","La Corey","Ardmore"],
                        "Saskatchewan": ["Pierceland"],
                        "British Columbia": ["Comox","Courtenay","Balmoral Beach", "Royston"],
                        "Nova Scotia": ["Kingston", "Greenwood"],
                        "Yukon": ["Kloo","Haines Junction","Bear Creek"],
                        "Newfoundland and Labrador": ["Hopedale"],
        }

        prov_list = list(canada_provinces.keys())

        option1 = st.selectbox('Select Province', prov_list)

        locations = canada_provinces[option1]

                # Create a select box with options for each station name
        option = st.selectbox('Select Your City', locations)


        location_data = {
                    

                        "ARMSTRONG (AUT)":["Armstrong","Mud River","Ferland", "Willet"],
                        "CAPE PARRY A":["Letty Harbour","Paulatuk","Cape Parry"],
                        "COLD LAKE A":["Cold Lake","Bonnyville","La Corey","Ardmore","Pierceland"],
                        "COMOX A":["Comox","Courtenay","Balmoral Beach", "Royston"],      
                        "GREENWOOD A":["Kingston","Greenwood"],
                        "HAINES JUNCTION":["Kloo","Haines Junction","Bear Creek"], 
                        "HOPEDALE (AUT)	":["Hopedale",],
                        "PILOT MOUND (AUT)":["Pilot Mound","Crystal City","Clearwater", "Wood Bay"],
                        "TRENTON A":[ "Sidney","Quinte West", "Belleville"]     
                        
                }

        city_to_find = option

                # Finding the key for the specified city
        found_keys = [key for key, cities in location_data.items() if city_to_find in cities]

                # Displaying the result
        if found_keys:
                    print(f"The city '{city_to_find}' is in the location(s): {', '.join(found_keys)}")
        else:
                    print(f"The city '{city_to_find}' was not found in any location.")

                    
        option = found_keys[0]

        df1 = df[df["Station Name"]== option]



        df1['size_mean'] = (df1['Mean Temp (°C)'].abs().round().astype(int))

        st.write(" ")
        st.write(" ")

        #df['Spd of Max Gust (km/h)'] = pd.to_numeric(df['Spd of Max Gust (km/h)'], errors='coerce')



        df_mean_temp_by_year = df1.groupby(df1["Year"])["Mean Temp (°C)"].mean().reset_index()

        df_max_temp_by_year = df1.groupby(df1["Year"])["Max Temp (°C)"].max().reset_index()

        df_min_temp_by_year = df1.groupby(df1["Year"])["Min Temp (°C)"].min().reset_index()


        df_mean_precip_by_year = df1.groupby(df1["Year"])["Total Precip (mm)"].mean().reset_index()
        df_mean_snow_by_year = df1.groupby(df1["Year"])["Total Snow (cm)"].mean().reset_index()

        st.write("---")
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

        st.write("---")
        
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
                    fig = px.line(df_mean_snow_by_year, x = "Year", y = "Total Snow (cm)", color_discrete_sequence=["yellow"],
                                    template = "seaborn",markers=True)

                    
                    fig.update_xaxes(
                    tick0=df_mean_temp_by_year["Year"].min(),
                    dtick=5,  # Adjust based on your preferences

                    )
                    st.plotly_chart(fig,use_container_width=True)


       


        st.write("---")          

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

            st.subheader("Years with Highest And Lowest Mean Rain ")
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

        st.write("---")
# Identify top five years with the highest mean temperature
        top_five_years = df_mean_temp_by_year.nlargest(5, "Mean Temp (°C)")

        bottom_five_years = df_mean_temp_by_year.nsmallest(5, "Mean Temp (°C)")

            # Assign colors to differentiate between top and bottom years
        top_color = "highest"
        bottom_color = "lowest"

            # Combine both top and bottom five years with assigned colors
        top_five_years["Color"] = top_color
        bottom_five_years["Color"] = bottom_color
        combined_years = pd.concat([top_five_years, bottom_five_years], ignore_index=True)

        combined_years['Year'] = combined_years['Year'].astype(str)

        st.subheader("Years with Highest And Lowest Mean Temperature ")
        fig = px.bar(combined_years,
                        x = "Year", 
                        y = "Mean Temp (°C)",
                        color="Color", 
                        template = "seaborn",
                        color_discrete_map={"highest": "#FF9633", "lowest": "#3371FF"}, 

                        )
            
        fig.update_traces(marker=dict(line=dict(width=0.2)))
        st.plotly_chart(fig,use_container_width=True)



        st.write("---")
        st.subheader("Weather Stations Map")
        # Example DataFrame with full weather data
        weather_data = pd.read_csv("weather_data.csv")

        # Extract information for the 9 weather stations
        selected_stations = weather_data['Station Name'].unique()

        # Create a new DataFrame with information for the 9 stations
        stations_df = weather_data[weather_data['Station Name'].isin(selected_stations)].copy()
        stations_df = stations_df[['Station Name', 'lat', 'lon']].drop_duplicates()

        # Set the center and zoom level for the map
        center = [stations_df['lat'].mean(), stations_df['lon'].mean()]
        zoom_start = 4

        # Create a Folium map
        m = folium.Map(location=center, zoom_start=zoom_start)



        # Add markers for each station
        for index, row in stations_df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=row['Station Name'],
                tooltip=row['Station Name'],
            ).add_to(m)

        # Save the map to an HTML file
        #m.save("weather_stations_map.html")
        st_data = st_folium(m, use_container_width=True, height= 400)
        # Display the map




elif selected_page == "Extreme Weather Analytics":
        st.title("Extreme Weather Analysis")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

        df = pd.read_csv("extreme_predict.csv")



        canada_provinces = {
                        "Ontario": ["Armstrong","Mud River","Ferland", "Willet","Sidney","Quinte West","Belleville"],
                        "Northwest Territories": ["Letty Harbour","Paulatuk","Cape Parry"],
                        "Alberta": ["Cold Lake","Bonnyville","La Corey","Ardmore"],
                        "Saskatchewan": ["Pierceland"],
                        "British Columbia": ["Comox","Courtenay","Balmoral Beach", "Royston"],
                        "Nova Scotia": ["Kingston", "Greenwood"],
                        "Yukon": ["Kloo","Haines Junction","Bear Creek"],
                        
        }

        prov_list = list(canada_provinces.keys())

        option1 = st.selectbox('Select Province', prov_list)

        locations = canada_provinces[option1]

                # Create a select box with options for each station name
        option = st.selectbox('Select Your City', locations)


        location_data = {
                    

                        "ARMSTRONG (AUT)":["Armstrong","Mud River","Ferland", "Willet"],
                        "CAPE PARRY A":["Letty Harbour","Paulatuk","Cape Parry"],
                        "COLD LAKE A":["Cold Lake","Bonnyville","La Corey","Ardmore","Pierceland"],
                        "COMOX A":["Comox","Courtenay","Balmoral Beach", "Royston"],      
                        "GREENWOOD A":["Kingston","Greenwood"],
                        "HAINES JUNCTION":["Kloo","Haines Junction","Bear Creek"], 
                        "PILOT MOUND (AUT)":["Pilot Mound","Crystal City","Clearwater", "Wood Bay"],
                        "TRENTON A":[ "Sidney","Quinte West", "Belleville"]     
                        
                }

        city_to_find = option

                # Finding the key for the specified city
        found_keys = [key for key, cities in location_data.items() if city_to_find in cities]

                # Displaying the result
        if found_keys:
                    print(f"The city '{city_to_find}' is in the location(s): {', '.join(found_keys)}")
        else:
                    print(f"The city '{city_to_find}' was not found in any location.")

                    
        option = found_keys[0]

        df = df[df["Station Name"]== option]



        df1 = pd.DataFrame()
        df1["Date/Time"] = df['Date/Time']
        df1["Extreme_Weather_Condition"] = df['Extreme_Weather_Condition']

        df1['Date/Time'] = pd.to_datetime(df1['Date/Time'])

        # Extract year from 'Date/Time' and create a new 'Year' column
        df1['Year'] = df1['Date/Time'].dt.year

        # Group by 'Year' and 'Extreme_Weather_Condition', then count occurrences
        grouped_data = df1.groupby(['Year', 'Extreme_Weather_Condition']).size().reset_index(name='Occurrence_Count')

        # Display the resulting grouped data
        #print(grouped_data)


        # Assuming grouped_data is your DataFrame with 'Year', 'Extreme_Weather_Condition', and 'Occurrence_Count' columns

        # Specify the undesired value in the Extreme_Weather_Condition column
        undesired_value = 'Normal'  # Replace with the actual value to exclude

        # Filter out the undesired value
        filtered_data = grouped_data.query(f'Extreme_Weather_Condition != "{undesired_value}"')

        # Create the stacked bar chart using Plotly Express
        fig = px.bar(filtered_data, x='Year', y='Occurrence_Count', color='Extreme_Weather_Condition',
                    labels={'Occurrence_Count': 'Occurrence Count'},
                    title='Stacked Bar Chart of Extreme Weather Conditions Across Years',
                    category_orders={'Extreme_Weather_Condition': sorted(filtered_data['Extreme_Weather_Condition'].unique())},
                    height=600)

        # Customize the layout
        fig.update_layout(
            xaxis=dict(tickangle=45),
            legend=dict(title='Extreme Weather Condition'),
            barmode='stack',  # Set to 'stack' for stacked bar chart
        )

        # Show the plot
        st.plotly_chart(fig,use_container_width=True)


        st.write("---")

        # Assuming df is your DataFrame with "Date/Time" and "Extreme_Weather_Condition" columns

        # Convert 'Date/Time' to datetime format
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])

        # Extract year and month from the 'Date/Time' column
        df['Year'] = df['Date/Time'].dt.year
        df['Month'] = df['Date/Time'].dt.strftime('%B')  # Full month name

        # Define the list of weather conditions
        weather_conditions = ['Extreme Cold', 'Snow Storm', 'Heavy Rainfall', 'Heavy Snowfall']

        # Define corresponding marker shape for each weather condition (square)
        marker_shape = 'square'

        # Define different colors for each weather condition
        colors = px.colors.qualitative.Set1

        # Create separate scatter plots for each weather condition with square marker shape, different colors, and adjusted marker size
        for condition, color in zip(weather_conditions, colors):
            
            
            st.write(" ")
            st.write(" ")
            st.write(" ")
            
            st.subheader(f"Occurrence of {condition} Over Time")

            df_condition = df[df["Extreme_Weather_Condition"] == condition]

            fig = px.scatter(df_condition, x="Year", y="Month",
                            color_discrete_sequence=[color],
                            labels={"Month": "Month"},
                            #title=f"Occurrence of {condition} Over Time",
                            hover_data={"Date/Time": "|%B %d, %Y"},
                            symbol="Extreme_Weather_Condition",
                            symbol_sequence=[marker_shape],  # Set marker shape for each condition
                            symbol_map={condition: marker_shape},  # Map each condition to its marker shape
                            size_max=10,  # Adjust the maximum marker size
                            #opacity=0.7
                            )
                            #   # Set the marker transparency
            fig.update_layout(yaxis=dict(categoryorder='array', categoryarray=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']))
            # Update the layout for better aesthetics
            fig.update_layout(
                showlegend=False,  # Hide legend for clarity
                xaxis_title="Year",
                yaxis_title="Month",
                template="plotly_white"  # Choose a plotly template for a cleaner look
            )

            # Show each individual plot
            st.plotly_chart(fig,use_container_width=True)

     


elif selected_page == "About":  


    st.title("About Our Team")
    
    st.write(
        "Welcome to the About page! Here, we'll introduce you to the amazing individuals who make up our team."
    )
    
    st.header("Meet the Team", divider="grey")
    st.write("---")
    st.header("", divider="rainbow")
    st.write(" ")
    st.write(" ")
    
    team_members = [
        {
            "name": "Marco",
            "role": "Team Lead",
            "bio": "Organized and guided team efforts, ensuring collaboration and efficient implementation of data-driven solutions.",
            "contact": "Email: marconinaflores@loyalistcollege.com",
            "photo_url": "marco.png",
        },
        {
            "name": "Surya",
            "role": "Data Scientist",
            "bio": "Developed architecture, selected data sources, created forecasting models.",
            "contact": "LinkedIn: https://www.linkedin.com/in/suryabansal1995",
            "photo_url": "surya.jpeg",
        },
        {
            "name": "Parminder",
            "role": "UI/UX Developer & Deployment Specialist",
            "bio": "Deployed web applications and led UI/UX design initiatives, seamlessly merging development and deployment processes. Adept at crafting visually appealing interfaces, gathering user feedback, and ensuring optimal performance.",
            "contact": "Email: parmindersinghgil@loyalistcollege.com",
            "photo_url": "gill.png",
        },
        {
            "name": "Barinder",
            "role": "Data Scientist(helper)",
            "bio": "Hourly Data fetching through API and Pre Processing the data with integration with LSTM model. Optimizing the Results for Achieving more Accurate results in Terms of Loss and Sparse Categorical Entropy. Dealing with Extreme Weather conditions.",
            "contact":"barindersingh2@loyalistcollege.com",
            "photo_url": "bari.png",
        },
        {
            "name": "Manpreet",
            "role": "Documentation",
            "bio": "Helped the team stay organized and on track by providing a clear understanding of the progress of the project.",
            "contact": "Email: manpreetkaur115@loyalistcollege.com",
            "photo_url": "mano.png",
        },
        {
            "name": "Tanishq",
            "role": "Tester & GitHub Repository Manager",
            "bio": "Ensures accuracy by validating data sources and verifying the precision of forecasting algorithms through rigorous testing  protocols and maintained the repository throughout the project.",
            "contact":"Tanishqtaneja@loyalistcollege.com",
            "photo_url": "tanu.png",
        },
    ]
    
    for member in team_members:
        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader(member["name"])
            st.write(f"**Role:** {member['role']}")
            st.write(member["bio"])
            st.write(member["contact"])
    
        with col2:
            st.image(member["photo_url"], caption=f"{member['name']} - {member['role']}", use_column_width=False, width=300)
    
        # Add more information as needed, such as images, social media links, etc.
    
        st.subheader(" ", divider='rainbow')
    
    
