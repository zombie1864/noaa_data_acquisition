import os 
import pathlib
import logging 
import ftplib
from business_logic.utils_IO_bound import fetch_noaa_ftp_data, logger
this_dir = os.path.dirname(os.path.realpath(__file__)) 
dir_path = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw'
csv_filepath = pathlib.Path(this_dir) / 'data' / 'station-metadata.csv'


def main():
    attempts = 1 
    while attempts <= 3: 
        try: 
            fetch_noaa_ftp_data(2016, 2022, dir_path, csv_filepath) 
        except ftplib.all_errors: 
            if attempts < 3: 
                logger.warning('Error accured with FTP connection - reattemping connection')
            else: 
                logger.error('EXIT: FTP connection failed on 3rd attempt - closing connection')
        finally:
            attempts += 1 


if __name__ == '__main__': 
    logging.basicConfig(level=logging.INFO)
    main() 