# This script generates GeoTiff files based Corine land cover data
# Usage: python generateGeotiff.py berryName
# berryName is optional. If not provided all output layers are generated.
# Licensed under the MIT license

from osgeo import gdal, ogr, gdalconst
import sys

gdal.UseExceptions()
gdal.AllRegister()

# Paths for input and output. These may be adjusted as needed.
src_filename = "../../aineisto/Clc2012_FI20m.tif"
dstPath = "../../output"

berries = ["mustikka", "puolukka", "karpalo", "vadelma"]

if len(sys.argv) > 1:
	berries = [sys.argv[1]]

# WARNING: these values are not based on scientific research.
corineToBerryIndex = dict()
corineToBerryIndex["mustikka"] = dict()
corineToBerryIndex["mustikka"][24] = 70
corineToBerryIndex["mustikka"][25] = 80
corineToBerryIndex["mustikka"][27] = 50
corineToBerryIndex["mustikka"][28] = 60
corineToBerryIndex["puolukka"] = dict()
corineToBerryIndex["puolukka"][24] = 80
corineToBerryIndex["puolukka"][25] = 60
corineToBerryIndex["karpalo"] = dict()
corineToBerryIndex["karpalo"][40] = 50
corineToBerryIndex["karpalo"][42] = 80
corineToBerryIndex["vadelma"] = dict()
corineToBerryIndex["vadelma"][36] = 80
corineToBerryIndex["vadelma"][35] = 60

# Normalize values so that the highest value in output is always 100
normalizationFactor = 100.0 / 80.0

srcDs = gdal.Open(src_filename)
corineBand = srcDs.GetRasterBand(1)
xSize = corineBand.XSize
ySize = corineBand.YSize
print "Input raster size is ", xSize, ySize

for berry in berries:
	driver = srcDs.GetDriver()
	dstDs = driver.Create(dstPath + "/" + berry + ".tif", xSize, ySize, 1, gdal.GDT_UInt16, options = ['COMPRESS=LZW'])
	dstDs.SetGeoTransform(srcDs.GetGeoTransform())
	dstDs.SetProjection(srcDs.GetProjection())

	array = corineBand.ReadAsArray(0, 0, xSize, ySize)

	for x in range(0, xSize):
		indexes = corineToBerryIndex[berry]
		if x % 500 == 0:
			print `round(100.0 * x / xSize)` + " % of " + berry + " done"
		for y in range(0, ySize):
			origVal = array[y,x]
			if origVal in indexes:
				finalVal = int(indexes[origVal] * normalizationFactor)
			else:
				finalVal = 0
			array[y,x] = finalVal

	dstBand = dstDs.GetRasterBand(1)
	dstBand.WriteArray(array, 0, 0)

	# Once we're done, close properly the dataset
	dstBand = None
	dstDs = None

corineBand = None
srcDs = None
