import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'feburary', 'march', 'april', 'may', 'june']
days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Type a city to explore, chicago, new york city or washington: ').lower()
        if city not in CITY_DATA.keys():
            print('Invalid choice please choose a city from the provided list')
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Type a month (january, feburary, march, april, may, june or all) to explore: ').lower()
        if month not in months:
            print('Invalid month please choose from the list provided')
            continue
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Type a day of the week to explore or all for everyday: ').lower()
        if day not in days:
            print('Invalid day of the week chosen please choose a valid day of the week or all')
            continue
        else:
            break                
            
    print('-'*40)
    #print(city, month, day)
    return city, month, day
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    #convert to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day, hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour   

    #filter by month and day
    if month != 'all':
        #months = ['january', 'feburary', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df[df['month'] == month]
    if day != 'all':
        day = days.index(day)
        df = df[df['day_of_week'] == day]
                       
    return df
     
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #find common month and standarize it    
    common_month = df['month'].mode().max()
    ind_month = int(common_month)
    print('The most common month is:', months[ind_month].title())                        

    # TO DO: display the most common day of week
    #find the common day and standarize it    
    common_day = df['day_of_week'].mode().max()
    ind_day = int(common_day)
    print('The most common day of the week:', days[ind_day].title())                            
    
        # TO DO: display the most common start hour
    #find the common hour   
    common_hour = df['hour'].mode().max()
    print('The most common hour is (24hr time):', common_hour)                            

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #find the most common start
    common_start = df['Start Station'].mode().max()
    print('The most common start station is:', common_start)

    # TO DO: display most commonly used end station
    #find most common end
    common_end = df['End Station'].mode().max()
    print('The most common end station is:', common_end)

    # TO DO: display most frequent combination of start station and end station trip
    #combine start and end stations find common combo
    df['Start_End_Station'] = df['Start Station'] +' - '+ df['End Station']
    common_combined = df['Start_End_Station'].mode().max()
    Trips = f"{common_combined} -  {df['Start_End_Station'].value_counts().max()}"
    print('The most common start and end combination and the number of trips is: ', Trips)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    #find total travel time to display in days, hours, min, sec
    travel_time = df['Trip Duration']
    #print(travel_time,'as check')
    travel_time = pd.to_timedelta(travel_time, unit = 's').sum()
    
    print(f'Total travel time for', city, 'in', month, ':',travel_time)
    
    # TO DO: display mean travel time
    #find mean (1 source for mean travel time documented in readme)
    avg_trip = df['Trip Duration'].mean()
    t_min, t_sec = divmod(avg_trip, 60)
    if t_min > 60:
        t_hr = divmod(t_min, 60)
        print('The mean travel time is: {} hour(s) {} minute(s) {} second(s)'.format(t_hr, t_min, t_sec))
    else:
        print('The mean travel time is: {} minute(s) {} second(s)'.format(t_min, t_sec))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city, month):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    #find count for each user type subscriber & customer
    
    total_count = df['User Type'].value_counts()
    count_of_sub = total_count.get('Subscriber',0)
    count_of_cust = total_count.get('Customer',0)
    
    print('The number of subscribers for', city, 'in', month, 'is', count_of_sub, '.\nThe number of customers is: ', count_of_cust,'\n')

    # TO DO: Display counts of gender
    if city == 'washington':
        print('Gender data only available for NYC and Chicago')
    else:    
        count_gender = df['Gender'].value_counts()
        count_male = count_gender.get('Male',0)
        count_female = count_gender.get('Female',0)

        print('The number of male bikers for ', city, 'in ', month, 'is', count_male, '\nThe number of female bikers is ', count_female,'\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Birth year data only available for NYC and Chicago')
    else:    
        clean_by = df['Birth Year'].dropna(axis = 0).apply(int)
        min_by = clean_by.min()
        max_by = clean_by.max()
        common_by = clean_by.mode()[0]
        print('The oldest rider was born in', min_by, '\nThe youngest rider was born in', max_by, '\nThe most common year of birth is', common_by)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """ display 5 rows of raw data from the selected csv and iterate through the data as user requests
    Args: df, the data frame to work with
    Return: none
    """
    # create variables and list of yes/no 
    view_raw_data = ['yes','no']
    raw_data = ''
    ex_data = ''
    counter = 0
    #set display to show all columns in df
    pd.set_option('display.max_columns', 13)
    while raw_data not in view_raw_data:
        print('\nWould you like to review raw data (yes, no)?')
        raw_data = input().lower()
        if raw_data not in view_raw_data:
            print('\nIncorrect response please choose yes or no')
            raw_data =input().lower()
            continue
        if raw_data == 'yes':
            ex_data = 'yes'
            print(df.head())
        elif raw_data == 'no':            
            break        
    while raw_data == 'yes': 
        print('Would you like to see more raw data(yes or no)?')
        counter = counter + 5
        ex_data = input().lower()
        if ex_data not in view_raw_data:
            print('\nIncorrect response please choose yes or no')
        if ex_data == 'yes':            
            print(df[counter:counter+5])
            #sanity check
            #print('\n',counter)
            continue
        if ex_data == 'no':
            break
          
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, city, month)
        user_stats(df, city, month)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    print('-'*40)

if __name__ == "__main__":
	main()
