# a file that holds classes and methods used to parse ssurgo soil data
# https://github.com/NCRN/NCRN_DM/issues/144


import pandas as pd
import wget
import os
import datetime
import urllib.request
import pickle
import arcpy
import json
import re

class Huc():
    '''
    # A class that holds HUC lookup codes
    '''

    def __init__(self, filename:str, sheet:str='', VERBOSE:bool=False) -> None:
        '''
        # Constructor for class Huc
        
        ### `filename`; kwarg; str
            - Required
            - Only two filetypes are accepted: xlsx and csv
            - The filename of the file containing the xlsx of huc codes
            - Must include file extension (.xlsx or .csv)
            - File file must have two columns: 'HUC8' and 'Name'. E.g.,
                |  HUC8  |  Name  |
                |  ------  | ------  | 
                |  02070008  |  Middle Potomac-Catoctin  |
        ### `sheet`; kwarg; str
            - Optional
            - In the case that the xlsx in `filename` has multiple sheets, provide the name of the sheet containing HUC8 codes & names
            - When provided, `sheet` is used to load xlsx data to pd dataframe
        ### `VERBOSE`; kwarg; bool
            - Required, default False
            - A constant that turns on messaging and pretty-printing for the interactive console

        ### Examples
        ```
        import ssurgo
        myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
        myhuc.huc_data
        ```
        '''
        # super().__init__()
        try:
            # validate user input
            if isinstance(filename, str):
                if filename.endswith('.xlsx'):
                    self.filename = filename
            else:
                print('error filename xlsx')
            if isinstance(sheet, str):
                self.sheet = sheet
            else:
                print('error sheet not string')
            if isinstance(VERBOSE, bool):
                self.verbose = VERBOSE
            else:
                print('error verbose not bool')

            # build huc dataframe
            self.huc_data = self._parse_huc()

            # provide user feedback
            # successful instantiation returns a pd.dataframe of at least one row and two columns
            if self.huc_data.shape[0] >= 1:
                if self.huc_data.shape[1] >= 2:
                    if self.verbose == True:
                        print(bcolors.OKBLUE + '`Huc` created!' + bcolors.ENDC)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            return None

    def _parse_huc(self):
        '''
        # Parse HUC data from the filename 

        ### A protected helper method for instantiating objects of class Huc; accepts no args

        ### Returns
            - pandas `DataFrame`
            - DataFrame has at least one row and at least two columns

        ### Examples
        ```
        self.huc_data = self._parse_huc()
        ```
        '''
        try:
            # load data
            if self.filename.endswith('xlsx'):
                if self.sheet != '':
                    huc_data = pd.read_excel(self.filename, sheet_name=self.sheet)
                else:
                    huc_data = pd.read_excel(self.filename)
            if self.filename.endswith('csv'):
                huc_data = pd.read_csv(self.filename)

            # clean data
            huc_data["Name"] = huc_data["Name"].str.strip() # strip trailing whitespace
            huc_data["HUC8"] = huc_data["HUC8"].apply(str) # type-cast to str
            huc_data["HUC8"] = huc_data["HUC8"].str.strip() # strip trailing whitespace
            counter = 0 # start a row-counter
            for huc in huc_data['HUC8']: # check that there are no sneaky HUC12s
                counter += 1 # increment row counter
                if len(huc) > 8:
                    raise Huc8Error(problem_val=str(huc), row_num=str(counter), filename=self.filename)
            huc_data["HUC8"] = huc_data["HUC8"].str.zfill(8) # enforce 8-digit length,, adding leading zeroes if needed
            
            return huc_data
        
        except Huc8Error:
            myerror = Huc8Error(problem_val=str(huc), row_num=str(counter), filename=self.filename)
            myerror.print_problem()
        except:
            print('error parse_huc')

    def build_urls(self):
        '''
        # Build ESRI endpoint urls given huc data
        '''
        try:
            URL_STRING = r'https://soilspackage-useast.s3.amazonaws.com/2021/'
            # example: https://soilspackage-useast.s3.amazonaws.com/2021/MiddlePotomacAnacostiaOccoquan_02070010.ppkx
            urls = []
            for i in range(0, self.huc_data.shape[0]):
                urlname = self.huc_data['Name'][i].replace(" ", "")
                urlname = urlname.replace("-", "")
                urlstring = URL_STRING + urlname + '_' + self.huc_data['HUC8'][i] + '.ppkx'
                urls.append(urlstring)
            self.huc_data['url'] = urls

            if self.verbose == True:
                print('URLs created:')
                print('----------')
                mysubset = self.huc_data[['HUC8', 'Name', 'url']]
                if mysubset.shape[0] > 10: # if there are lots of rows, just show a few
                    print(mysubset.head(10))
                    print(f'\nThe first 10 of {self.huc_data.shape[0]} total records are shown here.\n')
                    print('Call `{your_huc}.huc_data` to investigate all records.')
                else:
                    print(mysubset)
        except:
            pass
    
    def write_huc(self, out_file:str):
        '''
        # Write the dataset as xlsx

        ### `out_file`; kwarg; str
            - Required
            - The (absolute or relative) filepath and filename with file extension
        ### Examples
        ```
        myhuc.write_huc(out_file='data/test.xlsx')
        ```
        '''
        try:
            if not out_file.endswith('.xlsx'):
                raise Exception
            else:
                with pd.ExcelWriter(out_file) as writer:
                    self.huc_data.to_excel(writer, sheet_name='huc_data', index=False)
        except:
            print('error `save`')

    def download(self, save_directory:str):
        '''
        # Save files at `url` endpoints to directory

        ### `save_directory`; kwarg; str
            - Required
            - The directory into which you want to save the files downloaded from the endpoints in `huc_data['url']`
            - Accepts relative or absolute filepaths
        ### Examples
        ```
        myhuc.download(save_directory='mydir/mysubdir')
        myhuc.download(save_directory='C:\\Users\\myuser\\Desktop')
        ```
        '''
        try:
            # capture job start time
            start_dtm = datetime.datetime.now()

            # check url validity before trying to download
            self._check_url_status()

            # verify dir structure, create dir structure if needed
            self._check_dirs(save_directory)

            # check our work before moving on
            mydirs = []
            for i in range(0, self.huc_data.shape[0]):
                check = os.path.isdir(self.huc_data["huc_dir"][i])
                mydirs.append(check)
            myurls = []
            for i in range(0, self.huc_data.shape[0]):
                if self.huc_data["status"][i] == '200':
                    check = True
                else:
                    check = False
                myurls.append(check)
            
            problem = True
            if all(mydirs):
                if all(myurls):
                    problem = False

            # download files and add log entries
            if problem == False:
                download_completed = []
                for i in range(0, self.huc_data.shape[0]):
                    wget.download(url=self.huc_data["url"][i], out=self.huc_data["huc_dir"][i])
                    # full_filepath = os.path.join(self.huc_data["huc_dir"][i], 'test.xlsx')
                    # self.write_huc(out_file=full_filepath)
                    download_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]) # https://www.iso.org/iso-8601-date-and-time-format.html
                    if self.verbose == True:
                        print(f'\n{self.huc_data["HUC8"][i]} download completed: {download_dtm}')
                    download_completed.append(download_dtm)
                self.huc_data['downloaded'] = download_completed # add log entries
                
                end_dtm = datetime.datetime.now() # capture job end time

                if self.verbose == True:
                    print('----------')
                    print('Job completed.')
                    print(f'Time elapsed: {end_dtm - start_dtm}')
                    print('----------')
                    print(self.huc_data)
            else:
                raise Exception
            
        except:
            print('error `download()`')

    def download_progress_bar_custom(current, total, width=80):
        """
        # Utility function to create a custom progress bar
        
        # `current`; kwarg; -- The full URL of a file on the internet as a string.
            Example: r'https://www.fws.gov/wetlands/Data/State-Downloads/DC_shapefile_wetlands.zip'
        Return:
        size -- File size in bytes as integer
        """
        #print(int(int(current) / int(total) * 100) % 10)
        if int(int(current) / int(total) * 100) % 10 == 0:
            print("Downloading: {0}% [{1} / {2}] bytes".format(current / total * 100, current, total))

    def _check_dirs(self, save_directory:str):
        '''
        # Check for directories by name, create dir if missing

        A protected method that checks the directory structure of the parent directory `save_directory` and creates child directories `HUC8`.
        ### Examples
        ```
        self._check_dirs(save_directory)
        ```
        '''
        try:
            dir_found = False
            if os.path.isdir(save_directory):
                dir_found = True
            elif os.path.exists(os.path.join(os.getcwd(), save_directory)):
                dir_found = True
            else:
                os.makedirs(save_directory)
                dir_found = True
            
            # once parent dir `save_directory` is found,
            # check child dir structure and make dirs if needed
            if dir_found == True:
                parent_dir = os.path.join(os.getcwd(), save_directory)
                huc_dirs = [] # capture huc_dirs
                for i in range(0, self.huc_data.shape[0]):
                    huc_dir = os.path.join(parent_dir, self.huc_data["HUC8"][i])
                    huc_dirs.append(huc_dir)
                    if not os.path.isdir(huc_dir):
                        os.makedirs(huc_dir)
                        if self.verbose == True:
                            print(f'Created directory \'{huc_dir}\'')
                    else:
                        if self.verbose == True:
                            print(f'Using existing directory {huc_dir}')
                self.huc_data["huc_dir"] = huc_dirs
            else:
                raise NotADirectoryError

        except NotADirectoryError as e:
            print(e)
    
    def _check_url_status(self):
        '''
        # Check that each program-generated url is valid

        A protected method that gets the http status code of each endpoint in `huc_data['url']`
        https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

        ### Examples
        ```
        self._check_url_status()
        ```
        '''
        try:
            return_codes = []
            log_times = []
            
            for url in self.huc_data['url']:
                return_code = str(urllib.request.urlopen(url).getcode())
                return_codes.append(return_code)
                log_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]) # https://www.iso.org/iso-8601-date-and-time-format.html
                log_times.append(log_time)
            self.huc_data['status_checked'] = log_times
            self.huc_data['status'] = return_codes
        except:
            print('error `_check_url_status()`')

    def save_huc(self, filename:str):
        '''
        # Save a `Huc` instance

        Allows a user to save a `Huc` instance, thereby enabling a user to work asynchronously with `Huc` objects without re-creating them for each session.

        ### `filename`; kwarg; str
            - Required
            - The filename, EXCLUDING A FILE EXTENSION, where you want to save your `Huc` instance

        ### Examples
        ```
        myhuc.save_huc(filename='data/myhuc')
        ```
        '''
        # https://www.thoughtco.com/using-pickle-to-save-objects-2813661
        try:
            object = self
            filehandler = open(filename, 'wb')
            pickle.dump(object, filehandler)
            filehandler.close()
        except:
            print('error `save_huc`')

    def unpack(self):
        '''
        # Unpack geoprocessing packages

        ### Examples
        ```
        myhuc.unpack()
        ```
        '''
        try:
            # check that dirs in self.huc_data["huc_dir"] exist
            dirs_found = []
            for dir in self.huc_data["huc_dir"]:
                if os.path.isdir(dir):
                    dir_found = True
                else:
                    dir_found = False
                dirs_found.append(dir_found)
            # print(f'dirs found: {dirs_found}')

            # check that .ppkx files exist in  self.huc_data["huc_dir"]
            # check that there's only one .ppkx file, error if there's >1
            ppkx_found = {}
            ppkx_ok = []
            for dir in self.huc_data["huc_dir"]:
                ppkx_found[dir] = {'ppkx_count': 0, 'ppkx': None, 'ok_to_unpack': False}
                arcpy.env.workspace = dir # set destination directory
                ppkx_in_dir = arcpy.ListFiles('*.ppkx')
                ppkx_count = len(arcpy.ListFiles('*.ppkx'))
                ppkx_found[dir]["ppkx_count"] = ppkx_count
                ppkx_found[dir]["ppkx"] = ppkx_in_dir
                if ppkx_found[dir]["ppkx_count"] != 1:
                    status = False
                    if self.verbose == True:
                        print(f'Zero or multiple .ppkx files detected:')
                        print(json.dumps(ppkx_found[dir]["ppkx"], indent=4))
                else:
                    status = True
                ppkx_found[dir]["ok_to_unpack"] = status
                ppkx_ok.append(status)
            

            # extract
            if all(dirs_found): # check that dirs exist
                if all (ppkx_ok): # check that there's only one ppkx to extract
                    unpack_dirs = []
                    unpack_timestamps = []
                    for dir in self.huc_data["huc_dir"]: # replace `mytest` with variable for the log file
                        arcpy.env.workspace = dir # set destination directory
                        # source_ppkx = arcpy.ListFiles('*.ppkx')[0]
                        destination_subdir = os.path.splitext(arcpy.ListFiles('*.ppkx')[0])[0] # choose a name for destination sub-directory
                        arcpy.management.ExtractPackage(arcpy.ListFiles('*.ppkx')[0], os.path.splitext(arcpy.ListFiles('*.ppkx')[0])[0])
                        # print(f'Unpacking {source_ppkx} into subdir {os.path.join(dir, destination_subdir)}')
                        unpack_dtm = datetime.datetime.now()
                        unpack_timestamps.append(unpack_dtm)
                        unpack_dir = os.path.join(dir, destination_subdir)
                        unpack_dirs.append(unpack_dir)
                    self.huc_data["unpack_dir"] = unpack_dirs
                    self.huc_data["unpack_timestamp"] = unpack_timestamps
                else:
                    raise Exception
            else:
                raise Exception
            
            if self.verbose == True:
                print('-----------')
                print('Unpack checks completed:')
                print('-----------')
                print(json.dumps(ppkx_found, indent=4))
                print('-----------')
                mysubset = self.huc_data[['HUC8', 'Name', 'unpack_dir', 'unpack_timestamp']]
                print('Unpack results:')
                print('-----------')
                if mysubset.shape[0] > 10: # if there are lots of rows, just show a few
                    print(mysubset.head(10))
                    print(f'\nThe first 10 of {self.huc_data.shape[0]} total records are shown here.\n')
                    print('Call `{your_huc}.huc_data` to investigate all records.')
                else:
                    print(mysubset)
                print('-----------')
        except:
            print('error `unpack()`')

    def merge(self, filename:str, file_dir:str):
        '''
        # Merge feature classes unpacked via `unpack()` into one file geodatabase
        
        ### `filename`; kwarg; str
            - Required
            - The filename, including file extension (.gdb), for the geodatabase (gdb) that you want to create to save the merged files feature classes into
            - e.g., `mygdb.gdb`
        ###`file_dir`; kwarg; str
            - Required
            - The filepath to the directory where you want to save `filename` gdb
        ### Examples
        ```
        # relative path
        import os # only needed for relative path
        filename = 'test.gdb'
        file_dir = os.path.join(os.getcwd(), 'data')
        myhuc.merge(filename=filename, file_dir=file_dir)

        # absolute path
        filename = 'test.gdb'
        file_dir = r'C:\\Users\\cwainright\\OneDrive - DOI\\Documents\\data_projects\\2023\\20230322_iss144_ssurgo\\data'
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
        ```
        '''
        # print('got here')
        try:
            # check that out dir exists, create if not
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
                if self.verbose == True:
                    print('Created directory:\n')
                    file_dir
            # make empty gdb
            arcpy.management.CreateFileGDB(file_dir, filename)
            self.huc_data["gdb"] = os.path.join(file_dir, filename) # save the gdb filepath to log file

            # find feature classes
            targets = []
            for dir in range(0, self.huc_data.shape[0]):
                target = os.path.join(self.huc_data["unpack_dir"][dir], 'p20')
                for file in os.listdir(target):
                    if file.endswith('.gdb'):
                        target = os.path.join(target, file)
                targets.append(target)

            feature_classes = []
            for gdb in targets:
                arcpy.env.workspace = gdb
                datasets = arcpy.ListDatasets()
                datasets = [''] + datasets if datasets is not None else []

                for ds in datasets:
                    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                        path = os.path.join(arcpy.env.workspace, ds, fc)
                        # print(f'path: {path}')
                        if path.endswith('Mapunits'): # exclude "Subbasin" and other non-"Mapunits" feature classes
                            feature_classes.append(path)
            self.merged_featureclasses = feature_classes # save

            if self.verbose == True:
                print('----------')
                print(f'Found {len(feature_classes)} feature classes to merge:')
                print('----------')
                counter = 1
                for f in feature_classes:
                    print(f'{counter}. {f}')
                    counter += 1
                print('----------')
                print('Merging...')
                print('----------')
            
            # merge feature classes into gdb
            arcpy.management.Merge(feature_classes, os.path.join(file_dir, filename, 'Mapunits'))

            # add output to log file
            self.huc_data['merge_datetime'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
            self.huc_data['merge_feature'] = path

            if self.verbose == True:
                # get proof that arcpy thinks the merge worked properly
                arcpy.env.workspace = os.path.join(file_dir, filename)
                datasets = arcpy.ListDatasets()
                datasets = [''] + datasets if datasets is not None else []

                for ds in datasets:
                    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                        path = os.path.join(arcpy.env.workspace, ds, fc)
                        print('Merged feature classes to:')
                        print('----------')
                        print(path)
                        print('----------')
                        
        except:
            print('problem `merge()`')

    def join(self, *join_features:str, target_feature:str, dest_feature:str):
        '''
        # Spatial join the gdb produced by `merge()` with NCRN monitoring locations data
        
        ### `join_features`; arbitrary arg; str
            - Required
            - Accepts one or more comma-separated feature layers to join to `target_feature`
            - e.g., 'data/mygdb.gdb/water_locations', 'data/mygdb.gdb/veg_locations'
        ### `target_feature`; kwarg; str
            - Required
            - The filepath to the feature layer to which `join_feature` will be joined
            - e.g., 'data/test.gdb/Mapunits'
        ### `out_feature`; kwarg; str
            - Required
            - The filepath to the feature layer that will result from the join
            - e.g., 'data/test.gdb/join_output'
        ### Examples
        ```
        # `join()`
        myhuc.join(
            os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt"),
            os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\ECO_MonitoringLocations_pt"),
            target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'),
            dest_feature='data/test.gdb/join_output'
        )

        # prove that `join()` worked
        dest_feature = r'data/test.gdb/join_output'
        field_names = [f.name for f in arcpy.ListFields(dest_feature)]

        # arcpy.env.workspace = r'data\\test.gdb'
        # datasets = arcpy.ListDatasets()
        # datasets = [''] + datasets if datasets is not None else []
        # mydata = []
        # for ds in datasets:
        #     for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        #         path = os.path.join(arcpy.env.workspace, ds, fc)
        #         print(path)
        #         mydata.append(path)
        # featureclass = mydata[1]
        # field_names = [f.name for f in arcpy.ListFields(featureclass)] # will only return colnames if join worked
        ```
        '''
        try:
            # confirm that the provided features exist
            target_feature_ok = False

            arcpy.env.workspace = os.path.split(target_feature)[0]
            datasets = arcpy.ListDatasets()
            datasets = [''] + datasets if datasets is not None else []

            paths = []
            for ds in datasets:
                for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                    path = os.path.join(arcpy.env.workspace, ds, fc)
                    paths.append(path)
            if os.path.normpath(target_feature) in paths:
                target_feature_ok = True

            join_features_ok = []
            for feature in join_features:
                arcpy.env.workspace = os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!\\\IMD).)*', feature)[0]))
                datasets = arcpy.ListDatasets()
                datasets = [''] + datasets if datasets is not None else []

                paths = []
                for ds in datasets:
                    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                        path = os.path.normpath(os.path.join(arcpy.env.workspace, ds, fc))
                        paths.append(path)
                if os.path.normpath(feature) in paths:
                    join_features_ok.append(True)
                else:
                    join_features_ok.append(False)
            
            if all(join_features_ok) and target_feature_ok == True:
                if self.verbose == True:
                    print('----------')
                    print(f'target_feature_ok: {target_feature_ok}')
                    print('----------')
                    print(f'join_features_ok: {join_features_ok}')
                    print('----------')
                    print(f'{len(join_features)} features provided to join:')
                    print('----------')
                    counter = 1
                    for f in join_features:
                        print(f'{counter}. {f}')
                        counter += 1
                    print('----------')
                    print('Joining...')
                    print('----------')

                # build up the temp-feature filepaths
                temps = []
                for i in range(0, len(join_features)):
                    temp = 'data\\test.gdb\\temp' + str(i+1)
                    temps.append(temp)
                out_features = []
                for i in range(0, len(join_features)):
                    out_feature = os.path.join(os.getcwd(), temps[i])
                    out_features.append(out_feature)

                # join first feature
                counter = 0
                arcpy.analysis.SpatialJoin(target_feature, join_features[0], out_features[0])
                if self.verbose == True:
                    print(f'counter: {int(counter) + 1}; (type: join_feature to target_feature); {join_features[0]}')

                # join nth feature
                counter += 1
                if len(join_features) > 1:
                    for i in range(1, len(join_features)): # start loop at [1] to avoid double-joining layer at index [0]
                        arcpy.analysis.SpatialJoin(out_features[i-1], join_features[i], out_features[i])
                        if self.verbose == True:
                            print(f'counter: {int(counter) + 1}; (type: join_feature to out_feature); {join_features[i]}')
                        counter += 1
                
                # copy output from nth joined feature to `dest_feature`
                arcpy.management.CopyFeatures(out_features[len(out_features)-1], dest_feature)

                # delete temporary features
                for layer in out_features:
                    arcpy.management.DeleteFeatures(layer)

                # save field names
                self.field_names = [f.name for f in arcpy.ListFields(dest_feature)] # will only return colnames if join worked
                # add output to log file
                self.huc_data['join_datetime'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
                self.huc_data['join_features'] = ';'.join(join_features)
                self.huc_data['out_layer'] = dest_feature

            if not self.field_names:
                raise Exception
            elif len(self.field_names) == 0:
                raise Exception

            if self.verbose == True:
                print('----------')
                print(f'Joined features saved:')
                print('----------')
                print(dest_feature)
        except:
            print('error `join()`')
    
    def select(self, start_field:str='INDICATORCAT', save_file:str='', save:bool=False):
        '''
        # Select the columns needed for the final table

        ### `start_field`; kwarg; str
            - Required
            - Default 'IMLOCID'
            - Program will select columns up to but not including the column name provided
        ### `save_file`; kwarg; str
            - Required if `save` is True
            - The filename including file extension (.csv) for the output table
        ### `save`; kwarg; bool
            - Required
            - Default False
            - True tells the program to save the table generated by `select()` to the location specified in `save_file`
        ### Examples
        ```

        ```
        '''
        try:
            field_exist = False
            if start_field in self.field_list:
                field_exist = True
            
            if field_exist == True:
                final_index = self.field_names.index(start_field)
                self.final_fieldnames = self.field_names[:final_index]

            if self.verbose == True:
                print('Original fields:')
                print('----------')
                print(self.field_names)
                print('Final fields:')
                print('----------')
                print(self.final_fieldnames)

            else:
                print('You entered a `start_field` that does not exist.')
        except:
            print('problem `select()`')

def open_huc(filename:str):
        # saving `open_huc` outside a class instance so it's accessible via `ssurgo.open_huc` not as `ssurgo.Huc.open_huc` bound method
        '''
        # Read a saved `Huc` instance

        Allows a user to read a saved `Huc` instance, thereby enabling a user to work asynchronously with `Huc` objects without re-creating them for each session.

        ### `filename`; kwarg; str
            - Required
            - The filename, EXCLUDING A FILE EXTENSION, where you saved your `Huc` instance

        ### Examples
        ```
        import ssurgo
        myhuc = ssurgo.open_huc(filename='data/myhuc')
        ```
        '''
        try:
            filehandler = open(filename, 'rb')
            object = pickle.load(filehandler)
            filehandler.close()
            return object
        except:
            print('error `open_huc`')

class Error(Exception):
    """Parent class for exceptions"""
    pass

class Huc8Error(Error):
    """
    # A child class of `Exception` that handles TypeErrors for future date strings
    
    ### Examples
    ```
    try:
        for huc in huc_data['HUC8']:
            if len(huc) > 8:
                raise Huc8Error(huc)
    except Huc8Error:
        myerror = Huc8Error(problem_val=huc)
        myerror.print_problem()
    ```
    """

    def __init__(self, problem_val:str, row_num:str, filename:str):
        self.problem_val = problem_val
        self.row_num = row_num
        self.filename = filename
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + '\n`huc` ' + bcolors.WARNING + f'\'{self.problem_val}\' at row {self.row_num} of column "HUC8" in \'{self.filename}\' caused this error.'\
            + bcolors.FAIL + '\nParameter ' \
            + bcolors.OKBLUE + '`HUC8` ' \
            + bcolors.FAIL + 'values cannot be more than eight characters in length.' + bcolors.ENDC
        
    def print_problem(self):
        print(f"{self.msg}")

class bcolors:
    '''
    # Colors used in Huc console messages

    ### Examples
    ```
    assert filepath != "", bcolors.FAIL + "`filepath` cannot be blank" + bcolors.ENDC
    print(f'{bcolors.OKGREEN} \nEmld instance created!\n {bcolors.ENDC}')
    ```
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
