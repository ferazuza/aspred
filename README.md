# aspred
Astronomical Seeing Prediction

Fernando Abárzuza Ascasso @ Light Bridges and LJMU

This repository relies on two types of data: local data and remote data. 
## Local data
Local data consists on csv files which contain old data from different weather stations. This is not included in the repository. Follow this steps:
1. Download the zip file from https://drive.google.com/open?id=1RWEHqkVWTuegDqZbrimESl1GKRfVqnw6&usp=drive_fs
2. Unzip the file in the root folder of the repository.

## Remote data
Remote data is accessed through Influx queries and MySQL queries. You need credentials to access this data. Follow the instructions in the 'Setting up credentials' section to set up your credentials.

## Setting up credentials 
In order to run the application, you need to set up your credentials. We provide an example credentials file named 'credentials.example.yaml' located in the 'notebooks' folder.

Follow these steps to set up your credentials:

1. Navigate to the 'notebooks' folder.
2. Make a copy of the 'credentials.example.yaml' file and rename it to 'credentials.yaml'.
3. Open 'credentials.yaml' in a text editor.
4. Fill in the required parameters with your credentials.

Alternatively, if you have been given a 'credentials.yaml' file, you can simply place it inside the 'notebooks' folder.

Please ensure that you do not commit the 'credentials.yaml' file to your version control system to keep your credentials secure.