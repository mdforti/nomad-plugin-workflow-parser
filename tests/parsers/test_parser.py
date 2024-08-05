import logging

from nomad.datamodel import EntryArchive
from nomad_workflow_parser.parsers.ams_workflow_parser import AMSWorkflowParser
from nomad.client import parse


def test_parse_file():
    parser = AMSWorkflowParser()
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging.getLogger())

    assert archive.results.material.elements == ['H', 'O']


def test_parse_outcar():
    anoutcar = 'tests/data/R-AAAAAAAABBB/relax/xc=PBE-PAW.E=450.dk=0.020/OUTCAR'
    archives = parse(anoutcar, parser_name='parsers/vasp')
    assert(len(archives) > 0)
