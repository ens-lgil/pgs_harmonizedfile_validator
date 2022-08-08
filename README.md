# PGS Catalog Harmonized Scoring file validator
* Scripts to validate the data and the format of the PGS Catalog Harmonized Scoring


## Running script
```
usage: run_validator.py [-h] [-t HM_TYPE] [-f HM_FILE_NAME] [--hm_dir HM_DIR] [--score_dir SCORE_DIR] --log_dir LOG_DIR

optional arguments:
  -h, --help            show this help message and exit
  -t HM_TYPE            Type of validator: hm_pos or hm_final
  -f HM_FILE_NAME       The path to the harmonized scoring file to be validated (no need to use the [--dir] option)
  --hm_dir HM_DIR       The name of the directory containing the harmonized scoring files that need to processed (no need to use the [-f]
                        option
  --score_dir SCORE_DIR
                        The name of the directory containing the formatted scoring files to compare with harmonized scoring files
  --log_dir LOG_DIR     The name of the log directory where the log file(s) will be stored
```

### Examples
```
## Single file - HmPOS
python run_validator.py -t hm_pos -f <file_to_valid>.txt.gz --log_dir <log_directory> --score_dir <formatted_scoring_files_dir>

## Directory - HmPOS
python run_validator.py -t hm_pos  --hm_dir <harmonized_scoring_files_dir> --log_dir <log_directory> --score_dir <formatted_scoring_files_dir>


## Single file - HmFinal
python run_validator.py -t hm_final -f <file_to_valid>.txt.gz --log_dir <log_directory> --score_dir <formatted_scoring_files_dir>

## Directory - HmFinal
python run_validator.py -t hm_final  --hm_dir <harmonized_scoring_files_dir> --log_dir <log_directory> --score_dir <formatted_scoring_files_dir>
```

## Requirements (Python libraries)
  * cyvcf2
  * numpy
  * pandas
  * pandas-schema
  * pyliftover
  * requests
  * tqdm
