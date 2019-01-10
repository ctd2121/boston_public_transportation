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

def station_popularities(zip_closest_station, zip_pop):
    '''
    Computes the popularity of all subway stations, based on the populations of surrounding neighborhoods.
    This function "reverses" the zip_closest_station; that is, values become keys and keys become values,
    ensuring that no duplicates are produced.
    Args:
        zip_closest_station: a dictionary with zip code keys and station values
        zip_pop: a dictionary with zip code keys and population values
    Returns:
        unique_stations: an array containing all the unique MBTA stations for which the sum of populations of
        its corresponding zip code neighborhoods is nonzero
        station_popularity: a dictionary with station keys and the sum of the populations of all zip codes to 
        which this station is closest
    '''
    # Initialize station_popularity dictionary
    station_popularity = {}
    # Initialize array that consists of all the unique MBTA stations
    unique_stations = []
    
    # For all zip codes in zip_closest_station dictionary
    for zip_code in zip_closest_station:
        # Retrieve the MBTA station that this zip code neighborhood is closest to
        station = zip_closest_station[zip_code]
        # If the station is not already a key in the station_popularity dictionary
        if station not in station_popularity:
            # Add it as a key with value equal to the population of the zip code neighborhood
            station_popularity[station] = zip_pop[zip_code]
            # Append station name to unique_stations array
            unique_stations.append(station)
        # If the station is already a key in the station_popularity dictionary
        else:
            # Increment the dictionary value by the population of the zip code neighborhood
            station_popularity[station] = station_popularity[station] + zip_pop[zip_code]
    
    return unique_stations, station_popularity
    
    
    
    
    
