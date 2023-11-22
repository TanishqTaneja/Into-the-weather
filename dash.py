import streamlit as st
import plotly.express as px
import geopandas as gpd
import pandas as pd
import numpy as np
import os
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Weather!!!", page_icon=":bar_chart:",layout="wide")

st.title("Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


df = pd.read_csv("/Users/princegill/Documents/VSCode/AIP/Data and other/Daily dataset/daily_weather_data_v6.csv")


df['size_mean'] = (df['Mean Temp (°C)'].abs().round().astype(int))



#df['Spd of Max Gust (km/h)'] = pd.to_numeric(df['Spd of Max Gust (km/h)'], errors='coerce')

region = st.sidebar.multiselect("Pick your Region", df["Station Name"].unique())
if not region:
    df1 = df[df["Station Name"] == df["Station Name"].iloc[0]]
else:
    df1 = df[df["Station Name"].isin(region)]


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