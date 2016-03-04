#dan mcgraw
import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
			import arcpy


			# Local variables:
			DEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\DEM"
			FilledDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\FilledDEM"
			AnalysisMask = "AnalysisMask"
			MaskRas = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\MaskRas"
			Output_drop_raster = ""
			DirDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\DirDEM"
			AccumDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\AccumDEM"
			MultipliedDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\MultipliedDEM"
			finalcalc = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\finalcalc"
			ReclassDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\ReclassDEM"
			Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Stream"

			# Set Geoprocessing environments
			arcpy.env.snapRaster = "DEM"

			# Process: Fill
			arcpy.gp.Fill_sa(DEM, FilledDEM, "")

			# Process: Polygon to Raster
			arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", MaskRas, "CELL_CENTER", "NONE", "40")

			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.cellSize
			arcpy.env.cellSize = "MAXOF"
			tempEnvironment1 = arcpy.env.mask
			arcpy.env.mask = MaskRas
			arcpy.gp.FlowDirection_sa(FilledDEM, DirDEM, "NORMAL", Output_drop_raster)
			arcpy.env.cellSize = tempEnvironment0
			arcpy.env.mask = tempEnvironment1

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(DirDEM, AccumDEM, "", "FLOAT")

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("Float(\"%AccumDEM%\")*(40*40)", MultipliedDEM)

			# Process: Raster Calculator (2)
			arcpy.gp.RasterCalculator_sa("\"%MultipliedDEM%\" / 43560", finalcalc)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(finalcalc, "Value", "0 883 NODATA;883 22532.3046875 1", ReclassDEM, "DATA")

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(ReclassDEM, DirDEM, Stream, "SIMPLIFY")


        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
        
			# Import arcpy module
			import arcpy


			# Local variables:
			ReclassDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\ReclassDEM"
			DirDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\DirDEM"
			Impervious = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Impervious"
			ImpervCalc = Impervious
			ImperviousRAS = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\ImperviousRAS"
			BlockStats = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\BlockStats"
			AggregateImperv = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\AggregateImperv"
			WeightedAccum = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\WeightedAccum"
			AccumDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\AccumDEM"
			Divide__2_ = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Divide"
			ReclassDivide = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\ReclassDivide"
			Multiplied = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Multiplied"
			Task3Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Task3Stream"

			# Process: Calculate Field
			arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")

			# Process: Feature to Raster
			arcpy.FeatureToRaster_conversion(ImpervCalc, "LENGTH", ImperviousRAS, "4")

			# Process: Block Statistics
			arcpy.gp.BlockStatistics_sa(ImperviousRAS, BlockStats, "Rectangle 10 10 CELL", "SUM", "DATA")

			# Process: Aggregate
			arcpy.gp.Aggregate_sa(BlockStats, AggregateImperv, "10", "MEAN", "EXPAND", "DATA")

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(DirDEM, WeightedAccum, AggregateImperv, "FLOAT")

			# Process: Divide
			arcpy.gp.Divide_sa(WeightedAccum, AccumDEM, Divide__2_)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(Divide__2_, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", ReclassDivide, "DATA")

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("(\"%ReclassDEM%\")*(\"%ReclassDivide%\")", Multiplied)

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(Multiplied, DirDEM, Task3Stream, "SIMPLIFY")



		except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
