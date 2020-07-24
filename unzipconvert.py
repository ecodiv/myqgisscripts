"""
Unzipconvert 
Name : Unzip_and_convert_rasters
Group : File handling
With QGIS : 31401
"""

from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterString
import processing
import os
import zipfile
import tempfile
import pathlib
import ntpath

class unzipconvert(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            'INPUT',
            'INPUT', 
            optional=True, 
            behavior=QgsProcessingParameterFile.File, 
            fileFilter='All files (*.*)',
            defaultValue=None))
        self.addParameter(QgsProcessingParameterFile(
            'OUTPUT',
            'OutputFolder', 
            optional=True, 
            behavior=QgsProcessingParameterFile.Folder, 
            fileFilter='All files (*.*)',
            defaultValue=None))
        self.addParameter(QgsProcessingParameterString(
            'TYPE',
            'raster file type',
            multiLine=False,
            defaultValue='.tif'))

    def processAlgorithm(self, parameters, context, model_feedback):
        """
        The actual data processing
        """
        
        # Use a multi-step feedback, so that individual child algorithm
        # progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Output folder
        out_dir = parameters['OUTPUT']
        # Input zip file
        yzf = parameters['INPUT']
        # Temporary download folder
        temp_dir = tempfile.mkdtemp()
        # Placeholder for file names
        myfiles = []
        
        with zipfile.ZipFile(yzf) as zf:     
            # Get list with file names in zipfile
            files = zf.namelist() 
            # Get list with all raster layers in zip file (ascii and tif rasters)
            lrf = ('.asc', '.tif', '.bil', '.dwg', '.hdr')
            filesasc = [i for i in files if i.endswith(lrf)] 
            # Extract the raster layers to the user defined folder
            for asciifile in filesasc:
                file_path = os.path.join(temp_dir, asciifile)
                myfiles.append(file_path)
                f = open(file_path, 'wb')
                f.write(zf.read(asciifile))
                f.close()

        outputfiles = []
        kext = parameters['TYPE']
        for rasterfile in myfiles:
            # If other than geotif, convert raster to tif
            if pathlib.Path(rasterfile).suffix != kext:
                # Replace suffix with tif and temp folder path for path output folder
                tmpfilename = pathlib.Path(rasterfile).with_suffix(kext)
                transfile = os.path.join(out_dir, ntpath.basename(tmpfilename))
                  # Translate (convert format)
                alg_params = {
                    'COPY_SUBDATASETS': False,
                    'DATA_TYPE': 0,
                    'EXTRA': '',
                    'INPUT': rasterfile,
                    'NODATA': None,
                    'OPTIONS': '',
                    'TARGET_CRS': None,
                    'OUTPUT': transfile
                }
                outputs['TranslateConvertFormat'] = processing.run(
                    'gdal:translate', 
                    alg_params, context=context, 
                    feedback=feedback,
                    is_child_algorithm=True)

            # Move downloaded file from temp folder to user defined folder
            else:
                transfile = os.path.join(out_dir, ntpath.basename(rasterfile))
                os.rename(rasterfile, transfile)
            outputfiles.append(transfile)
        results['The downloaded (and optionally converted) raster layer(s):'] = outputfiles
        return results

    def name(self):
        return 'unzipconvert'

    def displayName(self):
        return 'unzipconvert'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>Unzips zipped raster files and converts ascii raster layers to geotif files.</p>
<h2>Input parameters</h2>
<h3>InputFile</h3>
<p>The name and path of the zip file</p>
<h3>Raster file type</h3>
<p>The file type in which you want to save the raster file (indicated by the file extension).</p>
<h3>OutputFolder</h3>
<p>The folder where the unzipped (and converted) raster file(s) will be stored.</p>
<h2>Outputs</h2>
<h3>OutputFile</h3>
<p>The folder where the unzipped raster file(s) should be stored.</p>
<br><p align="right">Algorithm author: Paulo van Breugel <paulo at ecodiv dot earth></p><p align="right">Help author: Paulo van Breugel <paulo at ecodiv dot earth></p></body></html>"""

    def helpUrl(self):
        return 'https://ecodiv.earth/post/qgisscript'

    def createInstance(self):
        return unzipconvert()
