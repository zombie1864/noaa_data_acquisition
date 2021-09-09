import os
import pathlib
from business_logic.utils_file_IO import rm_0_byte_files_from, retreive_file_content_from, save_data_to_json_files_for
from business_logic.utils_data_manipulation import isd_data_parser, monthly_data_aggregation_for, rm_0_len_weather_station_data_for


this_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw' 
dir_path = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'monthly_weather_data'


''' this script only contains application logic '''
def main():
    rm_0_byte_files_from(raw_dir) 
    num_of_files, dir_content_dict = retreive_file_content_from(raw_dir)
    weather_station_matrix_data = isd_data_parser(num_of_files, dir_content_dict) 
    aggregated_weather_station_data = monthly_data_aggregation_for(weather_station_matrix_data)
    aggregated_weather_station_data = rm_0_len_weather_station_data_for(aggregated_weather_station_data)
    save_data_to_json_files_for(aggregated_weather_station_data, dir_path)


if __name__ == '__main__': 
    main() 