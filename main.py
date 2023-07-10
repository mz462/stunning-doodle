from models import Product, RentalRate, LaborFTE

def main():
    # Set initial parameters
    start_date = '2023-07-01'
    total_units_input = {'IL': 100, 'AL': 80, 'MC': 60}  # Just an example
    occupied_units_input = {'IL': 70, 'AL': 50, 'MC': 40}  # Just an example
    occupancy_cap_input = {'IL': 0.94, 'AL': 0.92, 'MC': 0.90}  # Just an example
    second_person_percentage_input = {'IL': 0.05, 'AL': 0.06, 'MC': 0.07}  # Just an example
    base_rates = {'IL': 3700, 'AL': 5400, 'MC': 6800}
    inflation_rates_input = {'IL': [0.04, 0.035, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03], 
                             'AL': [0.04, 0.035, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
                             'MC': [0.04, 0.035, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]}
    concession_rates_input = {'IL': [1, 0.5, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                              'AL': [1, 0.5, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                              'MC': [1, 0.5, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}
    staffing_patterns = {
    "Director of Sales & Marketing": {
        "short_hand": "DSM",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Sales and Marketing",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Sales Manager": {
        "short_hand": "SM",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Sales and Marketing",
        "is_hourly": True,
        "minimum_FTE": 1,
        "change_in_FTE": -1,
        "trigger": {"type": "occupancy", "value": 0.8},
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Commissions": {
        "short_hand": "Commission",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Sales and Marketing",
        "is_hourly": True,
        "minimum_FTE": 0,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Director of Engagement": {
        "short_hand": "DE",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Program",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Driver": {
        "short_hand": "Driver",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Program",
        "is_hourly": True,
        "minimum_FTE": 1.4,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Engagement Associate": {
        "short_hand": "EA",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Program",
        "is_hourly": True,
        "minimum_FTE": 0,
        "change_in_FTE": 1,
        "trigger": {"type": "occupancy", "value": 0.6},
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Executive Director": {
        "short_hand": "ED",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Operations",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Business Office Director": {
        "short_hand": "BOD",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Operations",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Concierge": {
        "short_hand": "Concierge",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Operations",
        "is_hourly": True,
        "minimum_FTE": 2.1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Director of Memory Care": {
        "short_hand": "DOV",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Memory Care",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "MC Care Manager": {
        "short_hand": "MCCNA",
        "type": "ratio",
        "ratio_based_on": ["MC","AL"],
        "department": "Memory Care",
        "is_hourly": True,
        "minimum_FTE": 4.2,
        "change_in_FTE": 1.4,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": 10, "PM": 10, "NOC": 20},
    },
    "MC Medication Care Manager": {
        "short_hand": "MCCMA",
        "type": "ratio",
        "ratio_based_on": ["MC"],
        "department": "Memory Care",
        "is_hourly": True,
        "minimum_FTE": 2.8,
        "change_in_FTE": 1.4,
        "trigger": None,
        "maximum_FTE": 4.2,
        "shifts_ratio": {"AM": 18, "PM": 18, "NOC": None},
    },
    "Director of Plant Operations": {
        "short_hand": "DPO",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Maintenance",
        "is_hourly": True,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Plant Operations Assistant": {
        "short_hand": "PlantOps",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Maintenance",
        "is_hourly": True,
        "minimum_FTE": 0.5,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Director of Housekeeping": {
        "short_hand": "DOH",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Housekeeping",
        "is_hourly": True,
        "minimum_FTE": 0,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Housekeeping Associate": {
        "short_hand": "Housekeeper",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Housekeeping",
        "is_hourly": True,
        "minimum_FTE": 1.4,
        "change_in_FTE": 1,
        "trigger": {"type": "occupied units", "value": 40},
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Director of Culinary Services": {
        "short_hand": "DOC",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Dining",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Chef": {
        "short_hand": "Chef",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Dining",
        "is_hourly": True,
        "minimum_FTE": 2.9,
        "change_in_FTE": 1,
        "trigger": {"type": "occupied units", "value": 80},
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Dining Room Associate": {
        "short_hand": "DM",
        "type": "ratio",
        "ratio_based_on": ["IL", "AL", "MC"],
        "department": "Dining",
        "is_hourly": True,
        "minimum_FTE": 4.9,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": 20, "PM": None, "NOC": None},
    },
    "Dish Washer": {
        "short_hand": "Washer",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Dining",
        "is_hourly": True,
        "minimum_FTE": 2,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "MC Attendant": {
        "short_hand": "MCDM",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Dining",
        "is_hourly": True,
        "minimum_FTE": 1.4,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "Director of Health & Wellness": {
        "short_hand": "DHW",
        "type": "fixed",
        "ratio_based_on": None,
        "department": "Care",
        "is_hourly": False,
        "minimum_FTE": 1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": None, "PM": None, "NOC": None},
    },
    "LPN": {
        "short_hand": "LPN",
        "type": "ratio",
        "ratio_based_on": ["AL","MC"],
        "department": "Care",
        "is_hourly": True,
        "minimum_FTE": 2.1,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 4.2,
        "shifts_ratio": {"AM": 50, "PM": None, "NOC": None},
    },
    "Medication Care Manager": {
        "short_hand": "CMA",
        "type": "ratio",
        "ratio_based_on": ["AL"],
        "department": "Care",
        "is_hourly": True,
        "minimum_FTE": 2.8,
        "change_in_FTE": None,
        "trigger": {"type": "occupied units", "value": 20},
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": 30, "PM": 30, "NOC": None},
    },
    "Care Manager": {
        "short_hand": "CNA",
        "type": "ratio",
        "ratio_based_on": ["AL"],
        "department": "Care",
        "is_hourly": True,
        "minimum_FTE": 4.2,
        "change_in_FTE": None,
        "trigger": None,
        "maximum_FTE": 999,
        "shifts_ratio": {"AM": 18, "PM": 18, "NOC": 36},
    }
}


    # Create a Product object for each product type
    products = {
        product_type: Product(
            start_date=start_date,
            total_units=total_units_input[product_type],
            occupied_units=occupied_units_input[product_type],
            occupancy_cap=occupancy_cap_input[product_type],
            second_person_percentage=second_person_percentage_input[product_type],
        )
        for product_type in ['IL', 'AL', 'MC']
    }

    # Populate the occupancy projection for each product type
    for product in products.values():
        product.populate_projection()

    # Create a RentalRate object for each product type
    rental_rates = {
        product_type: RentalRate(
            base_rate=base_rate,
            start_date=start_date,
            inflation_rates=inflation_rates_input[product_type],
            concession_rates=concession_rates_input[product_type]
            )
        for product_type, base_rate in base_rates.items()
    }

    # Populate the rate projection for each product type
    for rental_rate in rental_rates.values():
        rental_rate.populate_rate_projection()

    # Create a LaborFTE object
    labor_fte = LaborFTE(
        start_date=start_date,
        products=products,
        staffing_patterns=staffing_patterns
    )

    # Populate the FTE projection
    labor_fte.populate_fte_projection()

    # Now each product object has an occupancy projection, each rental rate object has a rate projection,
    # and labor_fte object has an FTE projection.
    # They can be accessed with product.get_projection(), rental_rate.get_rate_projection() and labor_fte.get_fte_projection() respectively

    # As an example, print the first few rows of the occupancy, rate and FTE projections for each product type

    for product_type in ['IL', 'AL', 'MC']:
        print(f"\n{product_type} Occupancy Projection:")
        occupancy_projection = products[product_type].get_projection()
        print(occupancy_projection.head())
        occupancy_projection.to_csv(f"{product_type}_occupancy_projection.csv", index=False)
        
        print(f"\n{product_type} Rate Projection:")
        rate_projection = rental_rates[product_type].get_rate_projection()
        print(rate_projection.head())
        rate_projection.to_csv(f"{product_type}_rate_projection.csv", index=False)

    print("\nFTE Projection:")
    fte_projection = labor_fte.get_fte_projection()
    print(fte_projection.head())
    fte_projection.to_csv("fte_projection.csv", index=False)


if __name__ == '__main__':
    main()