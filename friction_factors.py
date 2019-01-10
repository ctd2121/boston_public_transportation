import pandas as pd

def consolidate_turnstile_data(turnstile_df, unique_stations):
    '''
    Reads in raw turnstile_data.csv file and formats it in a way that facilitates analysis
    Args:
        turnstile_df: the raw turnstile_data.csv file as a pandas dataframe
        unique_stations: an array consisting of all the unique MBTA stations for which data was scraped
    Returns:
        turnstile_df: an array consisting of all the unique MBTA stations, and corresponding enter and exit values
    '''    
    # Filter out unnecessary observations from turnstile_df
    # There are 63 unique stations in turnstile data, but we are narrowing our analysis down to 20 for simplicity
    # This decreases the size of turnstile_df from ~1.9m rows to ~600k rows
    turnstile_df = turnstile_df[turnstile_df.station.isin(unique_stations)]

    # Ensure the station names of both data sources are identical
    assert sorted(turnstile_df.station.unique()) == sorted(unique_stations)

    # Aggregate the turnstile_df data into 20 rows, each representing a unique station
    # We group by station name while summing the total entries and exits that occur at each station
    turnstile_df = turnstile_df.groupby('station').sum()
    
    return turnstile_df

def compute_factor_estimates(unique_stations, station_popularity, station_distances):
    '''
    Computes the friction factors between all MBTA stations based on populations of nearby zip code neighborhoods
    and distances between stations.
    Args:
        unique_stations: an array containing all the unique MBTA stations for which the sum of populations of
        its corresponding zip code neighborhoods is nonzero
        station_distances: a pandas dataframe/matrix holding the distances between all MBTA stations in the unique_stations array
    Returns:
        friction_estimates: a pandas dataframe/matrix holding the friction factors between all MBTA stations in the unique_stations array
    '''
    # Instantiate dataframe friction_estimates, with MBTA stations as both rows and columns
    # Entry (i,j) in this matrix will represent the friction factor between station i and station j
    # This dataframe ends up being of shape 20 x 20
    friction_estimates = pd.DataFrame(columns=list(unique_stations), index=list(unique_stations))
    
    for i in range(len(friction_estimates)): # For every row in friction_estimates dataframe
        for j in range(len(friction_estimates)): # For every column in friction_estimates dataframe
            # Compute friction factor between station i and station j
            # Get the ratio of station popularities = (station i popularity) / (station j popularity)
            pop_ratio = float(station_popularity[friction_estimates.index[i]]) / float(station_popularity[friction_estimates.columns[j]])
            
            # Multiply pop_ratio by the distance between station i and station j
            fric_factor = float(pop_ratio) * float(station_distances.loc[friction_estimates.index[i]][friction_estimates.columns[j]])
            
            # Enter the friction factor into the appropriate position in the dataframe
            # This represents the "friction" between two stations
            # A high friction value from station i to station j means there is relatively little transportation
            # in this direction
            friction_estimates.iloc[i][j] = fric_factor

    # For analysis purposes, multiply all values by 100
    friction_estimates = friction_estimates * 100
    
    return friction_estimates

def compute_factor_actuals(turnstile_df, unique_stations, station_distances):
    '''
    Computes the friction factors between all MBTA stations based on actual station turnstile data and distances between stations.
    Args:
        turnstile_df: the raw turnstile_data.csv file as a pandas dataframe
        unique_stations: an array consisting of all the unique MBTA stations for which data was scraped
        station_distances: a pandas dataframe/matrix indicating the coordinate distances between MBTA stations
    Returns:
        friction_actuals: a pandas dataframe/matrix holding friction factors between MBTA stations based on actual turnstile data
    '''
    df = consolidate_turnstile_data(turnstile_df, unique_stations)
    
    # Instantiate dataframe friction_actuals, with MBTA stations as both rows and columns
    # Entry (i,j) in this matrix will represent the friction factor between station i and station j
    # Although we have data to support a 63 x 63 matrix, we only had data for a 20 x 20 estimation matrix, so we will do the same
    # with the raw data to give an apples to apples comparison
    friction_actuals = pd.DataFrame(columns=list(unique_stations), index=list(unique_stations))
    
    for i in range(len(friction_actuals)): # For every row i in friction_actuals dataframe
        for j in range(len(friction_actuals)): # For every column j in friction_actuals dataframe
            # Compute friction factor between station i and station j
            # Get the ratio of station dynamics = (station i entrances) / (station j exits)
            enter_exit_ratio = float(df.loc[friction_actuals.index[i]]['entries']) / float(df.loc[friction_actuals.columns[j]]['exits'])
    
            # Multiply enter_exit_ratio by the distance between station i and station j
            fric_factor = float(enter_exit_ratio) * float(station_distances.loc[friction_actuals.index[i]][friction_actuals.columns[j]])
            
            # Enter the friction factor into the appropriate position in the dataframe
            friction_actuals.iloc[i][j] = fric_factor
    
    # For analysis purposes, multiply all values by 100
    friction_actuals = friction_actuals * 100
    
    return friction_actuals

def compare_factors(friction_factor_estimates, friction_factor_actuals, unique_stations):
    '''
    Compares the estimated friction factors that were based on scraped population data versus those calibrated based on actual
    MBTA station turnstile data.
    Args:
        friction_factor_estimates: a pandas dataframe/matrix holding friction factor estimates between MBTA stations
        friction_factor_actuals: a pandas dataframe/matrix holding friction factors between MBTA stations based on actual turnstile data
        unique_stations: an array holding all MBTA stations for which we are analyzing data
    Returns:
        friction_ratios: a dataframe that is the same size as friction_factor_estimates and friction_factor_actuals, holding respective
        ratios between actual values and estimated factors
    '''
    # Instantiate a pandas dataframe that will hold ratios of actual friction factors to estimated friction factors
    friction_ratios = pd.DataFrame(columns=list(unique_stations), index=list(unique_stations))
    
    # For every row in the friction_ratios dataframe
    for i in range(len(unique_stations)):
        # For every column in the friction_ratios dataframe
        for j in range(len(unique_stations)):
            try:
                # Compute the actual to expected ratio
                value = float(friction_factor_actuals.iloc[i][j]) / float(friction_factor_estimates.iloc[i][j])
            except: # If there is a divide by zero error
                value = 0.0 # Coerce value to be zero
            # Add value as entry into friction_ratios dataframe
            friction_ratios.iloc[i][j] = value
    return friction_ratios












