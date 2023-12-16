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
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Weather!!!", page_icon=":bar_chart:", layout="wide")



# Sidebar for navigation

st.sidebar.header("Weather Dashboard")
selected_page = st.sidebar.radio("Select a Page", ["Forecast", "Weather Analytics","About"])

if selected_page == "Forecast":
        

        ot = pd.read_csv("comox pred full.csv")
        ot['Date/Time'] = pd.to_datetime(ot['Date/Time'], format="%d-%m-%Y")

        st.title('Into The Weather &nbsp;&nbsp;🌦️')
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        station_names = ['No City Selected'] + ot["Station Name"].unique().tolist()

        # Create a select box with options for each station name
        option = st.selectbox('Select Your City', station_names)
        
        
        st.write(" ")

        if option == 'No City Selected':
              st.warning(" PLease select the valid city first ")

        else :
                

                st.write('You selected:', option)

                ot = ot[ot["Station Name"]== option]
                
                 

                d1 = st.date_input("Select the Date", value=None)
                st.write("Start Date:", d1) 

                if d1 is None:
                    st.warning(" PLease select the valid date first ")
                    
                else:
                    
                        d2 = datetime.strptime("2024-11-13", "%Y-%m-%d").date()

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
                                    elif 10 <= temperature_data <= 30:
                                        st.info("☀️ Moderate temperature. Enjoy the pleasant weather.")
                                    else:
                                        st.info("❄️ Cooler temperatures expected. Don't forget your jacket.")

                                    # Check for rain conditions
                                    if rain_data > 0:
                                        st.info(f"☔ Rainfall expected: {rain_data:.1f} mm. Don't forget your umbrella!")
                                    else:
                                        st.success("🌧️ No rain expected. Enjoy a dry day!")

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
     
    


        st.title("Dashboard")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


        df = pd.read_csv("daily_weather_data_v6.csv")


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
                    fig = px.line(df_mean_snow_by_year, x = "Year", y = "Total Snow (cm)", color_discrete_sequence=["yellow"],
                                    template = "seaborn",markers=True)

                    
                    fig.update_xaxes(
                    tick0=df_mean_temp_by_year["Year"].min(),
                    dtick=5,  # Adjust based on your preferences

                    )
                    st.plotly_chart(fig,use_container_width=True)

        st.map(df,
            latitude='Latitude',
            longitude='Longitude',
            size='size_mean'*1000,
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
            "role": "Data Scientist jr",
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
    
    
    
    
