from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.results import Material, Results
from nomad.parsing.parser import MatchingParser

from amstools.pipeline import Pipeline

from nomad.datamodel.metainfo.workflow import Workflow, Task, Link
from nomad.metainfo import SubSection, Section
from nomad.datamodel.datamodel import EntryArchive, EntryMetadata
from ruamel.yaml import YAML, dump

import os

configuration = config.get_plugin_entry_point(
    'nomad_workflow_parser.parsers:ams_workflow_parser'
)

import pdb
class AMSWorkflowParser(MatchingParser):

    def parse(
        self,
        mainfile: str,
        logger: 'BoundLogger',
        #child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:

        pipeline = Pipeline.read_json(mainfile)
        pdb.set_trace()
        logger.info(f'main file: {mainfile}')
        
        #        logger.info('AMSWorkflowParser.parse', parameter=configuration.parameter)
#         archive.results = Results(material=Material(elements=['H', 'O']))

    def parse_single_point_calculation(
            self,
            input_archive: EntryArchive,
            logger: 'BoundLogger',
            ):


        section_root = os.path.join( '..','upload', 'archive', 'mainfile', os.path.basename(  input_archive.metadata.mainfile ))

        workflow_dict  ={'workflow2':
                         {
                             'name': 'SinglePointCalc',
                             'inputs':[{'name':  'Input Structure' , 'section': section_root+'#run/0/system/-1' }],
                             'outputs':[{'name' : 'Output Calculation','section': section_root+'#run/0/calculation/-1'}],
                             'tasks': [{
                                 'm_def' : 'nomad.datamodel.metainfo.workflow.TaskReference',
                                 'task' :section_root+'#workflow2',
                                 'name' : 'Structure optimization',
                                 'inputs': [ {'name' : 'Input Structure','section' : section_root+ '#run/0/system/-1' }],
                                 'outputs': [{ 'name' : 'Output Calculation','section' : section_root+'#run/0/calculation/-1'}]
                                 }]
                             }
                         }


        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.explicit_start = True
        output_dir = os.path.dirname ( input_archive.metadata.mainfile )
        output_yaml = os.path.join(output_dir, 'test_single_point_workflow.archive.yaml')
        with open(output_yaml, 'w') as f:
            yaml.dump(workflow_dict, stream=f)
        return workflow_dict

    def create_workflow_from_scratch(
            self,
            input_archive: EntryArchive,
            logger: 'BoundLogger'
            ):

        data_root = os.path.dirname(input_archive.metadata.mainfile)
        data_file = os.path.join(data_root, 'scratch_workflow.archive.yaml')

        root_url = os.path.join('../upload/archive/mainfile', os.path.basename(input_archive.metadata.mainfile))

        workflow_archive = EntryArchive()

        workflow_object = Workflow()
        
        
        workflow_object.m_add_sub_section(
                Workflow.inputs,
                Link(name='Input Structure', section=input_archive.run[-1].system[-1], m_context=root_url)
                #                Link(name='Input Structure', section=input_archive.run[-1].system[-1])
                )

        workflow_object.m_add_sub_section(
                Workflow.outputs,
                Link(name='Calculation Output', section=input_archive.run[-1].calculation[-1], m_context=root_url)
                )

        workflow_archive.m_add_sub_section(
                EntryArchive.workflow2, 
                workflow_object
                )

        archive_dict = workflow_archive.m_to_dict()

        yaml = YAML()
        yaml.preserve_quotes = True
        with open(data_file, 'w') as f:
            yaml.dump(archive_dict, f)

        return data_file



