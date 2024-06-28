import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv('data/googlelinks2.csv')

# Load cities and states data
cities_states_df = pd.read_csv('data/unique_locations.csv')

# Sort cities and states in ascending order
sorted_cities = cities_states_df['city'].sort_values().unique()
sorted_states = cities_states_df['state'].sort_values().unique()

# State abbreviation to full name mapping
state_full_names = {
    'AB': 'Alberta', 'AK': 'Alaska', 'AR': 'Arkansas', 'OK': 'Oklahoma', 'AZ': 'Arizona',
    'BC': 'British Columbia', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'NY': 'New York',
    'DC': 'District of Columbia', 'MD': 'Maryland', 'DE': 'Delaware', 'PA': 'Pennsylvania', 'FL': 'Florida',
    'HI': 'Hawaii', 'IA': 'Iowa', 'IL': 'Illinois', 'SD': 'South Dakota', 'LA': 'Louisiana',
    'MA': 'Massachusetts', 'RI': 'Rhode Island', 'VT': 'Vermont', 'MB': 'Manitoba', 'ME': 'Maine',
    'MI': 'Michigan', 'MO': 'Missouri', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MT': 'Montana',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NL': 'Newfoundland and Labrador', 'NM': 'New Mexico', 'NV': 'Nevada', 'OH': 'Ohio', 'ON': 'Ontario',
    'OR': 'Oregon', 'WA': 'Washington', 'SC': 'South Carolina', 'SK': 'Saskatchewan', 'UT': 'Utah',
    'WV': 'West Virginia', 'YT': 'Yukon Territory'
}

# Generate full state names for the dropdown
sorted_state_full_names = [f"{abbr} - {state_full_names[abbr]}" for abbr in sorted_states]

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
    selected_state_full_name = st.sidebar.selectbox('Select state', sorted_state_full_names)
    # Find the corresponding state abbreviation
    state = None
    for abbr, full_name in state_full_names.items():
        if selected_state_full_name.endswith(full_name):
            state = abbr
            break
    
    if state:
        filtered_df = filter_data(df, state=state)
    else:
        st.write(f"No abbreviation found for {selected_state_full_name}.")

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
        st.write(f"No dispensaries found in {selected_state_full_name}.")