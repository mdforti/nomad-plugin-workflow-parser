import logging
import sys

from nomad.datamodel import EntryArchive
from nomad_workflow_parser.parsers.ams_workflow_parser import AMSWorkflowParser

from nomad.parsing.parsers import run_parser, parser_dict

import json

import os

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, filename='testing.log')
stdoutStream = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutStream)


def no_test_parse_file():
    parser = AMSWorkflowParser()
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging.getLogger())
    assert archive.results.material.elements == ['H', 'O']


def skip_test_parse_outcar():
    anoutcar = 'tests/data/R-AAAAAAAABBB/volume_relaxed/xc=PBE-PAW.E=450.dk=0.020/OUTCAR.1.000'
    parser = parser_dict['parsers/vasp']
    archives = run_parser(mainfile_path=anoutcar, parser=parser, logger=logger)

    assert len(archives) > 0

    for i, archive in enumerate(archives):
        archive_json = archive.m_to_dict()
        with open(f'test{i}.json', 'w') as f:
            json.dump(archive_json, f,  indent=4)
        for section  in archive:
            logger.info(section)


def skip_test_parse_pipeline():
    apipeline = 'tests/data/Fe2Cr5FeCr3FeCrFe10CrFeCr2FeCr2/pipeline.json'
    parser = AMSWorkflowParser()
    archives = parser.parse(mainfile=apipeline, logger=logger)

def skip_test_singple_point_workflow():
    anoutcar = 'tests/data/R-AAAAAAAABBB/volume_relaxed/xc=PBE-PAW.E=450.dk=0.020/OUTCAR.1.000'
    parser = AMSWorkflowParser() # parser_dict['parsers/vasp']
    archive = run_parser(anoutcar, parser = parser_dict['parsers/vasp'], logger=logger)
    output_file = parser.parse_single_point_calculation(archive, logger)
    logger.info(output_file)
    assert(os.path.exists(output_file))

def test_create_workflow():
    anoutcar = 'tests/data/R-AAAAAAAABBB/volume_relaxed/xc=PBE-PAW.E=450.dk=0.020/OUTCAR.1.000'
    parser = AMSWorkflowParser() # parser_dict['parsers/vasp']
    archive = run_parser(anoutcar, parser = parser_dict['parsers/vasp'], logger=logger)
    output_file = parser.create_workflow_from_scratch(archive[0], logger)
    logger.info(output_file)
    assert(os.path.exists(output_file))
