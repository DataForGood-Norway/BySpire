# Consolidating raw datasets


## Approach 1: (abandoned) Connect directly to drive
[20180927 - Download data.ipynb](20180927 - Download data.ipynb)

1. Set up a connection to google drive
Follow the instructions here to create a project and generate a credentials file https://pythonhosted.org/PyDrive/quickstart.html#authentication

2. Set up a conda environment
...


## Approach 2: Sync to local disk first and take it from there
[20180928 - Merge local data.ipynb](20180928 - Merge local data.ipynb)

- `Rclone` https://rclone.org/drive/ is a great tool for syncing things between cloud and local stores.

- Follow the instructions to configure google drive, setting the root directory id to the id of the Measurements folder (`'1h-MNPZJg32SVFueMTFzpRG7b6QR2GXiE'`).

Run a sync command to load the data to `data/Measurements` in your local clone of this repository. Don't track the datafiles on git!
- `(vfa-01) Jakes-MacBook-Pro:01-data-loads jake$ mkdir -p ../data/Measurements`
- `(vfa-01) Jakes-MacBook-Pro:01-data-loads jake$ rclone sync vfa-Measurements:/ ../data/Measurements/`

