import streamlit as st
from models import Census

st.sidebar.title("Census Assumptions")

census_types = ["IL", "AL", "MC"]
censuses = {}

for census_type in census_types:
    st.sidebar.subheader(f"Census Type: {census_type}")

    start_date = st.sidebar.date_input(f"{census_type} Start Date")
    total_units = st.sidebar.number_input(f"{census_type} Total Units", min_value=0)
    occupied_units = st.sidebar.number_input(f"{census_type} Occupied Units", min_value=0, max_value=total_units)
    occupancy_cap = st.sidebar.slider(f"{census_type} Occupancy Cap", min_value=0.0, max_value=1.0, step=0.01)
    second_person_percentage = st.sidebar.slider(f"{census_type} Second Person Percentage", min_value=0.0, max_value=1.0, step=0.01)

    if st.sidebar.button(f"Create {census_type} Census"):
        census = Census(start_date, total_units, occupied_units, occupancy_cap, second_person_percentage, census_type)
        censuses[census_type] = census
        st.sidebar.write(f"{census_type} Census created successfully.")

st.sidebar.write("Created Censuses:", censuses.keys())

# Display tables in main panel
for census_type, census in censuses.items():
    st.subheader(f"{census_type} Census Projection")
    st.table(census.get_projection())
