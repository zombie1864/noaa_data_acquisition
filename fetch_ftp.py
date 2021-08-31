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
            fetch_noaa_ftp_data(2021, 2022, dir_path, csv_filepath) 
            ''' NOTE NOTE consider using a generator rather than a list comprehenion to get fatser results NOTE NOTE 
                    ⮑ as it stands if you run the fetch method for 2016 - 2022 you will have a runtime of abt 30 mins or so 
                        ⮑ instead see if by using a generator will speed things up quickly 
                            ⮑ for this run the algo as is with 2016 starting param, time it and write it down 
                            ⮑ then use a generator impl with the same starting param and time it 
                                ⮑ see if using a generator does speed up the process 
                                    ⮑ if it does this is a HUGE milestone that you would want to highlight on your resume 
            '''
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