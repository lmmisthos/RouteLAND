#	RouteLAND
#	Copyright (C) 2025 Loukas-Moysis Misthos (University of West Attica)

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Import arcpy, os and tempfile modules
import arcpy
import os
import tempfile

# Actual and Scratch Workspaaces 

# - Setting the actual working space / path
arcpy.env.workspace = "D:\\Moses\\IJGI_new_Python"
# - Defining a scratch workspace directory 
temp_dir = tempfile.mkdtemp()
# - Setting the scratch workspace environment to the temp directory
arcpy.env.scratchWorkspace = temp_dir

# Script arguments - Local variables: Input Parameters, Input/Output Data, Fields, Expressions & Codeblocks

# - Input Parameters (50 Meters, 5000 meters)
Buffer_distance = "6000 Meters"
Distance_line_to_points = "50 Meters"
Viewshed_outer_radius = "5000 Meters"
Observer_offset = "1 Meters"

# - Input Data
route = "\\Inputs\\Route_Eleochori_Lavrio.shp"
DEM_Attica_EGSA_tif = "\\Inputs\\DEM_Attica_EGSA.tif"
urban_atlas_clc_sea_Attica_clean = "\\Inputs\\urban_atlas_clc_sea_Attica_clean.shp"

# - Output Data
# -- Intermediate
route_dissolved = "\\Outputs\\route_dissolved.shp"
buf_route = "\\Outputs\\buf_route.shp"
DEM_Attica_EGSA_clip_tif = "\\Outputs\\DEM_Attica_EGSA_clip.tif"
slope_degrees_DEM_Attica_clip_tif = "\\Outputs\\slope_degrees_DEM_Attica_clip.tif"
aspect_degrees_DEM_Attica_clip_tif = "\\Outputs\\aspect_degrees_DEM_Attica_clip.tif"
urban_atlas_clc_sea_Attica_clean_clip = "\\Outputs\\urban_atlas_clc_sea_Attica_clean_clip.shp"
# -- Output
points_diss_50m = "\\Outputs\\points_diss_50m.shp"
points_50m = "\\Outputs\\points_50m.shp"
route_split_no_attrib = "\\Outputs\\route_split_no_attrib.shp"
route_split = "\\Outputs\\route_split.shp"
route_split_2 = route_split
route_split_3 = route_split_2
roads_direction = "\\Outputs\\roads_direction.shp"
points_start_direction = "\\Outputs\\points_start_direction.shp"
points_dir_elev = "\\Outputs\\points_dir_elev.shp"
points_dir_elev_maxspeed = "\\Outputs\\points_dir_elev_maxspeed.shp"
points_dir_elev_maxspeed_2 = points_dir_elev_maxspeed
points_dir_elev_maxspeed_3 = points_dir_elev_maxspeed_2
points_dir_elev_maxspeed_4 = points_dir_elev_maxspeed_3
points_dir_elev_maxspeed_5 = points_dir_elev_maxspeed_4
points_dir_elev_maxspeed_6 = points_dir_elev_maxspeed_5
points_dir_elev_maxspeed_7 = points_dir_elev_maxspeed_6
initial_route_viewpoints = "\\Outputs\\initial_route_viewpoints.shp"
sel_viewpoints_to_join = "\\Outputs\\sel_viewpoints_to_join.shp"
merged_viewpoints = "\\Outputs\\merged_viewpoints.shp"
merged_viewpoints_new = "\\Outputs\\merged_viewpoints_new.shp"
view_lines = "\\Outputs\\view_lines.shp"
view_lines_split = "\\Outputs\\view_lines_split.shp"
view_lines_attributes = "\\Outputs\\view_lines_attributes.shp"
view_lines_landscape = "\\Outputs\\view_lines_landscape.shp"
viewline_stats = "\\Outputs\\viewline_stats"
view_lines_landscape_copy = "\\Outputs\\view_lines_landscape_copy.shp"
view_lines_landscape_copy_1 = view_lines_landscape_copy
view_lines_landscape_copy_2 = view_lines_landscape_copy_1
view_lines_landscape_copy_3 = view_lines_landscape_copy_2
view_lines_landscape_copy_4 = view_lines_landscape_copy_3
view_lines_landscape_copy_5 = view_lines_landscape_copy_4
view_lines_landscape_final = "\\Outputs\\view_lines_landscape_final.shp"
view_lines_landscape_final_1 = view_lines_landscape_final
view_lines_landscape_final_2 = view_lines_landscape_final_1
view_lines_landscape_final_3 = view_lines_landscape_final_2

# - Fields
fieldName_01 = "road_str"
fieldName_02 = "hlf_angle"
fieldName_03 = "st_angle"
fieldName_04 = "end_angle"
fieldName_05 = "VPoint"
fieldName_06 = "VPElev"
fieldName_07 = "RoadID"
fieldName_08 = "VerAng"
fieldName_09 = "ActDist"
fieldName_10 = "RelVAng"
fieldName_11 = "ActHei"
fieldName_12 = "PerVerAng"
fieldName_13 = "RelHorA"
fieldName_14 = "RelHorAng"
fieldName_15 = "ActWid"
fieldName_16 = "PerHorAng"
fieldName_17 = "PerVSI"
fieldName_18 = "ConFID"
fieldName_19 = "LandComp"
fieldName_20 = "LandNam"
fieldName_21 = "MaxLand"
fieldName_22 = "DomLand"
fieldName_23 = "LandChar"

fieldLength = 100
fieldPrecision = 100
fieldScale = 100
fieldAlias = "AnyName"


# - Expressions & Codeblocks

exp_01 = "!FID!"

exp_02 = "convert(!maxspeed!)" 
code_block_02 = """
def convert(maxspeed):
    if (maxspeed == 0):
        return (60)
    elif (maxspeed > 0 and maxspeed <= 30):
        return (55)
    elif (maxspeed > 30 and maxspeed <= 65):
        return (50)         
    elif (maxspeed > 65 and maxspeed <= 80):
        return (30)
    elif (maxspeed > 80 and maxspeed <= 100):
        return (20)
    else:
        return (10)"""

exp_03 = "convert(!CompassA! - !hlf_angle!)"
code_block_03 = """
def convert(h_st_angle):
    if (h_st_angle < 0):
        return (360 - math.fabs(h_st_angle))
    elif (h_st_angle >= 0 and h_st_angle <= 360):
        return (h_st_angle)
    else:
        return (h_st_angle - 360)"""

exp_04 = "convert(!CompassA! +!hlf_angle!)"
code_block_04 = """
def convert(h_end_angle):
    if (h_end_angle < 0):
        return (360 - math.fabs(h_end_angle))
    elif (h_end_angle >= 0 and h_end_angle <= 360):
        return (h_end_angle)
    else:
        return (h_end_angle -360)"""

exp_05 = "fid_value"

exp_06 = "elev_value"

exp_07 = "math.degrees (math.atan ((!VPElev! - !ELEV! ) / !NEAR_DIST!))" 

exp_08 = "math.sqrt (math.pow (math.fabs(!VPElev! - !ELEV!) ,2 ) + math.pow(!NEAR_DIST!,2))" 

exp_09 = "math.fabs (math.fabs(!VerAng!) - !SLOPE!) " 

exp_10 = "math.sin(math.radians(!RelVAng!)) * 30" 

exp_11 = "math.degrees( 2*math.atan( !ActHei!/(2*!ActDist!)))" 

exp_12 = "convert(!ASPECT!,!NEAR_ANGLE!)" 
code_block_12 = """
def convert(ASPECT, NEAR_ANGLE):
    if (ASPECT  == -1):
        return (90)
    elif (0 <= ASPECT <= 180):
        return (math.fabs(math.fabs(NEAR_ANGLE) - ASPECT) )               
    else:
        return (math.fabs(math.fabs(NEAR_ANGLE) - (math.fabs(ASPECT-360)))) """

exp_13 = "convert(!RelHorA!)" 
code_block_13 = """
def convert(RelHorA):
    if (RelHorA <= 90):
        return (RelHorA)        
    else:
        return (RelHorA - 90)"""

exp_14 = "math.sin(math.radians(!RelHorAng!))*30"

exp_15 = "math.degrees(2*math.atan(!ActWid!/(2*!ActDist!)))" 

exp_16 = "!PerVerAng!*!PerHorAng!" 

exp_17 = "(!SUM_PERVSI!/!SUM_SUM_PE!)*100" 

exp_18 = "str(!FIRST_code!) + \":\" + \" \" + str( !LandComp! ) + \"%\"" 

exp_19 = "!osm_id! +  str(!FID!)"

exp_20 ="!MAX_MEAN_L!"

exp_21 = "convert ( !MEAN_LAST_!,!MaxLand! )" 
code_block_21 = """
def convert(MEAN_LAST_,MaxLand):
    if (MEAN_LAST_ == MaxLand):
        return (MEAN_LAST_)   
    else:
        return (9999)"""

exp_22 = "\"DomLand\" <> 9999"

exp_23 = "str( !FIRST_LAST! ) + \":\" + \" \" + str( !DomLand! ) + \"%\" "
      

# - Command for overwriting folders
arcpy.env.overwriteOutput = True

# - Command for preventing geoprocesses from adding outputs
arcpy.env.addOutputsToMap = False


# Geoprocessing Tasks (All)

# Process: Dissolve
arcpy.Dissolve_management(route, route_dissolved, "FID", "", "MULTI_PART", "DISSOLVE_LINES")
# Process: Buffer
arcpy.Buffer_analysis(route_dissolved, buf_route, Buffer_distance, "FULL", "ROUND", "ALL", "", "PLANAR")
# Process: Clip - features
arcpy.Clip_analysis(urban_atlas_clc_sea_Attica_clean, buf_route, urban_atlas_clc_sea_Attica_clean_clip, "")
# Process: Clip - raster
arcpy.Clip_management(DEM_Attica_EGSA_tif, "492202.118758799 4169178.94649716 510971.361206777 4190767.46274789", DEM_Attica_EGSA_clip_tif, buf_route, "-3.402823e+38", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
# Process: Slope
arcpy.gp.Slope_sa(DEM_Attica_EGSA_clip_tif, slope_degrees_DEM_Attica_clip_tif, "DEGREE", "1", "PLANAR", "METER")
# Process: Aspect
arcpy.gp.Aspect_sa(DEM_Attica_EGSA_clip_tif, aspect_degrees_DEM_Attica_clip_tif, "PLANAR", "METER")

# Process: Generate Points Along Lines
arcpy.GeneratePointsAlongLines_management(route_dissolved, points_diss_50m, "DISTANCE", Distance_line_to_points, "", "")
# - Process: Spatial Join - Spatial attachment of attributes from the viewpoints to the viewlines
arcpy.SpatialJoin_analysis(points_diss_50m, route, points_50m, "JOIN_ONE_TO_MANY", "KEEP_ALL", " ", "INTERSECT", "2 Meters", "")
# Process: Split Line at Point
arcpy.SplitLineAtPoint_management(route_dissolved, points_50m, route_split_no_attrib, "2 Meters")
# - Process: Spatial Join - Spatial attachment of attributes from the viewpoints to the viewlines
arcpy.SpatialJoin_analysis(route_split_no_attrib, points_50m, route_split, "JOIN_ONE_TO_ONE", "KEEP_ALL", " ", "INTERSECT", "2 Meters", "")
# Process: Add Field
arcpy.AddField_management(route_split, fieldName_01, "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")
# Process: Calculate Field
arcpy.CalculateField_management(route_split_2, fieldName_01, exp_01, "PYTHON", "")
# Process: Linear Directional Mean
arcpy.DirectionalMean_stats(route_split_3, roads_direction, "DIRECTION", fieldName_01)
# Process: Feature Vertices To Points
arcpy.FeatureVerticesToPoints_management(roads_direction, points_start_direction, "START")
# Process: Copy Features
arcpy.CopyFeatures_management(points_start_direction, points_dir_elev, "", "0", "0", "0")
# Process: Extract Multi Values to Points
arcpy.gp.ExtractMultiValuesToPoints_sa(points_dir_elev, [[DEM_Attica_EGSA_clip_tif, "RASTERVALU"]], "NONE")
# Process: Identity
arcpy.Identity_analysis(points_dir_elev, points_50m, points_dir_elev_maxspeed, "ALL", "2 Meters", "NO_RELATIONSHIPS")
# Process: Add Field
arcpy.AddField_management(points_dir_elev_maxspeed, fieldName_02, "FLOAT", "7", "3", "", "", "NULLABLE", "NON_REQUIRED", "")
# Process: Calculate Field
arcpy.CalculateField_management(points_dir_elev_maxspeed_2, fieldName_02, exp_02, "PYTHON", code_block_02)
# Process: Add Field
arcpy.AddField_management(points_dir_elev_maxspeed_3, fieldName_03, "FLOAT", "7", "3", "", "", "NULLABLE", "NON_REQUIRED", "")
# Process: Calculate Field
arcpy.CalculateField_management(points_dir_elev_maxspeed_4, fieldName_03, exp_03, "PYTHON", code_block_03)
# Process: Add Field
arcpy.AddField_management(points_dir_elev_maxspeed_5, fieldName_04, "FLOAT", "7", "3", "", "", "NULLABLE", "NON_REQUIRED", "")
# Process: Calculate Field
arcpy.CalculateField_management(points_dir_elev_maxspeed_6, fieldName_04, exp_04, "PYTHON", code_block_04)
# Process: Copy Features
arcpy.CopyFeatures_management(points_dir_elev_maxspeed_7, initial_route_viewpoints, "", "0", "0", "0")


# Preparation for the Iterative geoprocessing 

# Field name for the FID
fieldFID = "FID_points"
# Field name for the RASTERVALUE 
fieldRASTER = "RASTERVALU"

fields=[fieldFID, fieldRASTER]

# Create a temporary feature layer to run through the iteration rom the  feature class
temp_input_layer = "viewpoints_layer.shp"
arcpy.MakeFeatureLayer_management(initial_route_viewpoints, temp_input_layer)

# Initialize a variable to hold the selection for merging
merged_selection = None

# Iterate through each feature using a SearchCursor
with arcpy.da.SearchCursor(initial_route_viewpoints, fields) as cursor:     
    for row in cursor:
        fid_value = str(row[0])  # Get OBJECTID value
        elev_value = (row[1])   # Get RASTERVALUE value
                        
        sel_viewpoints_to_join = os.path.join(arcpy.env.scratchWorkspace, "sel_viewpoints_to_join_"+fid_value+".shp")
        
        # Temporarily save raster and features
        viewsheds = os.path.join(arcpy.env.scratchWorkspace, "viewsheds_"+fid_value+".tif")
        multi_values_points = os.path.join(arcpy.env.scratchWorkspace, "multi_values_points_"+fid_value+".shp")
        multi_values_clc_points = os.path.join(arcpy.env.scratchWorkspace, "multi_values_clc_points_"+fid_value+".shp") 
        multi_values_clc_points_join = multi_values_clc_points        
        Output_for_Model_4 = multi_values_clc_points_join  
        Output_for_Model_4_Land = os.path.join(arcpy.env.scratchWorkspace, "Output_for_Model_4_Land_"+fid_value+".shp")    
        Output_for_Model_4_Land_Copy = Output_for_Model_4_Land
        Output_for_Model_4_Land_Copy_1 = Output_for_Model_4_Land_Copy
        Output_for_Model_4_Land_Copy_2 = Output_for_Model_4_Land_Copy_1
        Output_for_Model_4_Land_Copy_3 = Output_for_Model_4_Land_Copy_2
        Output_for_Model_4_Land_Copy_4 = Output_for_Model_4_Land_Copy_3
        Output_for_Model_4_Land_Copy_5 = Output_for_Model_4_Land_Copy_4
        Output_for_Model_4_Land_Copy_6 = Output_for_Model_4_Land_Copy_5
        Output_for_Model_4_Land_Copy_7 = os.path.join(arcpy.env.scratchWorkspace, "Output_for_Model_4_Land_final_"+fid_value+".shp")
        
        # Temporarily save tables  
        near_table = os.path.join(arcpy.env.scratchWorkspace, "near_table_"+fid_value)        
        sum_stat = os.path.join(arcpy.env.scratchWorkspace, "sum_stat_"+fid_value)
        stat_table = os.path.join(arcpy.env.scratchWorkspace, "stat_table"+fid_value)
        
        # # where_clause for feature row (viewpoint) selection
        where_clause = fieldFID + " = " + fid_value
        
        # Select the feature row (viewpoint) using the where_clause
        arcpy.management.SelectLayerByAttribute(temp_input_layer, "NEW_SELECTION", where_clause)
        
        
        # Geoprocesses within the iteration loop - based on the selected row (viewpoint) 
        
        # - Process: Copy selected features
        arcpy.CopyFeatures_management(temp_input_layer, sel_viewpoints_to_join, "", "0", "0", "0")
        
        # - Process: Viewshed2 based on selected row (viewpoint)        
        arcpy.gp.Viewshed2_sa(DEM_Attica_EGSA_clip_tif, temp_input_layer, viewsheds, "",
                          "FREQUENCY", "0 Meters", "", "0.13", "0 Meters", "RASTERVALU", Observer_offset, "",
                          "GROUND", Viewshed_outer_radius, "GROUND", fieldName_03, fieldName_04, "90", "-90", "ALL_SIGHTLINES")                      
                       
        # - Process: Raster to Point
        arcpy.RasterToPoint_conversion(viewsheds, multi_values_points, "VALUE")
        
        # - Process: Extract Multi Values to Points
        arcpy.gp.ExtractMultiValuesToPoints_sa(multi_values_points, [[DEM_Attica_EGSA_clip_tif, "ELEV"],[slope_degrees_DEM_Attica_clip_tif, "SLOPE"],[aspect_degrees_DEM_Attica_clip_tif, "ASPECT"]], "NONE")
        
        # - Process: Identity 
        arcpy.Identity_analysis(multi_values_points, urban_atlas_clc_sea_Attica_clean_clip, multi_values_clc_points, "ALL", "", "NO_RELATIONSHIPS")
                 
        # - Process: Generate Near Table
        arcpy.GenerateNearTable_analysis(temp_input_layer, multi_values_clc_points, near_table, "", "NO_LOCATION", "ANGLE", "ALL", "0", "PLANAR")
        
         # - Process: Join Field
        arcpy.JoinField_management(multi_values_clc_points_join, "FID", near_table, "NEAR_FID", "IN_FID;NEAR_FID;NEAR_DIST;NEAR_RANK;NEAR_ANGLE")
        
        # - Process: Add Field 
        arcpy.AddField_management(multi_values_clc_points_join, fieldName_05, "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
        
        # - Process: Add Field 
        arcpy.AddField_management(multi_values_clc_points_join, fieldName_06, "FLOAT", fieldPrecision, fieldScale,
                          field_alias=fieldAlias, field_is_nullable="NULLABLE")
        
        # - Process: Calculate Field 
        arcpy.CalculateField_management(multi_values_clc_points_join, fieldName_05, exp_05, "PYTHON")
        
        # - Process: Calculate Field 
        arcpy.CalculateField_management(multi_values_clc_points_join, fieldName_06, exp_06, "PYTHON")
        
        
        
        # Execute AddField for all new fields

        arcpy.AddField_management(Output_for_Model_4, fieldName_08, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_09, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_10, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_11, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_12, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_13, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")

        arcpy.AddField_management(Output_for_Model_4, fieldName_14, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")
                                  
        arcpy.AddField_management(Output_for_Model_4, fieldName_15, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")
                                  
        arcpy.AddField_management(Output_for_Model_4, fieldName_16, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")                          
        
        arcpy.AddField_management(Output_for_Model_4, fieldName_17, "FLOAT", fieldPrecision, fieldScale,
                                  field_alias=fieldAlias, field_is_nullable="NULLABLE")
                                  
                                  
        # Execute CalculateField for all new fields
       
        # - Calculations
        arcpy.CalculateField_management(Output_for_Model_4, fieldName_08, exp_07, "PYTHON")
        
        arcpy.CalculateField_management(Output_for_Model_4, fieldName_09, exp_08, "PYTHON")

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_10, exp_09, "PYTHON")

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_11, exp_10, "PYTHON")

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_12, exp_11, "PYTHON")

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_13, exp_12, "PYTHON", code_block_12)

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_14, exp_13, "PYTHON", code_block_13)
        
        arcpy.CalculateField_management(Output_for_Model_4, fieldName_15, exp_14, "PYTHON")
        
        arcpy.CalculateField_management(Output_for_Model_4, fieldName_16, exp_15, "PYTHON")

        arcpy.CalculateField_management(Output_for_Model_4, fieldName_17, exp_16, "PYTHON")

        # Process: Summary Statistics
        arcpy.Statistics_analysis(Output_for_Model_4, stat_table, "PerVSI SUM", "code_2018")

        # Process: Join Field
        arcpy.JoinField_management(Output_for_Model_4, "code_2018", stat_table, "code_2018", "FREQUENCY;SUM_PerVSI")
        
        
        
        # Processes for the Landscape Index
        
        # - Processes in the viewshed points        
        
        # -- Process: Dissolve
        arcpy.Dissolve_management(Output_for_Model_4, Output_for_Model_4_Land, "SUM_PERVSI", "FID FIRST;NEAR_FID FIRST;code_2018 FIRST;class_2018 FIRST;FREQUENCY FIRST", "MULTI_PART", "DISSOLVE_LINES")

        # -- Process: Add Field
        arcpy.AddField_management(Output_for_Model_4_Land_Copy, fieldName_18, "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        # -- Process: Summary Statistics
        arcpy.Statistics_analysis(Output_for_Model_4_Land, sum_stat, "SUM_PERVSI SUM", "")

        # -- Process: Join Field
        arcpy.JoinField_management(Output_for_Model_4_Land_Copy_1, fieldName_18, sum_stat, "FID", "SUM_SUM_PERVSI")

        # -- Process: Add Field (2)
        arcpy.AddField_management(Output_for_Model_4_Land_Copy_2, fieldName_19, "FLOAT", "7", "2", "", "", "NULLABLE", "NON_REQUIRED", "")

        # -- Process: Calculate Field
        arcpy.CalculateField_management(Output_for_Model_4_Land_Copy_3, fieldName_19, exp_17, "PYTHON", "")

        # -- Process: Add Field (3)
        arcpy.AddField_management(Output_for_Model_4_Land_Copy_4, fieldName_20, "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")

        # -- Process: Calculate Field (2)
        arcpy.CalculateField_management(Output_for_Model_4_Land_Copy_5, fieldName_20, exp_18, "PYTHON", "")
        
        
        # - Process for joining the viewshed points with the viewpoints
        
        # -- Adding common field
        
        # Process: Add Field (4)
        arcpy.AddField_management(Output_for_Model_4_Land_Copy_6, fieldName_05, "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
        
        # Process: Calculate Field (1)
        arcpy.CalculateField_management(Output_for_Model_4_Land_Copy_6, fieldName_05, exp_05, "PYTHON")
        
        # Process: Dissolve
        arcpy.Dissolve_management(Output_for_Model_4_Land_Copy_6, Output_for_Model_4_Land_Copy_7, "VPoint", "SUM_PERVSI MAX;FIRST_code LAST;FIRST_clas LAST;LandComp LAST;LandNam LAST", "MULTI_PART", "DISSOLVE_LINES")
        
        # -- Joining with common field
                     
        # Process: Join Field (2)
        arcpy.JoinField_management(sel_viewpoints_to_join, "FID_points", Output_for_Model_4_Land_Copy_7, "VPoint", "")
        
        
        # Process: Merge all viewpoints into one shapefile    
        
        # - Get the selected feature for the current iteration
        selected_features = arcpy.management.CopyFeatures(sel_viewpoints_to_join, "in_memory/selected_features")

        # - Merge the selected features with the previously merged selection
        if merged_selection is None:
            # If this is the first feature, initialize the merged selection
            merged_selection = arcpy.management.CopyFeatures(selected_features, "in_memory/merged_selection")
        else:
            # Merge the current selection with the previously merged features
            temp_merged = "in_memory/temp_merged"
            merged_selection = arcpy.management.Merge([merged_selection, selected_features], temp_merged)
            
            # Replace the old merged selection with the new temporary merged result
            merged_selection = arcpy.management.CopyFeatures(temp_merged, "in_memory/merged_selection")

# After the iteration (loop), clear the selection if needed
arcpy.management.SelectLayerByAttribute(temp_input_layer, "CLEAR_SELECTION")

# After the iteration, the final merged selection is saved to the output merged viewpoints
arcpy.management.CopyFeatures(merged_selection, merged_viewpoints)                             
# Process: Copy Features
arcpy.management.CopyFeatures(merged_viewpoints, merged_viewpoints_new)

# Adding a new field with information about the roadsID
# - Process: Add Field 
arcpy.AddField_management(merged_viewpoints_new, fieldName_07, "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
# -Execute CalculateField
arcpy.CalculateField_management(merged_viewpoints_new, fieldName_07, exp_19, "PYTHON")

# Creating view lines from viewpoints (pairwise), attributing the information carried in viewpoints 
# - Process: Spatial Join - Spatial attachment of attributes from the viewpoints to the viewlines
arcpy.SpatialJoin_analysis(route_split_3, merged_viewpoints_new, view_lines_attributes, "JOIN_ONE_TO_MANY", "KEEP_ALL", " ", "INTERSECT", "2 Meters", "")
# - Process: Dissolve - View Line records dissolve based on TARGET_FID (if the records have the same landcover)
arcpy.Dissolve_management(view_lines_attributes, view_lines_landscape, "TARGET_FID;LAST_FIRST", "VPoint FIRST;RoadID FIRST;LAST_FIRST FIRST;LAST_FIR_1 FIRST;LAST_LandC MEAN;LAST_LandN FIRST", "MULTI_PART", "DISSOLVE_LINES")
# - View Line records dissolve based on TARGET_FID (if the records have the same landcover)
# -- Process: Summary Statistics based on TARGET_FID - to get the maximum values (if the records have the same landcover)
arcpy.Statistics_analysis(view_lines_landscape, viewline_stats, "MEAN_LAST_ MAX", "TARGET_FID")
# -- Process: Copy Features
arcpy.CopyFeatures_management(view_lines_landscape, view_lines_landscape_copy, "", "0", "0", "0")
# -- Process: Join Field
arcpy.JoinField_management(view_lines_landscape_copy, "TARGET_FID", viewline_stats, "TARGET_FID", "MAX_MEAN_LAST_")
# -- Process: Add Field - to 'stabilize' the field name
arcpy.AddField_management(view_lines_landscape_copy_1, fieldName_21, "FLOAT", fieldPrecision, fieldScale, field_alias=fieldAlias, field_is_nullable="NULLABLE")
# -- Process: Calculate Field - the new field gets the max value 
arcpy.CalculateField_management(view_lines_landscape_copy_2, fieldName_21, exp_20, "PYTHON", "")
# -- Process: Add Field - to assign the max values only to the suitable records (based on TARGET_FID)
arcpy.AddField_management(view_lines_landscape_copy_3, fieldName_22, "FLOAT", fieldPrecision, fieldScale, field_alias=fieldAlias, field_is_nullable="NULLABLE")
# -- Process: Calculate Field - the new field gets value 9999 if a condition is not met 
arcpy.CalculateField_management(view_lines_landscape_copy_4, fieldName_22, exp_21, "PYTHON", code_block_21)
# -- Process: Select - only records with values <> 9999 are retained
arcpy.Select_analysis(view_lines_landscape_copy_5, view_lines_landscape_final, exp_22)
# -- Process: Delete Field - to 'clean' the view lines from unneeded/superfluous fields
arcpy.DeleteField_management(view_lines_landscape_final, "LAST_FIRST;MEAN_LAST_;FIRST_LA_2;MAX_MEAN_L;MaxLand")
# -- Process: Add Field - to assign to each record the dominant Landscape Character as a combination of i) landcover code & ii) dominant landcover percentage (as text)
arcpy.AddField_management(view_lines_landscape_final_1, fieldName_23, "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")
# -- Process: Calculate Field - the Landscape Character field is calculated 
arcpy.CalculateField_management(view_lines_landscape_final_2, fieldName_23, exp_23, "PYTHON", "")


print("Process completed: The segments of the highway route have been classified \n\n")


print("	RouteLAND \n")
print("	Copyright (C) 2025 Loukas-Moysis Misthos (University of West Attica) \n")
print("	This program is free software: you can redistribute it and/or modify \n")
print("	it under the terms of the GNU General Public License as published by \n")
print("	the Free Software Foundation, either version 3 of the License, or \n")
print("	(at your option) any later version. \n")
print("	This program is distributed in the hope that it will be useful, \n")
print("	but WITHOUT ANY WARRANTY; without even the implied warranty of \n")
print("	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the \n")
print("	GNU General Public License for more details. \n")
print("	You should have received a copy of the GNU General Public License \n")
print("	along with this program.  If not, see <https://www.gnu.org/licenses/>. \n")