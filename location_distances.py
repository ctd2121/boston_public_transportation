import math
import numpy as np
import pandas as pd

def station_dist_matrix(stations, station_lat, station_lon):
    '''
    Computes the Euclidean distances between MBTA stations
    Args:
        stations: an array of strings indicating the MBTA stations
        lat: a dictionary with MBTA station keys and latitude coordinate values
        lon: a dictionary with MBTA station keys and longitude coordinates values
    Returns:
        distance: a dataframe/matrix whose entry (i,j) represents the distance from station i to station j
    '''
    # Instantiate distance matrix as a dataframe
    distance = pd.DataFrame(columns=list(stations), index=list(stations))
    
    # Fill in distance matrix with Euclidean distances between stations
    # Note: entry (i,j) is equivalent to entry (j,i)
    for i in range(len(stations)):
        for j in range(i+1, len(stations)):
            lat_dist = station_lat[stations[i]] - station_lat[stations[j]]
            lon_dist = station_lon[stations[i]] - station_lon[stations[j]]
            # Compute distance
            dist = math.sqrt((lat_dist ** 2) + (lon_dist ** 2))
            distance.loc[stations[i]][stations[j]] = dist
            distance.loc[stations[j]][stations[i]] = dist
    
    # Add zeros along horizontal of matrix
    for i in range(len(distance)):
        distance.iloc[i][i] = 0.0
    
    return distance

def zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon):
    '''
    Computes the Euclidean distances between zip code locations to MBTA stations
    Args:
        zip_lat: a dictionary with zip code keys and latitude coordinate values
        zip_lon: a dictionary with zip code keys and longitude coordinate values
        station_lat: a dictionary with MBTA station keys and latitude coordinate values
        station_lon: a dictionary with MBTA station keys and longitude coordinate values
    Returns:
        distance: a dataframe/matrix whose entry (i,j) represents the distance from zip code i to station j
    '''
    # Get list of all unique zip codes
    zips = [key for key in zip_lat]
    # Get list of all unique MBTA stations
    stations = [key for key in station_lat]
    
    # Instantiate distance matrix as a dataframe: rows = stations, columns = zip codes
    distance = pd.DataFrame(columns=list(zips), index=list(stations))
    
    # Fill in distance matrix with Euclidean distances between zip codes and stations
    for i in range(len(zips)):
        for j in range(len(stations)):
            lat_dist = station_lat[stations[j]] - zip_lat[zips[i]]
            lon_dist = station_lon[stations[j]] - zip_lon[zips[i]]
            # Compute distance
            dist = math.sqrt((lat_dist ** 2) + (lon_dist ** 2))
            distance.loc[stations[j]][zips[i]] = dist

    return distance

def zip_closest_stations(station_zip_dist):
    '''
    Computes the nearest MBTA station for residents of each zip code.
    Args:
        station_zip_dist: a dataframe denoting the distances between all stations and all zip codes
    Returns:
        zip_closest_station: a dictionary with zip code keys and station values
    '''
    zip_closest_station = {} # Initialize dictionary
    zip_cols = station_zip_dist.columns # Get list of all zip codes
    for i in range(station_zip_dist.shape[1]): # For every column in dataframe
        min_dist = 10 # Initialize min_dist to an arbitrarily large value
        for j in range(station_zip_dist.shape[0]): # For every row in dataframe
            if station_zip_dist.iloc[j][i] < min_dist: # If distance from zip code to station is less than min_dist
                min_dist = station_zip_dist.iloc[j][i] # Set min_dist to this minimum value
                # Get the name of the station (row) that corresponds to min_dist
                closest_station = station_zip_dist[station_zip_dist[zip_cols[i]]==min_dist].index.item()
                # Update zip_closest_station dictionary
                zip_closest_station[zip_cols[i]] = closest_station
    return zip_closest_station    
