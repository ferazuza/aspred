import pandas as pd
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


def R2D2_seeing(start_date: datetime, end_date: datetime)-> pd.DataFrame:
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