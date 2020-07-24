"""
Model exported as python.
Name : Unzip and convert
Group : My script
With QGIS : 31401
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterBoolean
import processing


class UnzipAndConvert(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('DownloadURL', 'Download URL', multiLine=False, defaultValue='http://geodata.rivm.nl/downloads/ank/ANK_084_20170314_gm_Bomenkaart_percentage.zip'))
        self.addParameter(QgsProcessingParameterFile('Outputfolder', 'Output folder', behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Download file
        alg_params = {
            'URL': parameters['DownloadURL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadFile'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # unzipconvert
        alg_params = {
            'INPUT': outputs['DownloadFile']['OUTPUT'],
            'OUTPUT': parameters['Outputfolder'],
            'TYPE': '.tif'
        }
        outputs['Unzipconvert'] = processing.run('script:unzipconvert', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Unzip and convert'

    def displayName(self):
        return 'Unzip and convert'

    def group(self):
        return 'My script'

    def groupId(self):
        return 'My script'

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>Workflow combining the download and unzipconvert functions</p>
<h2>Input parameters</h2>
<h3>Download URL</h3>
<p>The URL of the zip file</p>
<h3>Output folder</h3>
<p>The folder to which the resulting raster layer is to be saved</p>
<h3>Verbose logging</h3>
<p></p>
<br><p align="right">Algorithm author: Paulo van Breugel <paulo at ecodiv dot earth></p><p align="right">Help author: Paulo van Breugel <paulo at ecodiv dot earth></p></body></html>"""

    def helpUrl(self):
        return 'https://ecodiv.earth/qgisscript'

    def createInstance(self):
        return UnzipAndConvert()
