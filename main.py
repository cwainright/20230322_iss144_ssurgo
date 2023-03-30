# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
import os
import arcpy
from importlib import reload
reload(ssurgo)

# myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
# myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
# myhuc.build_urls()
# myhuc.write_huc(out_file='data/test.xlsx')
# myhuc.download(save_directory='data')
# myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
# myhuc.write_huc(out_file='data/log.xlsx') # start log file

# myhuc.save_huc(filename='data/myhuc')
# del myhuc
myhuc = ssurgo.open_huc(filename='data/myhuc')
# myhuc.unpack()
# myhuc.save_huc(filename='data/myhuc')

# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')

# `merge()`
myhuc.merge(filename=filename, file_dir=file_dir)
# prove that `merge()` worked
arcpy.env.workspace = r'data\test.gdb'
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []
mydata = []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)
        mydata.append(path)

# arcpy.env.workspace = os.path.join(os.getcwd(), r'data\test.gdb')
# arcpy.management.DeleteFeatures(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))
# `join()`
myhuc.join(
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'),
    dest_feature=os.path.join(os.getcwd(), r'data\test.gdb\join_output')
)




# MANUAL JOIN

# step 1
myhuc.join(
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'),
    out_feature=os.path.join(os.getcwd(), r'data\test.gdb\temp1')
)
arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\temp1')) # check output
len([f.name for f in arcpy.ListFields(os.path.join(os.getcwd(), r'data\test.gdb\temp1'))])
# step 2
myhuc.join(
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\temp1'),
    out_feature=os.path.join(os.getcwd(), r'data\test.gdb\temp2')
)
arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\temp2')) # check output
len([f.name for f in arcpy.ListFields(os.path.join(os.getcwd(), r'data\test.gdb\temp2'))])
# step 3: copy output
arcpy.management.CopyFeatures(os.path.join(os.getcwd(), r'data\test.gdb\temp2'), os.path.join(os.getcwd(), r'data\test.gdb\join_output'))
arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\join_output')) # check output
len([f.name for f in arcpy.ListFields(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))])


# AUTOMATE THE MANUAL JOIN
dest_feature = os.path.join(os.getcwd(), r'data\test.gdb\test_output')
target_feature = os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
join_features = (
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\test1"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\test2"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\test3")
)
temps = []
for i in range(0, len(join_features)):
    temp = 'data\\test.gdb\\temp' + str(i+1)
    temps.append(temp)
out_features = []
for i in range(0, len(join_features)):
    out_feature = os.path.join(os.getcwd(), temps[i])
    out_features.append(out_feature)

counter = 0
# arcpy.analysis.SpatialJoin(target_feature, join_features[0], out_features[0])
# if self.verbose == True:
print(f'counter: {int(counter) + 1}; (type: join_feature to target_feature); {join_features[0]}')

# join nth feature
counter += 1
if len(join_features) > 1:
    for i in range(1, len(join_features)): # start loop at [1] to avoid double-joining layer at index [0]
        # arcpy.analysis.SpatialJoin(out_features[i-1], join_features[i], out_features[i])
        # if self.verbose == True:
        print(f'counter: {int(counter) + 1}; (type: join_feature to out_feature); {join_features[i]}')
        counter += 1
print(f'Joined features saved here:')
print('----------')
os.path.join(os.getcwd(), r'data\test.gdb\join_output')
# arcpy.management.CopyFeatures(join_features[len(join_features)-1], os.path.join(os.getcwd(), r'data\test.gdb\join_output'))





mydesc = arcpy.Describe(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))
print("Feature Type:  " + mydesc.featureType)
print("Shape Type: " + mydesc.shapeType)

arcpy.management.GetCount(os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"))
arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'))
arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))




join_features = (
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt")
)


target_feature = os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
out_feature = os.path.join(os.getcwd(), r'data\test.gdb\join_output')
arcpy.analysis.SpatialJoin(target_feature, join_features[0], out_feature)
[f.name for f in arcpy.ListFields(out_feature)]
for i in range(1, len(join_features)): # start loop at [1] to avoid double-joining layer at index [0]
    arcpy.analysis.SpatialJoin(out_feature, join_features[i], out_feature)




self.field_names = [f.name for f in arcpy.ListFields(out_feature)]

out_feature = 'data/test.gdb/join_output'
mytest = out_feature.split('/')
os.path.join(os.getcwd(), *mytest)
field_names = [f.name for f in arcpy.ListFields(out_feature)] # will only return colnames if join worked

out_feature = os.path.join(os.getcwd(), r'data\test.gdb\join_output')
field_names = [f.name for f in arcpy.ListFields(out_feature)]
myhuc.testnames = field_names


# `select()`
field_names.index("INDICATORCAT")
mytest = field_names[:field_names.index("INDICATORCAT")]





os.path.split(target_feature)[0]














































join_features = (
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt")
)

os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!/IMD).)*', os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"))[0]))
for feature in join_features:
    output = os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!/IMD).)*', feature)[0]))
    print(output)
    # arcpy.env.workspace = os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!/IMD).)*', feature)[0]))
    arcpy.env.workspace = os.path.join(os.getcwd(), feature)
    datasets = arcpy.ListDatasets()
    datasets = [''] + datasets if datasets is not None else []

    paths = []
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            path = os.path.normpath(os.path.join(arcpy.env.workspace, ds, fc))
            paths.append(path)
            print(path)

















re.search('(?:(?!\\\IMD).)*', os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"))[0]










































os.path.normpath(r'C:\Users\cwainright\OneDrive - DOI\Documents\data_projects\2023\20230322_iss144_ssurgo\data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationLogistics_py')
mystring = os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]
re.search('(^.*[/$])', mystring)
re.search('(^.*[/$])', mystring)

os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!/IMD).)*', mystring)[0]))



mystring = os.path.join(os.getcwd(), "data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt")
myanswer = re.search('(?:(?!NCRN).)*', mystring)
myanswer[0]

arcpy.env.workspace = os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

paths = []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        paths.append(path)

'data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt' in paths





target_features = "data/test.gdb/Mapunits"
join_features = "data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt"
out_feature_class = "data/test.gdb/testjoin1"
arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)

target_features = "data/test.gdb/testjoin1"
join_features = "data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocationsData_pt"
out_feature_class = "data/test.gdb/testjoin2"
arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)





os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]












arcpy.env.workspace = r'data\NCRN_Monitoring_Locations.gdb'
# datasets = arcpy.ListDatasets(feature_type='feature')
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)
