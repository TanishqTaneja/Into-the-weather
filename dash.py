import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Weather!!!", page_icon=":bar_chart:",layout="wide")

st.title("Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


df = pd.read_csv("/Users/princegill/Documents/VSCode/AIP/Data and other/Daily dataset/daily_weather_data_v6.csv")
df['Spd of Max Gust (km/h)'] = pd.to_numeric(df['Spd of Max Gust (km/h)'], errors='coerce')

region = st.sidebar.multiselect("Pick your Region", df["Station Name"].unique())
if not region:
    df1 = df[df["Station Name"] == df["Station Name"].iloc[0]]
else:
    df1 = df[df["Station Name"].isin(region)]



st.sidebar.header("Choose your filter: ")

available_options = ["Temperature", "Precipitation", "Wind"]

# Create a multiselect widget in the sidebar
selected_options = st.sidebar.multiselect("Line Chart Filters", available_options)

# Display the selected options



col1, col2 = st.columns((2))


df_mean_temp_by_year = df1.groupby(df1["Year"])["Mean Temp (°C)"].mean().reset_index()
df_mean_precip_by_year = df1.groupby(df1["Year"])["Total Precip (mm)"].mean().reset_index()
df_mean_snow_by_year = df1.groupby(df1["Year"])["Total Snow (cm)"].mean().reset_index()


with col1:
    st.subheader("Mean Temp vs Year ")
    fig = px.line(df_mean_temp_by_year, x = "Year", y = "Mean Temp (°C)", color_discrete_sequence=["blue"],
                 template = "seaborn")
    

    if "Precipitation" in selected_options:
    
        fig.add_trace(px.line(df_mean_precip_by_year,color_discrete_sequence=["yellow"], x="Year", y="Total Precip (mm)").data[0] )

    if "Wind" in selected_options:

        fig.add_trace(px.line(df_mean_snow_by_year,color_discrete_sequence=["white"], x="Year", y="Total Snow (cm)").data[0] )

    
    fig.update_xaxes(
    tick0=df_mean_temp_by_year["Year"].min(),
    dtick=5,  # Adjust based on your preferences

    )
    st.plotly_chart(fig,use_container_width=True)


    

df_mean_temp_by_year = df1.groupby(df1["Year"])["Mean Temp (°C)"].mean().reset_index()

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


with col2:   


    st.subheader("Years with Highest And Lowest Mean Temperature ")
    fig = px.bar(combined_years,
                 x = "Year", 
                 y = "Mean Temp (°C)",
                 color="Color", 
                 template = "seaborn",
                 color_discrete_map={"highest": "#FF9633", "lowest": "#3371FF"}, 
                 
                 )
    
    
    fig.update_xaxes(

        tickvals=combined_years["Year"],
        tickangle=45,
        

   )
    
    st.plotly_chart(fig,use_container_width=True)



'''
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
        
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

# Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                  color = "Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")

'''