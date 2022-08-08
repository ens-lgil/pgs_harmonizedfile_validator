import sys
import numpy as np
from pandas_schema import Column
from pandas_schema.validation import MatchesPatternValidation, InListValidation, CanConvertValidation, LeadingWhitespaceValidation, TrailingWhitespaceValidation, CustomElementValidation
from .helpers import InInclusiveRangeValidation

#from validate.common_constants import *
sys_paths = ['../']
sys.path.extend(sys_paths)
from common_constants import *


STD_COLS_VAR_POS = (HM_SOURCE_DSET, HM_CHR_DSET, HM_BP_DSET)

STD_COLS_VAR_FINAL = (EFFECT_DSET, EFFECT_WEIGHT_DSET, HM_CODE_DSET, HM_INFO_DSET)

SNP_COLS_VAR_POS = (SNP_DSET, HM_SNP_DSET)
CHR_COLS_VAR_POS = (CHR_DSET,)

SNP_COLS_VAR_FINAL = (VARIANT_DSET,)
CHR_COLS_VAR_FINAL = (CHR_DSET, HM_CHR_DSET)


VALID_COLS_POS = (HM_SOURCE_DSET, HM_SNP_DSET, HM_CHR_DSET, HM_BP_DSET, HM_OTH_DSET, HM_MATCH_CHR_DSET, HM_MATCH_BP_DSET)

VALID_COLS_FINAL = (SNP_DSET, CHR_DSET, BP_DSET, EFFECT_DSET, OTH_DSET, EFFECT_WEIGHT_DSET, LOCUS_DSET, HM_CODE_DSET, HM_SNP_DSET, HM_CHR_DSET, HM_BP_DSET, HM_OTH_DSET, HM_MATCH_CHR_DSET, HM_MATCH_BP_DSET)

VALID_CHROMOSOMES = ['1', '2', '3', '4', '5', '6', '7', '8',
                     '9', '10', '11', '12', '13', '14', '15', '16',
                     '17', '18', '19', '20', '21', '22',
                     'X', 'x', 'Y', 'y', 'XY', 'xy', 'MT', 'Mt', 'mt']

VALID_CODES = ['5','4','3','1','0','-1','-4','-5']

VALID_SOURCES = ['ENSEMBL','Author-reported']

BUILD_LIST = ['GRCh37','GRCh38']

VALID_FILE_EXTENSIONS = [".txt", ".txt.gz"]

error_msg = 'this column cannot be null/empty' 
null_validation = CustomElementValidation(lambda d: d is not np.nan and d != '', error_msg)


GENERIC_VALIDATORS = {
    CHR_DSET: Column(CHR_DSET, [InListValidation(VALID_CHROMOSOMES)], allow_empty=True),
    BP_DSET: Column(BP_DSET, [CanConvertValidation(DSET_TYPES[BP_DSET]), InInclusiveRangeValidation(1, 999999999)], allow_empty=True),
    EFFECT_WEIGHT_DSET: Column(EFFECT_WEIGHT_DSET, [CanConvertValidation(DSET_TYPES[EFFECT_WEIGHT_DSET]), null_validation], allow_empty=False),
    EFFECT_DSET: Column(EFFECT_DSET, [MatchesPatternValidation(r'^[ACTGN\-]+$')], allow_empty=False),
    OTH_DSET: Column(OTH_DSET, [MatchesPatternValidation(r'^[ACTGN\-]+$')], allow_empty=True),
    LOCUS_DSET: Column(LOCUS_DSET, [CanConvertValidation(DSET_TYPES[LOCUS_DSET]), LeadingWhitespaceValidation(), TrailingWhitespaceValidation(), null_validation], allow_empty=True)
}

POS_VALIDATORS = {}
POS_VALIDATORS[HR_DSET] = Column(HR_DSET, [CanConvertValidation(DSET_TYPES[HR_DSET]), null_validation], allow_empty=True)
POS_VALIDATORS[HM_SOURCE_DSET] = Column(HM_SOURCE_DSET, [CanConvertValidation(DSET_TYPES[HM_SOURCE_DSET]), LeadingWhitespaceValidation(), TrailingWhitespaceValidation(), null_validation], allow_empty=False)
POS_VALIDATORS[HM_SNP_DSET] = Column(HM_SNP_DSET, [CanConvertValidation(DSET_TYPES[HM_SNP_DSET]), MatchesPatternValidation(r'^(rs|HLA\-\w+\*)[0-9]+$')], allow_empty=True)
POS_VALIDATORS[HM_CHR_DSET] = Column(HM_CHR_DSET, [InListValidation(VALID_CHROMOSOMES)], allow_empty=True)
POS_VALIDATORS[HM_BP_DSET] = Column(HM_BP_DSET, [CanConvertValidation(DSET_TYPES[HM_BP_DSET]), InInclusiveRangeValidation(1, 999999999)], allow_empty=True)
POS_VALIDATORS[HM_OTH_DSET] =  Column(HM_OTH_DSET, [MatchesPatternValidation(r'^[ACTGN\-\/]+$')], allow_empty=True)
POS_VALIDATORS[HM_MATCH_CHR_DSET] = Column(HM_MATCH_CHR_DSET, [InListValidation(['True', 'False'])], allow_empty=True)
POS_VALIDATORS[HM_MATCH_BP_DSET] = Column(HM_MATCH_BP_DSET, [InListValidation(['True', 'False'])], allow_empty=True)

FINAL_VALIDATORS = {k:v for k,v in GENERIC_VALIDATORS.items()}
FINAL_VALIDATORS[EFFECT_DSET] = Column(EFFECT_DSET, [MatchesPatternValidation(r'^[ACTGN\-]+$')], allow_empty=True)
FINAL_VALIDATORS[OTH_DSET] = Column(OTH_DSET, [MatchesPatternValidation(r'^[ACTGN\-\.]+$')], allow_empty=True)
FINAL_VALIDATORS[VARIANT_DSET] = Column(VARIANT_DSET, [CanConvertValidation(DSET_TYPES[VARIANT_DSET]), MatchesPatternValidation(r'^((rs|HLA\-\w+\*)[0-9]+|\.)$')], allow_empty=True)
FINAL_VALIDATORS[HM_CODE_DSET] = Column(HM_CODE_DSET, [InListValidation(VALID_CODES), null_validation], allow_empty=True)
FINAL_VALIDATORS[HM_INFO_DSET] = Column(HM_INFO_DSET, [CanConvertValidation(DSET_TYPES[HM_INFO_DSET]), null_validation], allow_empty=True)


#### Metadata entries ####

HM_META_GENERIC = [
    '###PGS CATALOG SCORING FILE',
    '#format_version',
    '##POLYGENIC SCORE',
    '#pgs_id',
    '#pgs_name',
    '#trait_reported',
    '#trait_mapped',
    '#trait_efo',
    '#genome_build',
    '#variants_number',
    '#weight_type',
    '##SOURCE INFORMATION',
    '#pgp_id',
    '#citation',
    '##HARMONIZATION DETAILS'
]

HM_META_POS = [ x for x in HM_META_GENERIC ]
HM_META_POS.append('#HmPOS_build')
HM_META_POS.append('#HmPOS_date')
HM_META_POS.append('HmPOS_match_chr')
HM_META_POS.append('#HmPOS_match_pos')

HM_META_FINAL = [ x for x in HM_META_GENERIC ]
HM_META_FINAL.append('#Hm_file_version')
HM_META_FINAL.append('#Hm_genome_build')
HM_META_FINAL.append('#Hm_reference_source')
HM_META_FINAL.append('#Hm_creation_date')
HM_META_FINAL.append('#Hm_variants_number_matched')
HM_META_FINAL.append('#Hm_variants_number_unmapped')
