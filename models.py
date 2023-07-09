import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np

class Product:
    def __init__(self, start_date, total_units, occupied_units, occupancy_cap, second_person_percentage):
        self.start_date = pd.to_datetime(start_date)
        self.total_units = total_units
        self.occupied_units = occupied_units
        self.occupancy_cap = occupancy_cap
        self.second_person_percentage = second_person_percentage
        self.projection = self._create_empty_projection()

    def _create_empty_projection(self):
        """Create an empty DataFrame with DateTimeIndex."""
        projection = pd.DataFrame(
            index=pd.date_range(self.start_date, self.start_date + DateOffset(months=119), freq='MS')
        )
        projection['numeric_month'] = range(1, len(projection) + 1)
        projection['occupied_units'] = 0
        projection['vacant_units'] = self.total_units  # Initially all units are vacant
        projection['resident_count'] = 0  # Initially no residents
        projection['reached_occupancy_cap'] = False  # Initially, occupancy cap is not reached
        return projection

    def populate_projection(self):
        """Populate the DataFrame with projected occupied units."""
        self.projection.loc[self.projection.index[0], 'occupied_units'] = self.occupied_units
        self.projection.loc[self.projection.index[0], 'vacant_units'] = self.total_units - self.occupied_units
        self.projection.loc[self.projection.index[0], 'resident_count'] = np.round(self.occupied_units * (1 + self.second_person_percentage))
        self.projection.loc[self.projection.index[0], 'reached_occupancy_cap'] = self.occupied_units >= np.round(self.total_units * self.occupancy_cap)
        for month in range(1, len(self.projection)):
            # Here we apply the occupancy cap
            self.projection.loc[self.projection.index[month], 'occupied_units'] = min(
                np.round(self.projection.loc[self.projection.index[month-1], 'occupied_units'] + 1),
                np.round(self.total_units * self.occupancy_cap)
            )
            self.projection.loc[self.projection.index[month], 'vacant_units'] = self.total_units - self.projection.loc[self.projection.index[month], 'occupied_units']
            self.projection.loc[self.projection.index[month], 'resident_count'] = np.round(self.projection.loc[self.projection.index[month], 'occupied_units'] * (1 + self.second_person_percentage))
            self.projection.loc[self.projection.index[month], 'reached_occupancy_cap'] = self.projection.loc[self.projection.index[month], 'occupied_units'] >= np.round(self.total_units * self.occupancy_cap)

    def get_projection(self):
        return self.projection

class RentalRate:
    def __init__(self, base_rate, start_date, inflation_rates, concession_rates):
        self.base_rate = base_rate
        self.start_date = pd.to_datetime(start_date)
        self.inflation_rates = inflation_rates
        self.concession_rates = concession_rates
        self.rate_projection = self._create_empty_rate_projection()

    def _create_empty_rate_projection(self):
        """Create an empty DataFrame with DateTimeIndex."""
        projection = pd.DataFrame(
            index=pd.date_range(self.start_date, self.start_date + DateOffset(years=len(self.inflation_rates)), freq='MS')
        )
        projection['rate'] = 0.0
        return projection

    def populate_rate_projection(self):
        """Populate the DataFrame with projected rates."""
        for year in range(len(self.inflation_rates) + 1): 
            if year == 0:
                self.rate_projection.loc[self.rate_projection.index.year == self.start_date.year, 'rate'] = self.base_rate
            else:
                # Apply the inflation rate to the previous year's rate
                previous_rate = self.rate_projection.loc[self.rate_projection.index.year == self.start_date.year + year - 1, 'rate'].iloc[0]
                new_rate = previous_rate * (1 + self.inflation_rates[year - 1])
                # Apply the concession rate to reduce the new rate
                #new_rate = new_rate * (1 - self.concession_rates[year - 1])
                self.rate_projection.loc[self.rate_projection.index.year == self.start_date.year + year, 'rate'] = new_rate

    def get_rate_projection(self):
        return self.rate_projection

class LaborFTE:
    def __init__(self, start_date, products, staffing_patterns):
        self.start_date = pd.to_datetime(start_date)
        self.products = products  # {product_type: Product object}
        self.staffing_patterns = staffing_patterns  # {role: staffing_pattern}
        self.fte_projection = self._create_empty_fte_projection()

    def _create_empty_fte_projection(self):
        """Create an empty DataFrame with DateTimeIndex."""
        projection = pd.DataFrame(
            index=pd.date_range(self.start_date, self.start_date + DateOffset(months=119), freq='MS')
        )
        for role in self.staffing_patterns.keys():
            projection[role] = 0.0
        return projection

    def populate_fte_projection(self):
        """Populate the DataFrame with projected FTEs."""
        for month in range(len(self.fte_projection)):
            for role, pattern in self.staffing_patterns.items():
                if pattern['type'] == 'fixed':
                    self.fte_projection.loc[self.fte_projection.index[month], role] = pattern['value']
                elif pattern['type'] == 'ratio':
                    # Here, we assume 'product_types' to be either 'AL' or 'MC'
                    occupied_units = sum([self.products[product_type].get_projection().loc[self.fte_projection.index[month], 'occupied_units']
                                          for product_type in pattern['product_types']])
                    self.fte_projection.loc[self.fte_projection.index[month], role] = occupied_units / pattern['value']
                # Add more conditions here for other staffing patterns as necessary

    def get_fte_projection(self):
        return self.fte_projection