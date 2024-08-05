from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class AMSWorkflowParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_workflow_parser.parsers.ams_workflow_parser import AMSWorkflowParser

        return AMSWorkflowParser(**self.dict())


ams_workflow_parser = AMSWorkflowParserEntryPoint(
    name='AMSWorkflowParser',
    description='Parser defined using the new plugin mechanism.',
    mainfile_name_re='.*\.ams_workflow_parser',
)
