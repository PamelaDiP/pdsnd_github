import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = (input("Please enter the name of the city to analyze (options are 'chicago', 'new york city' or 'washington'): \n")).lower()
    
    # check user input for validity
    while city != 'chicago' and city != 'new york city' and city != 'washington': 
        print("Invalid input.")
        print("Valid input: chicaco, new york city, or washington.")
        city = (input("Please enter either 'chicago', 'new york city' or 'washington': \n")).lower()
    
    # get user input for month (all, january, february, ... , june) 
    month = (input("Please enter the name of the month to filter by ('january', 'february', 'march', 'april', 'may' or 'june'), or 'all' to apply no month filter: \n")).capitalize()
    
    # check user input for validity
    months = ('All', 'January', 'February', 'March', 'April', 'May', 'June')
    while month not in months:
        print("Invalid input.")
        month = (input("Please enter either 'january', 'february', 'march', 'april', 'may', 'june' or 'all': \n")).capitalize()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = (input("Please enter the name of the weekday to filter by (e.g. 'monday', 'tuesday', etc.) or 'all' to apply no day filter: \n")).capitalize()
    
    # check user input for validity
    weekdays = ('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    while day not in weekdays:
        print("Invalid input.")
        day = (input("Please enter the name of the weekday to filter by (e.g. 'monday', 'tuesday', etc.) or 'all' to apply no day filter: \n")).capitalize()

    print('-'*40)
    return city, month, day


def load_raw_data(city):
    """
    Loads data for the specified city.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame containing city data
    """
    # Read data from CSV file into Pandas dataframe
    df = pd.read_csv(CITY_DATA[city])
    return df


def filter_data(raw_df,month,day):
    """Filters the data based on user input and adds 'Hour' column to dataframe.
    
    Args:
        (dataframe) Pandas Dataframe raw_df - dataframe with data of the city that was asked for by the user
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dataframe - Pandas DataFrame containing city data filtered by month and day
        """
    
    # Create copy of raw dataframe
    df = raw_df.copy()
    
    # Convert start_time to datetime format
    df['start_time'] = pd.to_datetime(df['start_time'])
    
    # Add column for Start Month
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    df['Month'] = df['start_time'].dt.month
    df["Month"].replace(months, inplace=True)
    
    # Add column for Start Day
    df['Day'] = df['start_time'].dt.day_name()
    
    # Add column for Start Hour
    df['Hour'] = df['start_time'].dt.hour
    
    # Filter dataframe on user input
    if month != 'All':
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        df = df[df['Day'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('Most Popular Month: ', popular_month)

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print('Most Popular Day: ', popular_day)

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station: ', popular_start_station,'\n')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station: ', popular_end_station,'\n')

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = 'Start Station: ' + df['Start Station'] +'\n End Station: '+ df['End Station']
    popular_station_combination = df['Station Combination'].mode()[0]
    print('The Most Popular Start And End Station Combination:\n', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("Counts of User Types:\n",user_type_count,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Counts of Gender:\n",gender_count,'\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        
        print("Earliest Birth Year of Customers: ",earliest_birth_year)
        print("Most Recent Birth Year of Customers: ",most_recent_birth_year)
        print("Most Common Birth Year of Customers: ",most_common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        raw_df = load_raw_data(city)
        df = filter_data(raw_df,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Ask the user if they want to see 5 lines of raw data
        show_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        while show_raw == 'yes':
            print(raw_df.head())
            show_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()