# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
import os
import arcpy
from importlib import reload
reload(ssurgo)

# myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
myhuc.build_urls()
# myhuc.write_huc(out_file='data/test.xlsx')
myhuc.download(save_directory='data')
# myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
# myhuc.write_huc(out_file='data/testlog.xlsx') # start log file

# myhuc.save_huc(filename='data/myhuc')
# del myhuc
# myhuc = ssurgo.open_huc(filename='data/myhuc')
myhuc.unpack()
# myhuc.save_huc(filename='data/myhuc')

# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')

# `merge()`
myhuc.merge(filename=filename, file_dir=file_dir)
# prove that `merge()` worked
# arcpy.env.workspace = r'data\test.gdb'
# datasets = arcpy.ListDatasets()
# datasets = [''] + datasets if datasets is not None else []
# mydata = []
# for ds in datasets:
#     for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
#         path = os.path.join(arcpy.env.workspace, ds, fc)
#         print(path)
#         mydata.append(path)


# arcpy.env.workspace = os.path.join(os.getcwd(), r'data\test.gdb')
# arcpy.management.DeleteFeatures(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))
# `join()`
myhuc.join(
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
)
myhuc.convert()
myhuc.select()
myhuc.save_huc(filename='data/myhuc')
myhuc.write_huc(out_file='data/testlog.xlsx')

input_user = os.path.join(os.getcwd(), 'data', 'mygdb.gdb')
myhuc.copy(save_dir=input_user)











#################################
# scaled up example
#################################
# collect user input
input_user = os.path.join(os.getcwd(), 'data', 'mygdb2.gdb')
# process user input
realpath = input_user
splitpath = realpath.split('\\')
findindex = len(splitpath)-1
gdbname = splitpath[findindex]
splitpath.pop(gdbname)
shortpath = splitpath
shortpath.pop() # removes last element from list
shortpath = os.path.join(*shortpath)
shortpath = shortpath.replace('C:', 'C:\\')
if not os.path.isdir(realpath):
    arcpy.management.CreateFileGDB(shortpath, gdbname)

# copy tables
for i in range(0, len(myhuc.out_tables)):
    copied_table_name =  os.path.split(myhuc.out_tables[i])[1]
    out_data = os.path.join(realpath, copied_table_name)
    in_data = myhuc.out_tables[i]
    arcpy.management.Copy(in_data, out_data)
# copy Mapunits
# arcpy.env.workspace = r'data\test.gdb'
arcpy.env.workspace = os.path.split(myhuc.out_tables[0])[0]
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []
mydata = []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        mydata.append(path)
in_data = os.path.join(os.getcwd(), mydata[0])
copied_table_name = os.path.split(in_data)[1]
out_data = os.path.join(realpath, copied_table_name)
arcpy.management.Copy(in_data, out_data)

###################################################



path = os.path.join(os.getcwd(), r'data')
gdb_name = "fGDB5.gdb"
arcpy.management.CreateFileGDB(path, gdb_name)





shortpath == path







os.path.normpath(shortpath)




os.path.split(myhuc.out_features[0])
save_dir = os.path.join(os.getcwd() + r'data\test.gdb')
save_dir = os.path.normpath(save_dir)
destinations = []
for table in myhuc.out_tables:
    destination = os.path.join(save_dir, os.path.split(table)[1])
    # print(destination)
    destinations.append(destination)

os.path.normpath(destinations[0])













# concrete
table = myhuc.out_tables[0]
table_cols = final_field_names[table]["colnames"]
delete_me = table_cols[5:10]
arcpy.management.DeleteField(table, [f.name for f in arcpy.ListFields(table)][5], 'KEEP_FIELDS')


myoutput = {}
for i in range(0, len(myhuc.out_tables)):
    table = myhuc.out_tables[i]
    # print(table)
    table_cols = myhuc.field_names[myhuc.out_features[i]]["colnames"]
    # print(table_cols)
    if myhuc.out_features[i].endswith('ECO_MonitoringLocations_EsriSSRUGO_temp'):
        start_field = 'IMLOCNAME'
    elif myhuc.out_features[i].endswith('ECO_MonitoringLocationsData_EsriSSRUGO_temp'):
        start_field = 'DATAIMLOCNAME'
    else:
        print('problem')
    # print(start_field)
    find_index = table_cols.index(start_field)
    # print(find_index)
    delete_cols = table_cols[find_index:]
    # print(delete_cols)
    arcpy.management.DeleteField(table, delete_cols)
    print('got here')
    myoutput[table] = {
                    'ncol': len([f.name for f in arcpy.ListFields(table)]),
                    'colnames': [f.name for f in arcpy.ListFields(table)]
                }







# concrete
start_field = 'IMLOCNAME'
layer_colnames = myhuc.field_names[myhuc.out_features[0]]["colnames"] # tempvar holding the `layer`'s column names
final_index = layer_colnames.index(start_field) # find the index of `start_field` in the `layer`'s column names
table_cols = layer_colnames[:final_index] # list slice columns up to but not including `final_index`
delete_cols = layer_colnames[final_index:]
table = myhuc.out_tables[0]
arcpy.management.DeleteField(table, delete_cols)

# test
mytest = myhuc.field_names[myhuc.out_features[0]]["colnames"]
myhuc.field_names[myhuc.out_features[0]]["colnames"]
len(myhuc.field_names[myhuc.out_features[0]]["colnames"])
for feature in myhuc.out_features:
    'INDICATORCAT'in myhuc.field_names[feature]["colnames"]

myhuc.out_features[1].endswith('ECO_MonitoringLocationsData_EsriSSRUGO_temp')
myhuc.field_names[myhuc.out_features[1]]["colnames"]
myhuc.field_names[myhuc.out_features[0]]["colnames"]
# abstract

final_field_names = {}
for i in range(0, len(myhuc.out_features)):
    if myhuc.out_features[i].endswith('ECO_MonitoringLocations_EsriSSRUGO_temp'):
        start_field = 'IMLOCNAME'
    elif myhuc.out_features[i].endswith('ECO_MonitoringLocationsData_EsriSSRUGO_temp'):
        start_field = 'DATAIMLOCNAME'
    # print(start_field)
    layer_colnames = myhuc.field_names[myhuc.out_features[i]]["colnames"] # tempvar holding the `layer`'s column names
    final_index = layer_colnames.index(start_field) # find the index of `start_field` in the `layer`'s column names
    table_cols = layer_colnames[:final_index] # list slice columns up to but not including `final_index`
    delete_cols = layer_colnames[final_index:]
    # `table` is the name of a table
    # `field` is an iterable of field name strings
    # `KEEP_FIELDS` or ` DELETE_FIELDS` tells the function whether to keep or delete the fields provided in `field`
    # arcpy.management.DeleteField(table, field, 'KEEP_FIELDS') # delete fields other than those in `table_cols`
    final_field_names[myhuc.out_tables[i]] = { # capture output
                    'ncol': len(table_cols),
                    'colnames': table_cols
                }

import json
print(json.dumps(final_field_names, indent = 4))
# can you arcpy.ListFields() a table???






























































# convert feature layer to table proof-of-concept:
target_feature = os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
out_features = [] # list of join output layer filenames
for feature in join_features:
    first_part = os.path.split(target_feature)[0]
    if feature.endswith('_pt'):
        second_part = os.path.split(feature)[1].replace('_pt', '_EsriSSRUGO_temp')
        out_features.append(os.path.normpath(first_part + '\\' + second_part))


out_tables = []
for feature in out_features:
    table = feature.replace('_temp', '_tbl')
    out_tables.append(table)

print(f'Converting {len(out_tables)} layers to tables...')
for i in range(0, len(out_tables)):
    target_gdb = os.path.split(out_tables[i])[0]
    arcpy.env.workspace = target_gdb
    temp_layer = os.path.split(out_features[i])[1]
    out_table = os.path.split(out_tables[i])[1]
    if self.verbose == True:
        print('----------')
        print(f'{str(i+1)}. target gdb: {target_gdb}')
        print(f'Convert this feature layer: {temp_layer}')
        print(f'To this table: {out_table}')
        print('----------')
    arcpy.conversion.ExportTable(temp_layer, out_table)

    # arcpy.env.workspace = os.path.split(table)[0]
split_file = os.path.split(out_features[0])[1]
arcpy.conversion.ExportTable(split_file, "test")










# AN EXAMPLE OF FUNCTIONAL SYNTAX TO CONVERT FEATURE LAYER TO TABLE:
split_file = os.path.split(out_features[0])[1]
arcpy.env.workspace = os.path.split(out_features[0])[0]
split_file = os.path.split(out_features[0])[1]
arcpy.conversion.ExportTable(split_file, "test")


























arcpy.env.workspace = r'data\test.gdb'
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)

in_table = os.path.normpath(myhuc.huc_data["out_layers"][0])
out_view = os.path.normpath(in_table + '_test')
arcpy.management.MakeTableView(in_table, out_view)
arcpy.conversion.ExportTable(in_table, out_view)

# myhuc.write_huc(out_file='data/testlog.xlsx')

arcpy.conversion.ExportTable(
    r'C:\\Users\\cwainright\\OneDrive - DOI\\Documents\\data_projects\\2023\\20230322_iss144_ssurgo\\data\\test.gdb\\ECO_MonitoringLocations_EsriSSRUGO_tbl;C:\\Users\\cwainright\\OneDrive - DOI\\Documents\\data_projects\\2023\\20230322_iss144_ssurgo\\data\\test.gdb\\ECO_MonitoringLocationsData_EsriSSRUGO_tbl',
    r'C:\\Users\\cwainright\\OneDrive - DOI\\Documents\\data_projects\\2023\\20230322_iss144_ssurgo\\data\\test.gdb\\ECO_MonitoringLocations_EsriSSRUGO_tbl;C:\\Users\\cwainright\\OneDrive - DOI\\Documents\\data_projects\\2023\\20230322_iss144_ssurgo\\data\\test.gdb\\ECO_MonitoringLocationsData_EsriSSRUGO_tbl_out',
)

import arcpy
os.path.split(out_features[0])[0]

arcpy.env.workspace = os.path.split(out_features[0])[0]
split_file = os.path.split(out_features[0])[1]
arcpy.conversion.ExportTable(split_file, "test")


'ksat' in [f.name for f in arcpy.ListFields(out_features[0])]
'ksat' in [f.name for f in arcpy.ListFields(target_feature)]





len([f.name for f in arcpy.ListFields(out_features[0])])
len([f.name for f in arcpy.ListFields(target_feature)])
[f.name for f in arcpy.ListFields(out_features[0])]
[f.name for f in arcpy.ListFields(target_feature)]




for attr in [f.name for f in arcpy.ListFields(out_features[0])]:
    print(f'{attr}: {attr in [f.name for f in arcpy.ListFields(target_feature)]}')












os.path.split(os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'))[1]
# prove that `join()` worked
# arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\join_output')) # check output
# len([f.name for f in arcpy.ListFields(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))])
# myhuc.save_huc(filename='data/myhuc')
myhuc.select(
    start_field='INDICATORCAT',
    delete_from=''
)
start_field = 'INDICATORCAT'
final_index = myhuc.field_names.index(start_field)
# myhuc.final_fieldnames = myhuc.field_names[:final_index]
delete_fields = myhuc.field_names[final_index:]
delete_from = myhuc.out_layer
arcpy.management.DeleteField(delete_from, delete_fields)
myhuc.write_huc(out_file='data/testlog.xlsx') # update log file


import json
print(json.dumps(myhuc.field_names, indent=4))

os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt").replace('_pt', '_tbl')

join_features = (
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt")
)

for feature in join_features:
    feature.replace('_pt', '_tbl')


arcpy.env.workspace = os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!\\\IMD).)*', join_features[0])[0]))
import re
join_features_ok = []
for feature in join_features:
    arcpy.env.workspace = os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!\\\IMD).)*', feature)[0]))
    datasets = arcpy.ListDatasets()
    datasets = [''] + datasets if datasets is not None else []

    paths = []
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            path = os.path.normpath(os.path.join(arcpy.env.workspace, ds, fc))
            print(path)
            paths.append(path)
    if os.path.normpath(feature) in paths:
        join_features_ok.append(True)
    else:
        join_features_ok.append(False)












target_feature = os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
join_features = (
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt")
)

out_features = [] # list of join output layer filenames
for feature in join_features:
    first_part = os.path.split(target_feature)[0]
    if feature.endswith('_pt'):
        second_part = os.path.split(feature)[1].replace('_pt', '_EsriSSRUGO_tbl')
        out_features.append(os.path.normpath(first_part + '\\' + second_part))

for i in range(0, len(join_features)):
    arcpy.analysis.SpatialJoin(target_feature, join_features[i], out_features[i])

arcpy.analysis.SpatialJoin(target_feature, join_features[0], out_features[0])
arcpy.analysis.SpatialJoin(target_feature, join_features[1], out_features[1])


arcpy.env.workspace = r'data\test.gdb'
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)



















# MANUAL JOIN

# step 1
# myhuc.join(
#     os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
#     target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
# )


arcpy.management.GetCount(os.path.join(os.getcwd(), r'data\test.gdb\ECO_MonitoringLocations_tbl')) # check output
len([f.name for f in arcpy.ListFields(os.path.join(os.getcwd(), r'data\test.gdb\ECO_MonitoringLocations_tbl'))])
# step 2
myhuc.join(
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'),
    out_feature=os.path.join(os.getcwd(), r'data\test.gdb\ECO_MonitoringLocationsData_tbl')
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
