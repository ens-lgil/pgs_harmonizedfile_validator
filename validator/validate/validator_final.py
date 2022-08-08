import sys
import os
import re
import pandas as pd
from pandas_schema import Schema
#from validator.schema import *
from .schema import *
from .validator_base import *

"""
PGS Catalog Harmonized file validator
- using pandas_schema https://github.com/TMiguelT/PandasSchema
"""

class ValidatorFinal(ValidatorBase):
    ''' Validator for the final Harmonized file format, which is an extension of the HmVCF file format. '''

    def __init__(self, file, score_dir=None, logfile="VALIDATE.log", error_limit=0):
        super().__init__(file, score_dir, logfile, error_limit)
        self.meta_format = HM_META_FINAL
        self.validators = FINAL_VALIDATORS
        self.valid_cols = VALID_COLS_FINAL


    def extract_specific_metadata(self,line):
        ''' Extract some of the metadata. '''
        match_variants_number = re.search(r'#variants_number=(\d+)', line)
        if match_variants_number:
            self.variants_number = int(match_variants_number.group(1))
        match_hm_variants_number = re.search(r'#Hm_variants_number_matched=(\d+)', line)
        if match_hm_variants_number:
            self.hmvcf_n_matched = int(match_hm_variants_number.group(1))
        unmapped_hm_variants_number = re.search(r'#Hm_variants_number_unmapped=(\d+)', line)
        if unmapped_hm_variants_number:
            self.hmvcf_n_unmapped = int(unmapped_hm_variants_number.group(1))
                    

    def validate_line_content(self,cols_content,var_line_number):
        ''' Populate the abstract method from ValidatorBase, to check some data in esch row. '''
        # Check lines
        line_dict = dict(zip(self.header, cols_content))
        error_cols = []
        int_hm_code = int(line_dict['hm_code'])
        if int_hm_code == -1 or int_hm_code == -5:
            for key in ['chr_name','chr_position']:
                if line_dict[key] != '':
                    error_cols.append(key)
            if line_dict['variant_id'] != '.':
                self.logger.error(f"- Variant line {var_line_number} | The variant is failing the harmonization: the column variant_id should have the value '.'")
            if error_cols:
                self.logger.error(f"- Variant line {var_line_number} | The variant is failing the harmonization: the column(s) {', '.join(error_cols)} should be empty.")
        else:
            if line_dict['effect_allele'] == '':
                self.logger.error(f"- Variant line {var_line_number} | The variant is failing the harmonization: the column effect_allele should not be empty")


    def validate_filename(self):
        ''' Validate the file name structure. '''
        self.validate_file_extension()
        pgs_id, build, version = None, None, None
        filename = self.file.split('/')[-1].split('.')[0]
        filename_parts = filename.split('_')
        if len(filename_parts) != 3:
            self.logger.error("Filename: {} should follow the pattern <pgs_id>_h<build>_v<version>.txt.gz [build=XX, e.g. 37]".format(filename))
            return False
        else:
            pgs_id, build, version = filename_parts
            build = f'GRC{build}'
        self.file_pgs_id = pgs_id
        self.file_genomebuild = build
        if not self.check_build_is_legit(build):
            self.logger.error("Build: {} is not an accepted build value".format(build))
            return False
        elif not re.match("^v\d+$", version):
            self.logger.error("Version: {} should follow the patten v<numeric_value> (e.g. v1)".format(version))
            return False
        self.logger.info("Filename looks good!")
        return True


    def validate_headers(self):
        ''' Validate the list of column names. '''
        # Check if it has at least a "SNP" column or a "chromosome" column
        self.setup_field_validation()
        required_is_subset = set(STD_COLS_VAR_FINAL).issubset(self.header)
        if not required_is_subset:
            self.logger.error("Required headers: {} are not in the file header: {}".format(STD_COLS_VAR_FINAL, self.header))
       
        # Check if it has at least a "SNP" column or a "chromosome" column
        required_pos = set(SNP_COLS_VAR_FINAL).issubset(self.header)
        if not required_pos:
            # check if everything but snp:
            required_pos = set(CHR_COLS_VAR_FINAL).issubset(self.header)
            if not required_pos:
                self.logger.error("One of the following required header is missing: '{}' and/or '{}' are not in the file header: {}".format(SNP_COLS_VAR_FINAL, CHR_COLS_VAR_FINAL, self.header))
                required_is_subset = required_pos
        
        return required_is_subset



def run_validator(file,score_dir,logfile):

    validator = ValidatorFinal(file=file, score_dir=score_dir, logfile=logfile)

    if not file or not logfile:
        validator.info("Missing file and/or logfile")
        validator.info("Exiting before any further checks")
        sys.exit()
    if not os.path.exists(file):
        validator.info("Error: the file '"+file+"' can't be found")
        validator.info("Exiting before any further checks")
        sys.exit()

    is_ok_to_run_validation = 1
    validator.logger.info("Validating file extension...")
    if not validator.validate_file_extension():
        validator.logger.info("Invalid file extension: {}".format(file))
        validator.logger.info("Exiting before any further checks")
        is_ok_to_run_validation = 0

    if is_ok_to_run_validation:
        validator.logger.info("Comparing filename with metadata...")
        if not validator.compare_with_filename():
            validator.logger.info("Discrepancies between filename information and metadata: {}".format(file))
            is_ok_to_run_validation = 0

    if is_ok_to_run_validation:
        validator.logger.info("Validating filename...")
        if not validator.validate_filename():
            validator.logger.info("Invalid filename: {}".format(file))
            is_ok_to_run_validation = 0

    if is_ok_to_run_validation:
        validator.logger.info("Validating headers...")
        if not validator.validate_headers():
            validator.logger.info("Invalid headers...exiting before any further checks")
            is_ok_to_run_validation = 0

    if is_ok_to_run_validation:
        validator.logger.info("Validating data...")
        validator.validate_data()

    # Close log handler
    validator.logger.removeHandler(validator.handler)
    validator.handler.close()