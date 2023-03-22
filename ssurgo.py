# a file that holds classes and methods used to parse ssurgo soil data
# https://github.com/NCRN/NCRN_DM/issues/144


import pandas as pd
import wget
import os
import datetime

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
            # look for `save_directory` that user provided
            # if exists, move on, else make dir
            dir_found = False
            if os.path.isdir(save_directory):
                dir_found = True
            elif os.path.exists(os.path.join(os.getcwd(), save_directory)):
                dir_found = True
            else:
                # print(f'`{save_directory}` not found')
                # raise NotADirectoryError
                os.makedirs(save_directory)
                dir_found = True
            
            if dir_found == True:
                start_dtm = datetime.datetime.now()
                for url in self.huc_data['url']:
                    print(url)
                    # wget.download(url=url, out=save_directory, bar=download_progress_bar_custom)
                # print('dir found!')
                end_dtm = datetime.datetime.now()
                print(f'Time elapsed: {end_dtm - start_dtm}')
            else:
                raise NotADirectoryError
        except NotADirectoryError as e:
            print(e)
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
