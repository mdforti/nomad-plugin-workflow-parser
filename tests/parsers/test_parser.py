import logging
import sys

import unittest

from nomad.datamodel import EntryArchive, EntryMetadata
from nomad_workflow_parser.parsers.ams_workflow_parser import AMSWorkflowParser

from nomad.parsing.parsers import run_parser, parser_dict

import json

import os

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, filename='testing.log')
stdoutStream = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutStream)

class TestAMSPArser(unittest.TestCase):
    
    def setUp(self):
        self.anoutcar = 'tests/data/R-AAAAAAAABBB/volume_relaxed/xc=PBE-PAW.E=450.dk=0.020/OUTCAR.1.000'
        self.archives = run_parser(self.anoutcar, parser = parser_dict['parsers/vasp'], logger=logger)
        self.apipeline = 'tests/data/Fe2Cr5FeCr3FeCrFe10CrFeCr2FeCr2/pipeline.json'

    def no_test_parse_file(self):
        parser = AMSWorkflowParser()
        archive = EntryArchive()
        parser.parse('tests/data/example.out', archive, logging.getLogger())
        assert archive.results.material.elements == ['H', 'O']


    def skip_test_parse_outcar(self):

        assert len(self.archives) > 0

        for i, archive in enumerate(self.archives):
            archive_json = archive.m_to_dict()
            with open(f'test{i}.json', 'w') as f:
                json.dump(archive_json, f,  indent=4)
            for section  in archive:
                logger.info(section)


    def skip_test_parse_pipeline(self):
        parser = AMSWorkflowParser()
        archives = parser.parse(mainfile=apipeline, logger=logger)

    def skip_test_singple_point_workflow(self):
        parser = AMSWorkflowParser() # parser_dict['parsers/vasp']
        output_file = parser.parse_single_point_calculation(self.archives[0], logger)
        logger.info(output_file)
        assert(os.path.exists(output_file))

    def test_metadata(self):
        url = os.path.join('../upload/archive/',os.path.basename(self.archives[0].metadata.mainfile ))
        logger.info(f'url: {url}')
                           

    def test_create_workflow(self):
        parser = AMSWorkflowParser() # parser_dict['parsers/vasp']
        output_file = parser.create_workflow_from_scratch(self.archives[0], logger)
        logger.info(f'output file: {output_file}')
        assert(os.path.exists(output_file))


if __name__ == '__main__':
    unittest.main()
