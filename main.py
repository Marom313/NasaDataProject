"""
Name: Marom Gigi
    ID: 302583380
"""

print("---------------------------------Maman 16---------------------------------")
import pandas as pd
import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt


def load_data(file):
    """
    Gets a CSV file and convert it into a pandas DataFrame.
    :param file: any file.
    :type file: in this case, CSV
    :return: pandas DataFrame
    :rtype: DataFrame
    """
    try:
        df = pd.read_csv(file)
        print(f"The file: '{file}' loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error:\nThe file: '{file}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error:\nThe file: '{file}' is empty.")
    except pd.errors.ParserError:
        print(f"Error:\nCould not parse the file: '{file}'.")
    except Exception as e:
        print("Unexecpted error")

    return None


def mask_data(df):
    """Gets a DataFrame and filters it to include only rows where the
    'Close Approach Date' is in the year 2000 or later."""
    df["Close Approch Date"] = pd.to_datetime(
        df["Close Approach Date"], errors="coerce"
    )
    return df[df["Close Approch Date"].dt.year >= 2000]


def data_details(df):
    """
    Cleans columns from the dataFrame and returns a summary details on the table created.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: summary details
    :rtype: dict
    """
    columns_to_erase = ["Equinox", "Neo Reference ID", "Orbiting Body"]
    existing_columns = [i for i in columns_to_erase if i in df.columns]
    df = df.drop(columns=existing_columns)
    return (
        df.shape[1],
        df.shape[0],
        list(df.columns),
    )  # A tuple of number of rows, number of columns and a list of headlines from the table.


def max_absolute_magnitude(df):
    """
     Finds the maximum absolute magnitude from the dataFrame, and the name of it,
     and return it as a tuple.
    :param df: pandas DataFrame
     :type df: pd.DataFrame
     :return: tuple (name, MaxMagnitude)
    """
    max_index = df["Absolute Magnitude"].idxmax()
    name = df.at[max_index, "Name"]
    max_magnitude = df.at[max_index, "Absolute Magnitude"]
    return name, float(max_magnitude)


def closest_to_earth(df):
    """
    Finds the name of the asteroid that got closest to Earth, based on the column 'Miss Dist.(kilometers)'.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: The name of the closest asteroid
    :rtype: str ""
    """
    closest_index = df["Miss Dist.(kilometers)"].astype(float).idxmin()
    close_to_earth = df.at[closest_index, "Name"]
    return close_to_earth


def common_orbit(df):
    """
    Counts how many asteroids are in each unique orbit ID.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: Dictionary of orbit ID to number of occurrences
    :rtype: dict
    """

    return df["Orbit ID"].value_counts().to_dict()


def min_max_diameter(df):
    """
    Counts how many asteroids have a maximum diameter above the average maximum diameter.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: Number of asteroids above the average diameter
    :rtype: int
    """

    convert_diameters = pd.to_numeric(df["Est Dia in KM(max)"], errors="coerce")
    average_diameter = convert_diameters.mean()
    count_above_average_diameter = convert_diameters[
        convert_diameters > average_diameter
    ].count()
    return count_above_average_diameter


def plt_hist_diameter(df):
    """
    Displays a histogram of the average estimated diameter of asteroids using min and max values.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: None
    """

    diameter_min = pd.to_numeric(df["Est Dia in KM(min)"], errors="coerce")
    diameter_max = pd.to_numeric(df["Est Dia in KM(max)"], errors="coerce")
    average_diameter = (diameter_min + diameter_max) / 2

    plt.hist(average_diameter.dropna(), bins=100, color="skyblue", edgecolor="black")
    plt.title("Average Estimated Diameter of Asteroids (km)")
    plt.xlabel("Average Diameter (km)")
    plt.ylabel("Number of Asteroids")
    plt.grid(True)
    plt.show()


def plt_hist_commn_orbit(df):
    """
    Displays a histogram showing the distribution of the 'Minimum Orbit Intersection' values.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: None
    """

    min_orbit_intersection = pd.to_numeric(
        df["Minimum Orbit Intersection"], errors="coerce"
    )

    plt.hist(
        min_orbit_intersection.dropna(), bins=10, color="lightgreen", edgecolor="black"
    )
    plt.title("Minimum Orbit Intersection of Asteroids (km)")
    plt.xlabel("Minimum Orbit Intersection value")
    plt.ylabel("Number of Asteroids")
    plt.grid(True)
    plt.show()


def plt_pie_hazard(df):
    """
    Displays a pie chart showing the percentage of hazardous vs non-hazardous asteroids.
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: None
    """

    counts = df["Hazardous"].value_counts()
    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["tomato", "lightgray"],
    )
    plt.title("Hazardous vs Non-Hazardous Asteroids")
    plt.axis("equal")
    plt.show()


def plt_linear_motion_magnitude(df):
    """
    Displays a scatter plot showing the relationship between miss distance (km) and relative velocity (mph).
    :param df: pandas DataFrame
    :type df: pd.DataFrame
    :return: None
    """


    miss_dist = pd.to_numeric(df["Miss Dist.(kilometers)"], errors="coerce")
    print(df.columns)
    speed = pd.to_numeric(df["Relative Velocity km per hr"], errors="coerce")

    plt.scatter(miss_dist, speed, alpha=0.6, color="purple")
    plt.title("Miss Distance vs Relative Speed")
    plt.xlabel("Miss Distance (km)")
    plt.ylabel("Relative Velocity (mph)")
    plt.grid(True)
    plt.show()


def main():

    # Assigning the file
    file_path = "nasa.csv"

    # Load the data
    df = load_data(file_path)
    if df is None:
        return

    # Filter by year 2000 and above
    df = mask_data(df)

    # Clean and get details
    num_cols, num_rows, headers = data_details(df)
    print(f"Number of columns: {num_cols}")
    print(f"Number of rows: {num_rows}")
    print(f"Headers: {headers}")

    # Max absolute magnitude
    name_max_mag, max_mag = max_absolute_magnitude(df)
    print(f"Asteroid with max absolute magnitude: {name_max_mag}, Value: {max_mag}")

    # Closest to Earth
    closest_name = closest_to_earth(df)
    print(f"Closest asteroid to Earth: {closest_name}")

    # Most common orbits
    orbit_dict = common_orbit(df)
    print(f"Most common orbit counts: {orbit_dict}")

    # Diameter above average
    count_above_avg_diameter = min_max_diameter(df)
    print(
        f"Number of asteroids with diameter above average: {count_above_avg_diameter}"
    )

    # Visualizing
    plt_hist_diameter(df)
    plt_hist_commn_orbit(df)
    plt_pie_hazard(df)
    plt_linear_motion_magnitude(df)


if __name__ == "__main__":
    main()

print("----------------------------Made By Marom Gigi----------------------------")
