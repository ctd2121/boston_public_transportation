import coordinate_locations as cl
import friction_factors as ff
import location_distances as ld
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def visualize_results(friction_factor_comparison):
    '''
    Displays a heatmap of friction factor comparisons between actual factors and estimated factors.
    Args:
        friction_factor_comparison: a pandas dataframe, in which each entry represents the friction factor between two MBTA stations
    '''    
    # Visualize comparison of actual to estimated friction factors as a heatmap
    # Fill NAs (the only cell this line of code modifies is the top left corner cell, which is considered to be NA by pandas because it is blank)
    friction_factor_comparison.fillna(value=np.nan, inplace=True)
    # View heatmap
    ax = sns.heatmap(friction_factor_comparison,
                cmap='RdYlGn_r',
                linewidths=0.5,
                annot=False)
    ax.invert_yaxis() # Reverse order of y-axis for visual aid
    ax.set_title('MBTA Station Friction Factors: Comparison')
    plt.show()

if __name__ == '__main__':
    # Read in turnstile data
    # Data from https://github.com/mbtaviz/mbtaviz.github.io/
    turnstile_df = pd.read_csv('./data/turnstile_data.csv')
    # Get all unique MBTA station names for which we have turnstile data
    stations = turnstile_df.station.unique()
    
    # Get latitude, longitude coordinates and populations for each zip code
    zip_pop, zip_lat, zip_lon = cl.get_zip_coords()
    # Get latitude, longitude coordinations for each MBTA station
    station_lat, station_lon = cl.get_station_coords()
    
    # Get the distances (in Euclidean coordinate metrics) between all MBTA stations
    station_distances = ld.station_dist_matrix(stations, station_lat, station_lon)
    # Determine the closest MBTA station to each zip code neighborhood
    zip_closest_station = ld.zip_closest_stations(ld.zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon))
    # Format information that we already have into a dictionary with station keys and corresponding populations as values
    unique_stations, station_popularity, total_pop = ld.station_popularities(zip_closest_station, zip_pop)
    
    # Get friction factors according to the gravity model
    friction_factor_estimates = ff.compute_factor_estimates(unique_stations, station_popularity, station_distances, total_pop)
    # Save friction factors to CSV file for easy reference
    friction_factor_estimates.to_csv('./friction_factors/estimated_factors.csv')
    
    # Get friction factors based on actual turnstile data
    friction_factor_actuals = ff.compute_factor_actuals(turnstile_df, unique_stations, station_distances)
    # Save friction factors to CSV file for easy reference
    friction_factor_estimates.to_csv('./friction_factors/actual_factors.csv')
    
    # Generate a dataframe that displays a comparison (in ratios) of actual versus estimated friction factors
    friction_factor_comparison = ff.compare_factors(friction_factor_estimates, friction_factor_actuals, unique_stations)
    
    # Call function that allows visualization of results using a heatmap
    visualize_results(friction_factor_comparison)