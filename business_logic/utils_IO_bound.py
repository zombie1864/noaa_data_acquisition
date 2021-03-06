import os 
import ftplib
import pathlib 
import logging 
from business_logic.utils_data_manipulation import weather_stations_by
from business_logic.fileio import CsvReader
from business_logic.schemas import StationMetadataModel

logger = logging.getLogger(__name__)


def fetch_noaa_ftp_data(start:int, end:int, dir_path:pathlib.Path, csv_filepath:pathlib.Path) -> None: 
    ''' access noaa's ftp server and write to memory all years for each station from start to end  
        Args:
            start: the starting year for which to look in noaa's database 
            end: the ending year for which to terminate search 
            dir_path: the dir path to which write the `.gz` files names to 
            csv_filepath: csv file for which weather stations are being pulled from to cross reference with noaa server 
        Returns:
            None 
    '''
    list_of_inst_models = CsvReader().read(csv_filepath,StationMetadataModel) 
    list_of_weather_stations = weather_stations_by(start, end, list_of_inst_models)
    for year in range(start, end): 
        for weather_station in list_of_weather_stations:
            ftp_server = 'ftp.ncdc.noaa.gov' 
            ftp_dir = f'pub/data/noaa/{year}'
            file_name = f'{weather_station}-{year}.gz'
            file_path = dir_path / file_name
            if file_path.is_file(): 
                continue 
            _fetch_files(ftp_server, ftp_dir, file_name, dir_path)



def make_raw_dir(dir_path:pathlib.Path) -> None: 
    ''' creates `raw/` under `project_data` if `project_data/raw/` does not exist, then changes working dir to `raw`
        Args:
            dir_path: the dir path that needs to be created and switched to 
        Returns:
            None 
    '''
    if not dir_path.exists():
        dir_path.mkdir()
    os.chdir(dir_path)


def _fetch_files(ftp_server:str, ftp_dir:str, file_name:str, dir_path:pathlib.Path) -> None:
    ''' logs into noaa's ftp server and downloads to memory `.gz` files for a given year, for a given file_name
        Args:
            ftp_server: string of ftp server 
            ftp_dir: dir_path containing `.gz` files 
            file_name: weather station by `.gz` file 
            dir_path: the dir path to which the files will be saved to 
        Returns:
            None
    '''
    with ftplib.FTP(ftp_server, timeout=3.0) as ftp:
        ftp.login()
        ftp.cwd(ftp_dir)
        make_raw_dir(dir_path)
        try:
            with open(file_name, 'wb') as fp:
                ftp.retrbinary(f'RETR {file_name}', fp.write)
                logger.info(f'writing file: {file_name}')
        except ftplib.error_perm:
                logger.error(f'{file_name} not found')
        ftp.quit()
