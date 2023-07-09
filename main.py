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
    staffing_patterns = {'Executive Director': {'type': 'fixed', 'value': 1},
                         'Caregiver': {'type': 'ratio', 'value': 6, 'product_types': ['AL', 'MC']}}

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
        print(products[product_type].get_projection().head())
        print(f"\n{product_type} Rate Projection:")
        print(rental_rates[product_type].get_rate_projection().head())

    print("\nFTE Projection:")
    print(labor_fte.get_fte_projection().head(20))

if __name__ == '__main__':
    main()