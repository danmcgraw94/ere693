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
			FilledDEM = arcpy.gp.Fill_sa(DEM, "")

			# Process: Polygon to Raster
			MaskRas = arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", "CELL_CENTER", "NONE", "40")

			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.cellSize
			arcpy.env.cellSize = "MAXOF"
			tempEnvironment1 = arcpy.env.mask
			arcpy.env.mask = MaskRas
			DirDEM = arcpy.gp.FlowDirection_sa(FilledDEM, "NORMAL", Output_drop_raster)
			arcpy.env.cellSize = tempEnvironment0
			arcpy.env.mask = tempEnvironment1

			# Process: Flow Accumulation
			AccumDEM = arcpy.gp.FlowAccumulation_sa(DirDEM, "", "FLOAT")

			# Process: Raster Calculator
			MultipliedDEM = arcpy.gp.RasterCalculator_sa("Float(\"%AccumDEM%\")*(40*40)")

			# Process: Raster Calculator (2)
			finalcalc = arcpy.gp.RasterCalculator_sa("\"%MultipliedDEM%\" / 43560")

			# Process: Reclassify
			ReclassDEM = arcpy.gp.Reclassify_sa(finalcalc, "Value", "0 883 NODATA;883 22532.3046875 1", "DATA")

			# Process: Stream to Feature
			Stream = arcpy.gp.StreamToFeature_sa(ReclassDEM, DirDEM, "SIMPLIFY")


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
			ImpervCalc = arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")


			# Process: Feature to Raster
			ImperviousRAS = arcpy.FeatureToRaster_conversion(ImpervCalc, "LENGTH", "4")

			# Process: Block Statistics
			BlockStats = arcpy.gp.BlockStatistics_sa(ImperviousRAS, "Rectangle 10 10 CELL", "SUM", "DATA")

			# Process: Aggregate
			AggregateImperv = arcpy.gp.Aggregate_sa(BlockStats, "10", "MEAN", "EXPAND", "DATA")

			# Process: Flow Accumulation
			WeightedAccum = arcpy.gp.FlowAccumulation_sa(DirDEM, AggregateImperv, "FLOAT")

			# Process: Divide
			Divide__2_ = arcpy.gp.Divide_sa(WeightedAccum, AccumDEM)

			# Process: Reclassify
			ReclassDivide = arcpy.gp.Reclassify_sa(Divide__2_, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", "DATA")

			# Process: Raster Calculator
			Multiplied = arcpy.gp.RasterCalculator_sa("(\"%ReclassDEM%\")*(\"%ReclassDivide%\")")

			# Process: Stream to Feature
			Task3Stream = arcpy.gp.StreamToFeature_sa(Multiplied, DirDEM, "SIMPLIFY")




			
			
			#task4
			# Local variables:
			finalcalc = "finalcalc"
			SQUAREMILES = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\SQUAREMILES"
			DivideFloat = "DivideFloat"
			IA = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\IA"
			F100 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F100"
			F100Q100 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F100Q100"
			Q100 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q100"
			DirDEM = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\DirDEM"
			Q100Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q100Stream"
			F50 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F50"
			F50Q50 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F50Q50"
			Q50 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q50"
			Q50Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q50Stream"
			F25 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F25"
			F25Q25 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F25Q25"
			Q25 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q25"
			Q25Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q25Stream"
			F10 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F10"
			F10Q10 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F10Q10"
			Q10 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q10"
			Q10Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q10Stream"
			F5 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F5"
			F5Q5 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F5Q5"
			Q5 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q5"
			Q5Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q5Stream"
			f2 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\f2"
			F2Q2 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\F2Q2"
			Q2 = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q2"
			Q2Stream = "E:\\Storage\\GIS-Based Modeling\\Lab06Data.gdb\\Q2Stream"
			Output_raster = ""

			# Process: Raster Calculator (14)
			SQUAREMILES = arcpy.gp.RasterCalculator_sa("\"%finalcalc%\"*0.0015625")

			# Process: Raster Calculator (7)
			IA = arcpy.gp.RasterCalculator_sa("Float((\"%DivideFloat%\")/100)")

			# Process: Raster Calculator (6)
			F100 = arcpy.gp.RasterCalculator_sa("719*((\"%SQUAREMILES%\") **.643)")

			# Process: Raster Calculator (9)
			F100Q100 = arcpy.gp.RasterCalculator_sa("(48*((\"%SQUAREMILES%\")**.392))*((\"%IA%\")**.358)*((\"%F100%\")**.312)")

			# Process: Reclassify (5)
			Q100 = arcpy.gp.Reclassify_sa(F100Q100, "Value", "0 40 NODATA;40 1686.8005523523098 1", "DATA")

			# Process: Stream to Feature
			Q100Stream = arcpy.gp.StreamToFeature_sa(Q100, DirDEM, "SIMPLIFY")

			# Process: Raster Calculator (5)
			F50 = arcpy.gp.RasterCalculator_sa("581*((\"%SQUAREMILES%\")**.65)")

			# Process: Raster Calculator (10)
			F50Q50 = arcpy.gp.RasterCalculator_sa("(37.4*((\"%SQUAREMILES%\")**.391))*((\"%IA%\")**.396)*((\"%F50%\")**.325)")

			# Process: Reclassify (6)
			Q50 = arcpy.gp.Reclassify_sa(F50Q50, "Value", "0 40 NODATA;40 1296.6974764473775 1", "DATA")

			# Process: Stream to Feature (2)
			Q50Stream = arcpy.gp.StreamToFeature_sa(Q50, DirDEM, "SIMPLIFY")

			# Process: Raster Calculator (4)
			F25 = arcpy.gp.RasterCalculator_sa("467*((\"%SQUAREMILES%\")**.655)")

			# Process: Raster Calculator (8)
			F25Q25 = arcpy.gp.RasterCalculator_sa("(28.5*((\"%SQUAREMILES%\")**.39))*((\"%IA%\")**.436)*((\"%F25%\")**.338)")

			# Process: Reclassify (4)
			Q25 = arcpy.gp.Reclassify_sa(F25Q25, "Value", "0 40 NODATA;40 962.81450417328051 1", "DATA")

			# Process: Stream to Feature (3)
			Q25Stream = arcpy.gp.StreamToFeature_sa(Q25, DirDEM, "SIMPLIFY")

			# Process: Raster Calculator (3)
			F10 = arcpy.gp.RasterCalculator_sa("334*((\"%SQUAREMILES%\")** .665)")

			# Process: Raster Calculator (13)
			F10Q10 = arcpy.gp.RasterCalculator_sa("(22.7*((\"%SQUAREMILES%\")**.436))*((\"%IA%\")**.515)*((\"%F10%\")**.289)")

			# Process: Reclassify (2)
			Q10 = arcpy.gp.Reclassify_sa(F10Q10, "Value", "0 40 NODATA;40 478.64123930725066 1", "DATA")

			# Process: Stream to Feature (4)
			Q10Stream = arcpy.gp.StreamToFeature_sa(Q10, DirDEM, "SIMPLIFY")

			# Process: Raster Calculator (2)
			F5 = arcpy.gp.RasterCalculator_sa("248*((\"%SQUAREMILES%\") ** .67)")

			# Process: Raster Calculator (12)
			F5Q5 = arcpy.gp.RasterCalculator_sa("(16.3*((\"%SQUAREMILES%\")**.489))*((\"%IA%\")**.572)*((\"%F5%\")**.286)")

			# Process: Reclassify (3)
			Q5 = arcpy.gp.Reclassify_sa(F5Q5, "Value", "0 40 NODATA;40 339.62484033724843 1", "DATA")

			# Process: Stream to Feature (5)
			Q5Stream = arcpy.gp.StreamToFeature_sa(Q5, DirDEM, "SIMPLIFY")

			# Process: Raster Calculator
			f2 = arcpy.gp.RasterCalculator_sa("144*((\"%SQUAREMILES%\")** .691)")

			# Process: Raster Calculator (11)
			F2Q2 = arcpy.gp.RasterCalculator_sa("(7.87*((\"%SQUAREMILES%\")**.539))*((\"%IA%\")**.686)*((\"%f2%\")**.29)")

			# Process: Reclassify (8)
			Q2 = arcpy.gp.Reclassify_sa(F2Q2, "Value", "0 40 NODATA;40 145.66437272620374 1", "DATA")

			# Process: Stream to Feature (6)
			Q2Stream = arcpy.gp.StreamToFeature_sa(Q2, DirDEM, "SIMPLIFY")







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
		
