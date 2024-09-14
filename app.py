import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Load the dataset from the provided CSV URL
file_path = 'https://linked.aub.edu.lb/pkgcube/data/df6527f0de0990b7237dbcef186a3d52_20240904_215117.csv'
df = pd.read_csv(file_path)

# Title of the app
st.title('Guest House Distribution in Batroun and Other Towns')

# Allow the user to select towns to include in the comparison
all_towns = df['Town'].unique()
selected_towns = st.multiselect('Select Towns for Comparison (including Batroun)', all_towns, default=['Batroun'])

# Filter data based on selected towns
filtered_data = df[df['Town'].isin(selected_towns)]
batroun_data = filtered_data[filtered_data['Town'] == 'Batroun']
batroun_guest_houses = batroun_data['Total number of guest houses'].sum()
total_guesthouses = filtered_data['Total number of guest houses'].sum()

# Allow the user to choose the percentage calculation method
calc_method = st.selectbox(
    'Select how to calculate percentages:',
    ['Percentage of total guest houses in all towns', 'Percentage of selected towns only']
)

if calc_method == 'Percentage of total guest houses in all towns':
    total_all_towns = df['Total number of guest houses'].sum()
    batroun_percentage = (batroun_guest_houses / total_all_towns) * 100
    other_percentage = ((total_all_towns - batroun_guest_houses) / total_all_towns) * 100
    labels = ['Batroun', 'All Other Towns']
    values = [batroun_guest_houses, total_all_towns - batroun_guest_houses]
else:
    # If the user selects percentage of selected towns only
    batroun_percentage = (batroun_guest_houses / total_guesthouses) * 100
    other_percentage = ((total_guesthouses - batroun_guest_houses) / total_guesthouses) * 100
    labels = ['Batroun', 'Other Selected Towns']
    values = [batroun_guest_houses, total_guesthouses - batroun_guest_houses]

# Add some advanced interactive widgets
show_percent = st.checkbox("Show Percentages on the Pie Chart", value=True)

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Donut chart
    textinfo='label+percent' if show_percent else 'label',
)])

# Update layout with dynamic title
fig.update_layout(
    title=f'Guest House Distribution in Batroun vs. {labels[1]} ({calc_method})',
)

# Display the pie chart
st.plotly_chart(fig)

# Show detailed percentages as a table below the chart
st.write(f'Percentage of guest houses in Batroun: {batroun_percentage:.2f}%')
st.write(f'Percentage of guest houses in {labels[1]}: {other_percentage:.2f}%')










import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data from the CSV file
file_path = 'https://linked.aub.edu.lb/pkgcube/data/df6527f0de0990b7237dbcef186a3d52_20240904_215117.csv'
df = pd.read_csv(file_path)

# Title of the app
st.title('Proportion of Towns in Lebanon with/without Hotels')

# Advanced feature: Toggle between proportions and counts
display_mode = st.radio('Display as:', ('Proportion (%)', 'Absolute Counts'))

# Advanced feature: Choose bar colors
bar_color_exist = st.color_picker('Pick a color for "Hotels Exist" bar', '#636EFA')
bar_color_not_exist = st.color_picker('Pick a color for "Hotels Do Not Exist" bar', '#EF553B')

# Calculate either proportions or counts based on the user input
if display_mode == 'Proportion (%)':
    proportions = df['Existence of hotels - does not exist'].value_counts(normalize=True) * 100
    y_label = 'Proportion (%)'
else:
    proportions = df['Existence of hotels - does not exist'].value_counts()
    y_label = 'Absolute Counts'

# Prepare data for the bar chart
x = ['Hotels Exist', 'Hotels Do Not Exist']
y = proportions.sort_index()  # Sorting to ensure 0 (does not exist) is before 1 (exists)

# Advanced feature: Toggle grid lines on or off
show_grid = st.checkbox('Show Grid Lines', value=True)

# Create the bar chart
fig = go.Figure(data=[go.Bar(
    x=x,
    y=y,
    marker=dict(
        color=[bar_color_exist, bar_color_not_exist],  # Dynamic colors based on user input
    )
)])

# Update layout
fig.update_layout(
    title=f'Distribution of Towns with/without Hotels ({display_mode})',
    title_x=0.5,  # Center the title
    xaxis_title='Hotel Existence',
    yaxis_title=y_label,
    xaxis=dict(
        title='Existence of Hotels',
        tickvals=[0, 1],
        ticktext=['Does Not Exist', 'Exists'],
        zeroline=False,  # Hide the zero line
        gridcolor='LightGray' if show_grid else 'white',  # Grid lines based on user preference
        gridwidth=1  # Width of the grid lines
    ),
    yaxis=dict(
        title=y_label,
        zeroline=False,  # Hide the zero line
        gridcolor='LightGray' if show_grid else 'white',  # Grid lines based on user preference
        gridwidth=1  # Width of the grid lines
    ),
    plot_bgcolor='white',  # Background color of the plot
    paper_bgcolor='lightgrey',  # Background color of the entire figure
    margin=dict(l=40, r=40, t=40, b=40)  # Margins around the plot
)

# Show the plot
st.plotly_chart(fig)

# Optional: Show the raw data table for better insights
if st.checkbox('Show Raw Data'):
    st.write(df)









import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'https://linked.aub.edu.lb/pkgcube/data/df6527f0de0990b7237dbcef186a3d52_20240904_215117.csv'
df = pd.read_csv(file_path)

# Streamlit app
st.title("Interactive Tourism Data Plot")

# Display dataframe head
st.write("### Data Sample")
st.write(df.head())

# Slider for 'Tourism Index'
min_index = df['Tourism Index'].min()
max_index = df['Tourism Index'].max()
selected_index = st.slider('Select Tourism Index', min_value=int(min_index), max_value=int(max_index), value=int(min_index))

# Filter data based on slider
filtered_df = df[df['Tourism Index'] == selected_index]

# Create Plotly plot
fig = px.scatter(
    filtered_df,
    x='Total number of hotels',
    y='Total number of restaurants',
    color='Town',
    hover_name='Town',
    title=f"Tourism Data for Index {selected_index}"
)

# Display plot
st.plotly_chart(fig)










import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'https://linked.aub.edu.lb/pkgcube/data/df6527f0de0990b7237dbcef186a3d52_20240904_215117.csv'
df = pd.read_csv(file_path)

# Streamlit app
st.title("Treemap of Tourism Categories")

# Get the list of unique towns for dropdown
towns = df['Town'].unique()
selected_town = st.selectbox('Select a Town:', towns)

# Filter the data for the selected town
filtered_df = df[df['Town'] == selected_town]

# Calculate total counts for the selected town
total_guesthouses = filtered_df['Total number of guest houses'].sum()
total_hotels = filtered_df['Total number of hotels'].sum()
total_cafes = filtered_df['Total number of cafes'].sum()

# Create a DataFrame for the treemap
df_treemap = pd.DataFrame({
    'Category': ['Guest Houses', 'Hotels', 'Cafes'],
    'Count': [total_guesthouses, total_hotels, total_cafes]
})

# Create the treemap chart
fig = px.treemap(df_treemap, 
                 path=['Category'], 
                 values='Count',
                 title=f"Treemap of Tourism Categories in {selected_town}")

# Display the treemap chart
st.plotly_chart(fig)


