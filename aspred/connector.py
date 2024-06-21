import numpy as np
import pandas as pd
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

from aspred.utils import standard_angle


def r2d2_seeing(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    This function returns the seeing data from the R2D2 database for the given date range.

    Parameters:
    start_date (datetime): The start date of the date range.
    end_date (datetime): The end date of the date range.

    Returns:
    pd.DataFrame: A DataFrame containing the seeing data for the given date range.
    """
    target_url = "astro.ing.iac.es/seeing/r2d2_data.php"
    str1 = start_date.strftime("%Y-%m-%d")
    str2 = end_date.strftime("%Y-%m-%d")
    url = f"https://{target_url}?date1={str1}&date2={str2}&submit=Submit"

    print(f"Fetching data from {url}...")

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and print the text content of the webpage preserving line breaks
        text_with_line_breaks = soup.get_text(separator='\n')

        # Replace multiple consecutive line breaks with a single one
        text_with_line_breaks = re.sub(r'\n+', '\n', text_with_line_breaks)

        print("Data retrieved successfully")

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        text_with_line_breaks = ""

    text = text_with_line_breaks.split("\n")

    dates = []
    seeings = []

    for i, line in enumerate(text):
        if i > 2:
            date = line[0:18]
            seeing = line[23:]
            dates.append(date)
            seeings.append(float(seeing))

    dates = pd.to_datetime(pd.Series(dates), format="%Y-%m-%d %H:%M:%S")
    seeings = pd.Series(seeings)

    frame = {"Date": dates, "Seeing": seeings}
    df = pd.DataFrame(frame)

    return df


def lt_data(path: str = "../data/meteo_lt.dat") -> pd.DataFrame:
    """
    This function reads the data from a LT weather formatted file and returns it as a DataFrame.
    :param path: The path to the file where the data is stored.
    :return: df1: A DataFrame containing the data from the file.
    """

    col_names = ["date", "wms_status", "rain_flag", "moisture_flag", "truss_temp", "oil_temp", "wind_speed",
                 "wind_direction", "ambient_temp", "dew_point", "humidity", "air_pressure", "light"]
    df1 = pd.read_csv(path, sep=" ", names=col_names, parse_dates=[0], date_format="%Y-%m-%d%H:%M:%SUTC")
    df1["wind_direction_radians"] = df1["wind_direction"].apply(lambda x: standard_angle(np.radians(x)))
    return df1


from datetime import datetime


def decode_CMT_line(line: str) -> list:
    """ Decodes a line from the CMT weather data file and returns a list with the values

    :param line: str
        Line from the CMT weather data file

    :return: list
        List with the values
    """

    line = line.split(" ")
    line = [i for i in line if i]
    return line


def cmt_data(path: str = "../data/carlsberg.weather.data/janjun96.met") -> pd.DataFrame:
    """ Imports the CMT weather data and returns a pandas DataFrame

    :param path: str
        Path to the CMT weather data file

    :return: pd.DataFrame
        DataFrame with the CMT weather data
    """
    date_list = []
    pressure_list = []
    temperature_list = []
    wind_speed_list = []
    wind_direction_list = []
    humidity_list = []
    interior_temperature_list = []
    acceptance_list = []

    for line in open(path):
        line = decode_CMT_line(line)
        date = datetime(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
        date_list.append(date)
        pressure_list.append(float(line[6]))
        temperature_list.append(float(line[7]))
        wind_speed_list.append(float(line[8]))
        wind_direction_list.append(float(line[9]))
        humidity_list.append(float(line[10]))
        interior_temperature_list.append(float(line[11]))
        acceptance_list.append(int(line[12]))

    df = pd.DataFrame()
    df["date"] = date_list
    df["pressure"] = pressure_list
    df["temperature"] = temperature_list
    df["wind_speed"] = wind_speed_list
    df["wind_direction"] = wind_direction_list
    df["humidity"] = humidity_list
    df["interior_temperature"] = interior_temperature_list
    df["acceptance"] = acceptance_list

    return df


def query_from_lt_header(query: str) -> pd.DataFrame:
    """
    This function queries the LT MySQL database and returns the results as a DataFrame.

    :param query: The SQL query to be executed.
    :return: A DataFrame containing the results of the query.
    """
    import mysql.connector

    mydb = mysql.connector.connect(
        host="150.204.240.8",
        user="ffh_ro",
        password="ffhcaotLTfhk",
        charset='utf8',
        database="fullfitsheaders"
    )

    dataframe = pd.read_sql(query, mydb)
    return dataframe

def import_from_gtc() -> pd.DataFrame:
    """
    This function imports CSV data from the GTC weather station and returns it as a DataFrame.

    :return: A DataFrame containing the data from the CSV file.
    """

    path = "../data/gtc_Report_01-01-2020_22-05-2024_10min.csv"

    df = pd.read_csv(path, sep=",", skiprows=1, parse_dates=[0], date_format="%Y-%m-%d %H:%M:%S", na_values="Null")

    # Set column names
    df.columns = ["date", "wind_speed", "wind_direction", "temperature", "humidity", "pressure", "dew_point"]

    #df["wind_speed"]=df["wind_speed"].astype(float)
    #df["wind_direction"]=df["wind_direction"].astype(float)

    df["wind_direction_radians"] = df["wind_direction"].apply(lambda x: standard_angle(np.radians(x)))

    return df


