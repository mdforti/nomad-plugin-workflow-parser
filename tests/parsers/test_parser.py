import logging
import sys

from nomad.datamodel import EntryArchive
from nomad_workflow_parser.parsers.ams_workflow_parser import AMSWorkflowParser

from nomad.parsing.parsers import run_parser, parser_dict

import json

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
    anoutcar = 'tests/data/R-AAAAAAAABBB/volume_relaxed/xc=PBE-PAW.E=450.dk=0.020/OUTCAR.1.025'
    parser = parser_dict['parsers/vasp']
    archives = run_parser(mainfile_path=anoutcar, parser=parser, logger=logger)

    assert len(archives) > 0

    for i, archive in enumerate(archives):
        archive_json = archive.m_to_dict()
        with open(f'test{i}.json', 'w') as f:
            json.dump(archive_json, f,  indent=4)
        for section  in archive:
            logger.info(section)


def test_parse_pipeline():
    apipeline = 'tests/data/Fe2Cr5FeCr3FeCrFe10CrFeCr2FeCr2/pipeline.json'
    parser = AMSWorkflowParser()
    archives = parser.parse(mainfile=apipeline, logger=logger)
