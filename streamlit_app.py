import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv('data/googlelinks2.csv')

# Load cities and states data
cities_states_df = pd.read_csv('data/unique_locations.csv')

# Sort cities and states in ascending order
sorted_cities = cities_states_df['city'].sort_values().unique()
sorted_states = cities_states_df['state'].sort_values().unique()

# Function to filter data by city or state
def filter_data(df, city=None, state=None):
    if city:
        # Filter by exact match of city in address
        return df[df['address'].str.contains(fr'\b{city}\b', case=False, regex=True)]
    elif state:
        # Filter by exact match of state abbreviation in address
        return df[df['address'].str.contains(fr'\b{state}\b', case=False, regex=True)]
    return df

def generate_maps_link(address):
    return f"https://www.google.com/maps?q={address}&output=embed"

# Streamlit app
st.title('Dispensary Finder')

# Sidebar for filtering options
st.sidebar.title('Filter Options')
filter_option = st.sidebar.selectbox('Filter by', ['City', 'State'])

# City selection dropdown
if filter_option == 'City':
    city = st.sidebar.selectbox('Select city', sorted_cities)
    filtered_df = filter_data(df, city=city)
else:
    # State selection dropdown
    state = st.sidebar.selectbox('Select state', sorted_states)
    filtered_df = filter_data(df, state=state)

# Sort filtered results by dispensary name
filtered_df = filtered_df.sort_values(by='name')

# Display filtered results
if not filtered_df.empty:
    dispensary = st.selectbox('Choose a dispensary', filtered_df['name'].unique())
    dispensary_details = filtered_df[filtered_df['name'] == dispensary].iloc[0]
    
    st.write(f"**Name:** {dispensary_details['name']}")
    st.write(f"**Address:** {dispensary_details['address']}")
    st.write(f"**Phone Number:** {dispensary_details['phone_number']}")
    
    # Generate Google Maps embed link based on selected dispensary's address
    map_link = generate_maps_link(dispensary_details['address'])
    
    st.markdown(f"### Google Maps View")
    st.components.v1.iframe(map_link, height=500)
else:
    if filter_option == 'City':
        st.write(f"No dispensaries found in {city}.")
    elif filter_option == 'State':
        st.write(f"No dispensaries found in {state}.")