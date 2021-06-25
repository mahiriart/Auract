import os

script_path = os.path.dirname(os.path.abspath(__file__))

second_file_dir = os.path.join(script_path, 'second_file')
data_dir = os.path.join(script_path, 'data')

micro_json_dir = os.path.join(second_file_dir, 'microreact')
geo_csv_ll_dir = os.path.join(second_file_dir, 'Geocoding/csv_generate')
auspice_config_dir = os.path.join(second_file_dir, 'auspice/config')
auspice_data_dir = os.path.join(second_file_dir, 'auspice/data')
auspice_refine_dir = os.path.join(second_file_dir, 'auspice/result')

resultDir = os.path.join(script_path, 'result')

result_Dir_micro = os.path.join(resultDir, 'microreact')
result_Dir_auspice = os.path.join(resultDir, 'auspice')
