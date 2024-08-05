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
