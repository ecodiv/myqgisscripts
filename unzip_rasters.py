"""
Unzip zipped raster files (tif and asc)
Name : Unzip_rasters
Group : File handling
With QGIS : 31401
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
import processing
import os
import zipfile

class Unzip(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('InputFile', 'InputFile', behavior=QgsProcessingParameterFile.File, fileFilter='All files (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('outputFile', 'OutputFolder', behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        temp_dir = parameters['outputFile']
        with zipfile.ZipFile(parameters['InputFile']) as zf:
            files = zf.namelist()
            filesasc = [i for i in files if i.endswith(('.asc', '.tif'))]
            for asciifile in filesasc:
                file_path = os.path.join(temp_dir, asciifile)
                f = open(file_path, 'wb')
                f.write(zf.read(asciifile))
                f.close()
        return {'OUTPUTFOLDER': parameters['outputFile'],
                'OUTPUTFILES': filesasc}
                
    def name(self):
        return 'unzip'

    def displayName(self):
        return 'unzip'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>Unzips zipped raster files (tif and asc)</p>
<h2>Input parameters</h2>
<h3>InputFile</h3>
<p>The name and path of the zip file</p>
<h3>OutputFolder</h3>
<p>The folder where the unzipped raster file(s) should be stored.</p>
<h2>Outputs</h2>
<h3>OutputFile</h3>
<p>The folder where the unzipped raster file(s) should be stored.</p>
<br><p align="right">Algorithm author: Paulo van Breugel <paulo at ecodiv dot earth></p><p align="right">Help author: Paulo van Breugel <paulo at ecodiv dot earth></p></body></html>"""

    def helpUrl(self):
        return 'https://ecodiv.earth/post/qgisscript'

    def createInstance(self):
        return Unzip()
