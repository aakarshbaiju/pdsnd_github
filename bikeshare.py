import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months_dict = {
    'january': 0,
    'february': 1,
    'march': 2,
    'april': 3,
    'may': 4,
    'june': 5,
}

days_dict = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input(
            "Enter the city whose dataset you would like to analyze (chicago, new york city, washington): ").strip().lower()
        print(city)

        if city not in CITY_DATA:
            print(
                "It seems like you have provided an incorrect option. Please try again.")
            continue

        break

    while True:
        month = input(
            "Enter the month to analyze or type 'all' to include every month: ").strip().lower()

        if month not in ['january', 'february', 'march', 'april', 'june', 'all']:
            print(
                "It seems like you have provided an incorrect option. Please try again.")
            continue
        break

    while True:
        day = input(
            "Enter the day of the week to analyze or type 'all' to include every day of the week: ").strip().lower()

        if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print(
                "It seems like you have provided an incorrect option. Please try again.")
            continue
        break

    print('-'*40)
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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if (month != 'all'):

        df = df[df['Start Time'].dt.month == months_dict[month]]

    if (day != 'all'):
        df = df[df['Start Time'].dt.weekday == days_dict[day]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month_name()
    month = df['month'].mode()[0]
    print("Frequently Travelled Month: ", month)

    df['day'] = df['Start Time'].dt.day_name()
    day = df['day'].mode()[0]
    print('Frequently Travelled Day: ', day)

    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    print('Frequently Travelled Hour: ', hour)

    display_execution_time(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Popular Start Station: ', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Popular End Station: ', popular_end_station)

    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('Most popular trip taken: ', popular_trip)

    display_execution_time(start_time)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total trip duration: ', df['Trip Duration'].sum())

    print('Average trip duration', df['Trip Duration'].mean())

    display_execution_time(start_time)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User type stats: \n')
    print(user_types.to_frame())

    try:
        gender = df['Gender'].value_counts()
        print("Gender stats: \n")
        print(gender)
    except:
        print('Washington has no gender data for analysis')

    try:
        earliest_dob_year = df['Birth Year'].min()
        recent_dob_year = df['Birth Year'].max()
        common_dob_year = df['Brith Year'].mode()[0]

        print('Date of Birth Stats: \n')
        print('Earliest year of birth: ', earliest_dob_year)
        print('Most recent of birth: ', recent_dob_year)
        print('Most common year of birth: ', common_dob_year)
    except:
        print('Washington has no birth year records for analysis')

    display_execution_time(start_time)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data (yes/no)?\n')
    start_loc = 0

    if view_data == 'no':
        return
    
    while (start_loc < len(df.index) and view_data == 'yes'):
        print(df.iloc[start_loc: start_loc + 5])        
        start_loc += 5
        rem = len(df.index) - start_loc
        view_data = input("Do you wish to continue? (Remaining records: {}): ".format(rem)).lower()

def display_execution_time(start_time):
    print("\nThis took %s seconds." % (time.time() - start_time)) 
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
