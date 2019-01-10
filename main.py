import coordinate_locations as cl
import friction_factors as ff
import location_distances as ld
import pandas as pd

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
    # Determine the closest MBTA station to each zip code location
    zip_closest_station = ld.zip_closest_stations(ld.zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon))
    # Format information we already have into a dictionary with station keys and corresponding populations as values
    unique_stations, station_popularity = ld.station_popularities(zip_closest_station, zip_pop)
    
    # Get friction factors according to the gravity model
    friction_factor_estimates = ff.compute_factor_estimates(unique_stations, station_popularity, station_distances)
    # Save friction factors to CSV file for easy reference
    friction_factor_estimates.to_csv('./friction_factors/estimated_factors.csv')
    
    # Get friction factors based on actual turnstile data
    friction_factor_actuals = ff.compute_factor_actuals(turnstile_df, unique_stations, station_distances)
    # Save friction factors to CSV file for easy reference
    friction_factor_estimates.to_csv('./friction_factors/actual_factors.csv')

    friction_factor_comparison = ff.compare_factors(friction_factor_estimates, friction_factor_actuals, unique_stations)