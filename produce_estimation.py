import coordinate_locations as cl
import location_distances as ld
import pandas as pd

if __name__ == '__main__':
    # Read in turnstile data
    turnstile_df = pd.read_csv('./data/turnstile_data.csv')
    # Get all unique MBTA station names for which we have turnstile data
    stations = turnstile_df.station.unique()
    
    zip_pop, zip_lat, zip_lon = cl.get_zip_coords()
    station_lat, station_lon = cl.get_station_coords()
    station_distances = ld.station_dist_matrix(stations, station_lat, station_lon)
    station_zip_dist = ld.zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon)
    zip_closest_station = ld.zip_closest_stations(station_zip_dist)