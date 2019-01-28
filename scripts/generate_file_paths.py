#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from os.path import exists, join, dirname, realpath
import os
import sys

DEBUG = int(os.environ.get("DEBUG", logging.DEBUG))
EXPERIMENTS = {
  'ExperimentA_No01_2013_03_12_10min_actin_microtubules_vimentin_001.lsm': 50,
  'ExperimentA_No02_2013_03_22_10min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No04_2013_05_15_10min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No06_2013_06_26_10min_microtubules_vimentin_001.lsm': 120,
  'ExperimentA_No07_2012_06_17_1h_actin_microtubules_001.zvi': 300,
  'ExperimentA_No08_2012_06_17_1h_actin_microtubules_001.zvi': 300,
  'ExperimentA_No09_2012_08_06_1h_actin_microtubules_001.lsm': 63,
  'ExperimentA_No10_2012_08_07_1h_actin_microtubules_001.lsm': 81,
  'ExperimentA_No11_2013_03_12_20min_actin_microtubules_vimentin_001.lsm': 45,
  'ExperimentA_No12_2013_04_18_20min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No13_2013_04_18_20min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No14_2013_05_15_20min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No15_2013_05_15_20min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No16_2013_06_26_20min_actin_microtubules_001.lsm': 120,
  'ExperimentA_No17_2013_06_26_20min_microtubules_vimentin_001.lsm': 120,
  'ExperimentA_No18_2012_08_04_2h_actin_microtubules_001.lsm': 49,
  'ExperimentA_No19_2012_08_06_2h_actin_microtubules_001.lsm': 164,
  'ExperimentA_No20_2013_04_18_30min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No21_2013_04_18_30min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No22_2013_05_15_30min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No23_2013_05_15_30min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No24_2013_06_26_30min_actin_microtubules_001.lsm': 120,
  'ExperimentA_No25_2013_06_26_30min_microtubules_vimentin_001.lsm': 120,
  'ExperimentA_No26_2012_08_04_4h_actin_microtubules_001.lsm': 73,
  'ExperimentA_No27_2012_08_04_4h_actin_microtubules_001.lsm': 50,
  'ExperimentA_No28_2013_03_12_5min_actin_microtubules_vimentin_001.lsm': 50,
  'ExperimentA_No29_2013_04_18_5min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No30_2013_05_15_5min_actin_microtubules_001.lsm': 75,
  'ExperimentA_No31_2013_05_15_5min_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No32_2013_06_26_5min_actin_microtubules_001.lsm': 120,
  'ExperimentA_No33_2013_06_26_5min_microtubules_vimentin_001.lsm': 120,
  'ExperimentA_No34_2012_08_03_8h_actin_microtubules_001.lsm': 50,
  'ExperimentA_No35_2012_08_04_8h_actin_microtubules_001.lsm': 50,
  'ExperimentA_No36_2013_05_28_8h_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No37_2013_05_28_8h_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No38_2013_05_28_8h_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No39_2013_03_12_Kontrolle_actin_microtubules_vimentin_001.lsm':
  50,
  'ExperimentA_No40_2013_04_18_Kontrolle_actin_microtubules_001.lsm': 75,
  'ExperimentA_No41_2013_04_18_Kontrolle_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No42_2013_05_15_Kontrolle_actin_microtubules_001.lsm': 75,
  'ExperimentA_No43_2013_05_15_Kontrolle_microtubules_vimentin_001.lsm': 75,
  'ExperimentA_No44_2013_06_26_Kontrolle_actin_microtubules_001.lsm': 120,
  'ExperimentA_No45_2013_06_26_Kontrolle_microtubules_vimentin_001.lsm': 120,
  'ExperimentB_No01_DMSO_23_control__001.lsm': 2,
  'ExperimentB_No01_DMSO_23_control__003.czi': 9,
  'ExperimentB_No01_DMSO_23_control__012.lsm': 3,
  'ExperimentB_No01_DMSO_23_control__015.czi': 7,
  'ExperimentB_No01_DMSO_23_control__022.lsm': 1,
  'ExperimentB_No01_DMSO_23_control__023.czi': 10,
  'ExperimentB_No01_DMSO_23_control__033.lsm': 6,
  'ExperimentB_No01_DMSO_23_control__039.czi': 1,
  'ExperimentB_No02_DMSO_22_control__001.czi': 30,
  'ExperimentB_No03_Noc_21_control__001.czi': 28,
  'ExperimentB_No04_Noc_22_control__001.czi': 31,
  'ExperimentB_No05_DMSO_11_10min__001.czi': 22,
  'ExperimentB_No06_DMSO_12_10min__001.czi': 34,
  'ExperimentB_No07_Noc_10_10min__001.czi': 35,
  'ExperimentB_No08_Noc_09_10min__001.czi': 34,
  'ExperimentB_No09_DMSO_20_1h__001.czi': 40,
  'ExperimentB_No10_DMSO_21_1h__001.czi': 33,
  'ExperimentB_No11_Noc_18_1h__001.czi': 30,
  'ExperimentB_No12_Noc_19_1h__001.czi': 56,
  "ExperimentB_No13_DMSO_07_1h_40µMol__001.czi": 31,
  'ExperimentB_No14_DMSO_08_1h_40µMol__001.czi': 29,
  'ExperimentB_No15_Noc_04_1h_40µMol__001.czi': 27,
  'ExperimentB_No16_Noc_06_1h_40µMol__001.czi': 23,
  'ExperimentB_No17_DMSO_05_20min__001.czi': 30,
  'ExperimentB_No18_DMSO_C2_20min__001.czi': 30,
  'ExperimentB_No19_Noc_C1_20min__001.czi': 32,
  'ExperimentB_No20_Noc_23_20min__001.czi': 30,
  'ExperimentB_No21_DMSO_16_30min__001.czi': 33,
  'ExperimentB_No22_DMSO_17_30min__001.czi': 30,
  'ExperimentB_No23_Noc_14_30min__001.lsm': 2,
  'ExperimentB_No24_Noc_15_30min__001.czi': 43,
  'ExperimentB_No25_DMSO_26_5min__001.czi': 37,
  'ExperimentB_No26_DMSO_27_5min__001.czi': 31,
  'ExperimentB_No27_Noc_25_5min__001.czi': 34
}

BASE_DIRECTORY = "/uod/idr/filesets/idr0050-springer-cytoskeletalsystems"
FTP_DIRECTORY = "20181106-ftp"

# Patterns for detecting strain duration from filename
H_PATTERN = re.compile(r'.*_(\d)h_.*')
MIN_PATTERN = re.compile(r'.*_(\d+)min_.*')

IMAGE_FILEPATHS = join(
    dirname(dirname(realpath(sys.argv[0]))),
    "experimentA", "idr0050-experimentA-filePaths.tsv")


def get_strain_duration(imagename):
    """" Detect control or strain time"""
    if "Kontrolle" in imagename or "control" in imagename:
        return "Control"
    elif H_PATTERN.match(imagename):
        m = H_PATTERN.match(imagename)
        return "%sh" % m.group(1)
    elif MIN_PATTERN.match(experiment):
        m = MIN_PATTERN.match(imagename)
        return "%smin" % m.group(1)
    else:
        raise Exception("Could not detect the strain duration")


def get_treatment(imagename):
    """" Detect image treament"""
    if "_DMSO_" in experiment:
        return "DMSO"
    elif "_Noc_" in experiment:
        return "Noc"
    else:
        return "Untreated"


logging.basicConfig(level=DEBUG, format='%(message)s')

# Check paths
if not exists(BASE_DIRECTORY):
    raise Exception("Cannot find %s" % BASE_DIRECTORY)

filepaths = {}
for experiment, image_number in sorted(EXPERIMENTS.iteritems()):
    logging.info("Checking %s" % experiment[0:16])

    # Generate dataset name
    datasetname = "%s %s" % (
        get_treatment(experiment), get_strain_duration(experiment))

    # Detect presence of actin and vimentin
    if "actin" in experiment:
        actin = True
    elif experiment.startswith("ExperimentB"):
        # All images in experimentB contain actin
        actin = True
    else:
        actin = False
    if actin:
        datasetname += " Actin"

    if "_vimentin_" in experiment:
        datasetname += " Vimentin"
    logging.info("Detected as dataset %s" % datasetname)

    # Check all files exist on disk
    if experiment.startswith("ExperimentA"):
        images_directory = join(
            BASE_DIRECTORY, FTP_DIRECTORY, 'experimentA',
            'ImagesOfExperimentA')
    elif experiment.startswith("ExperimentB"):
        images_directory = join(
            BASE_DIRECTORY, FTP_DIRECTORY, 'experimentB',
            'ImagesOfExperimentB')

    # Check existence of image files
    first_image = int(experiment[-6:-4])
    for i in range(first_image, image_number + first_image):
        image_filepath = join(
            images_directory, experiment[0:-7] + "%03d" % i +
            experiment[-4:])
        assert exists(image_filepath), image_filepath
        filepaths[image_filepath] = datasetname
    logging.info("Found %s images" % image_number)

with open(IMAGE_FILEPATHS, 'w') as f:
    for filepath, dataset in sorted(filepaths.iteritems()):
        f.write("Dataset:name:%s\t%s\n" % (dataset, filepath))
