import streamlit as st
from models import Census, OverallCensus, RentalRate, LaborFTE

st.sidebar.title("Select Page")

page = st.sidebar.selectbox("Choose a page", ["Census", "Overall Census", "Rental Rate", "Labor FTE"])

if page == "Census":
    st.title("Census Assumptions")

    available_census_types = ["IL", "AL", "MC"]
    selected_census_types = st.multiselect("Select Census Types", available_census_types)

    censuses = {}

    for census_type in selected_census_types:
        st.subheader(f"Census Type: {census_type}")

        start_date = st.date_input(f"{census_type} Start Date")
        total_units = st.number_input(f"{census_type} Total Units", min_value=0)
        occupied_units = st.number_input(f"{census_type} Occupied Units", min_value=0, max_value=total_units)
        occupancy_cap = st.slider(f"{census_type} Occupancy Cap", min_value=0.0, max_value=1.0, step=0.01)
        second_person_percentage = st.slider(f"{census_type} Second Person Percentage", min_value=0.0, max_value=1.0, step=0.01)

        if st.button(f"Create {census_type} Census"):
            census = Census(start_date, total_units, occupied_units, occupancy_cap, second_person_percentage, census_type)
            census.populate_projection()  # Populate the DataFrame
            censuses[census_type] = census
            st.write(f"{census_type} Census created successfully.")

        st.write("Created Censuses:", censuses.keys())

        # Display tables
        for census_type, census in censuses.items():
            st.subheader(f"{census_type} Census Projection")
            st.dataframe(census.get_projection())

elif page == "Overall Census":
    st.title("Overall Census Page")
    # Add your code for the Overall Census page here

elif page == "Rental Rate":
    st.title("Rental Rate Page")
    # Add your code for the Rental Rate page here

elif page == "Labor FTE":
    st.title("Labor FTE Page")
    # Add your code for the Labor FTE page here
