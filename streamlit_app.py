import streamlit as st
import pandas as pd

# Function to load data for the first page
def load_first_data():
    return pd.read_csv('data/data_set.csv')

# Function to load data for the second page
def load_second_data():
    return pd.read_csv('data/second_data_set.csv')

# Function to filter data by city or state and company name
def filter_data(df, city=None, state=None, company_name=None):
    if 'address' in df.columns:
        if city:
            # Filter by exact match of city in address
            df = df[df['address'].str.contains(fr'\b{city}\b', case=False, regex=True)]
        
        if state:
            # Filter by exact match of state abbreviation in address
            df = df[df['address'].str.contains(fr'\b{state}\b', case=False, regex=True)]
    elif 'Company Legal Name' in df.columns:
        if company_name:
            # Filter by company name containing the input string
            df = df[df['Company Legal Name'].str.contains(company_name, case=False, na=False)]
    else:
        st.warning("No valid filter criteria found.")

    return df

# Function to generate Google Maps link
def generate_maps_link(address):
    return f"https://www.google.com/maps?q={address}&output=embed"

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
sorted_state_full_names = [f"{abbr} - {state_full_names[abbr]}" for abbr in sorted(state_full_names.keys())]

# Streamlit app
def main():
    st.title('Dispensary and Company Information Finder')

    # Sidebar navigation
    page = st.sidebar.selectbox('Go to', ['Dispensary Finder', 'Company Information'])

    if page == 'Dispensary Finder':
        st.header('Dispensary Finder')

        # Load data for the first page
        df = load_first_data()

        # Load cities and states data for filtering
        cities_states_df = pd.read_csv('data/unique_locations.csv')
        sorted_cities = cities_states_df['city'].sort_values().unique()

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
            state_abbr = selected_state_full_name.split(' - ')[0].strip()

            if state_abbr in state_full_names.keys():
                filtered_df = filter_data(df, state=state_abbr)
            else:
                st.warning(f"No data available for {selected_state_full_name}")

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
                st.write(f"No dispensaries found in {selected_state_full_name}")

    elif page == 'Company Information':
        st.header('Company Information')

        # Load data for the second page
        second_df = load_second_data()

        # State selection dropdown
        selected_state_full_name = st.selectbox('Select state', sorted_state_full_names)
        state_abbr = selected_state_full_name.split(' - ')[0].strip()

        # Company name search input
        company_name = st.text_input('Enter company name to search', '')

        if 'Company Legal Name' in second_df.columns:
            # Filter data based on selected state abbreviation and company name
            filtered_df = filter_data(second_df, state=state_abbr, company_name=company_name)

            # Display filtered company information
            if not filtered_df.empty:
                st.write(filtered_df[['Company Legal Name', 'Company emails', 'Company Phone']])
            else:
                st.write(f"No companies found in {selected_state_full_name} matching '{company_name}'.")
        else:
            st.warning("No valid filter criteria found for company information.")

if __name__ == "__main__":
    main()