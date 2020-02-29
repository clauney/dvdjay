#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 10:31:54 2020

@author: chrislauney
"""
import csv
import os
import pickle

import logging

# later, then we can stop doing stuff like saving file paths as the actual item
# =============================================================================
# class ManagedTable():
#     def __init__(self, name, *args, **kwargs):
#         self.data = []
#         self.name
#     
#     @property
#     def data(self):
#         pass
#     
#     def write(self):
#         pass
# 
# class ManagedCSV(ManagedTable):
#     pass
# 
# 
# class ManagedGSheet(ManagedTable):
#     pass
# =============================================================================

class DataStoreWrangler():
    def __init__(self, *args, **kwargs):
        self.datastores = {}
                
        self.location = kwargs.get('location')
        if self.location:
            self.init_location()

class HTTPDataStore():
    pass

class GSheetWrangler(DataStoreWrangler):
    def __init__(self, *args, **kwargs):
        super(GSheetWrangler, self).__init__(*args, **kwargs)

class OSDataStore():
    location_separator = '/'
    datastore_extension = None
    datastore_fullpath_format = '{loc}{loc_sep}{dsfile_name}{dsfile_ext}'

    def get_datastore_fullpath(self, datastore_name):
        '''
        >>>get_datastore_fullpath('mytest')
        '/Users/chrislauney/temp/mytest.csv'
        '''
        return self.datastore_fullpath_format.format(
            loc=self.location, loc_sep=self.location_separator, dsfile_name=datastore_name, dsfile_ext=self.datastore_extension)

    def check_location_exists(self):
        return os.path.exists(self.location)

    def init_location(self):
        print('old location:', self.location)
        self.location = self.location.rstrip(self.location_separator)
        print('new location:', self.location)
        if self.check_location_exists():
            if not os.path.isdir(self.location):
                logging.critical('LOCATION PROVIDED IS NOT A DIRECTORY!')
                raise FileExistsError
        else:
            os.makedirs(self.location)

    def check_datastore_exists(self, ds_name):
        '''
        >>>check_datastore_exists('mytest')
        False
        '''
        return os.path.isfile(self.get_datastore_fullpath(ds_name))

class PickleFileWrangler(DataStoreWrangler, OSDataStore):
    datastore_extension = '.pf'

    def __init__(self, *args, **kwargs):
        super(PickleFileWrangler, self).__init__(*args, **kwargs)

    def create_datastore(self, datastore_name, *args, **kwargs):
        '''
        >>>create_datastore('dvds')
        '''
        if datastore_name in self.datastores or self.check_datastore_exists(datastore_name):
            logging.error('CREATE ERROR! datastore in self.datastores (%s) or datastore in location (%s)',
                          datastore_name in self.datastores, self.check_datastore_exists(datastore_name))
        ds_path = self.get_datastore_fullpath(datastore_name)
        try:
            with open(ds_path, 'xb') as pf:
                pass
            self.datastores[datastore_name] = ds_path
            return ds_path
        except:
            return False

    def replace_datastore(self, datastore_name, data):
        '''
        
        '''
        ds_path = self.get_datastore_fullpath(datastore_name)
        if not datastore_name in self.datastores:
            if self.check_datastore_exists:
                self.datastores[datastore_name] = ds_path
            else:
                logging.error('REPLACE ERROR! No datastore with that name')
                return False

        try:
            with open(ds_path, 'wb') as ds:
                pickle.dump(data, ds)
            return ds_path
        except:
            return False
    
    def add_to_datastore(self, *args, **kwargs):
        logging.error('CANNOT ADD TO A PICKLE FILE DATASTORE. USE REPLACE INSTEAD')
        raise NotImplementedError

    def read_data_store(self, datastore_name):
        '''
        >>>read_data_store('test')
        {'some': 'stuff'}
        '''
        ds_path = self.get_datastore_fullpath(datastore_name)
        if not datastore_name in self.datastores:
            if self.check_datastore_exists:
                self.datastores[datastore_name] = ds_path
            else:
                logging.error('READ ERROR! No datastore with that name')
        with open(ds_path, 'rb') as ds:
            try:
                return pickle.load(ds)
            except Exception: # can't just except EOFError because it doesn't inherit from BaseException
                return None

class CSVWrangler(DataStoreWrangler, OSDataStore):
    datastore_extension = '.csv'
# =============================================================================
#     managed_datastore = ManagedCSV
# =============================================================================
    
    def __init__(self, *args, **kwargs):
        '''
        >>>CSVWrangler(location='./')
        '''
        super(CSVWrangler, self).__init__(*args, **kwargs)

    def create_datastore(self, datastore_name, *args, **kwargs):
        '''
        >>>create_datastore('dvds')
        True
        
        >>>create_datastore('dvds', header_row=['Title', 'Year'])
        True
        
        '''
        if datastore_name in self.datastores or self.check_datastore_exists(datastore_name):
            logging.error('CREATE ERROR! Datastore in self.datastores (%s) or datastore in location (%s)',
                          datastore_name in self.datastores, self.check_datastore_exists(datastore_name))
        ds_path = self.get_datastore_fullpath(datastore_name)
        
        try:
            with open(ds_path, 'x') as tab:
                if kwargs.get('header_row') and type(kwargs.get('header_row') == list):
                    csv.writer(tab).writerow(kwargs['header_row'])
            self.datastores[datastore_name] = ds_path
            return ds_path
        except:
            return False

    def replace_datastore(self, datastore_name, data):
        ds_path = self.get_datastore_fullpath(datastore_name)
        if not datastore_name in self.datastores:
            if self.check_datastore_exists:
                self.datastores[datastore_name] = ds_path
            else:
                logging.error('REPLACE ERROR! No datastore with that name')
                return False        
        try:
            with open(ds_path, 'w') as ds:
                for row in data:
                    csv.writer(ds).writerow(row)
            return ds_path
        except:
            return False

    def add_to_datastore(self, datastore_name, data):
        ds_path = self.get_datastore_fullpath(datastore_name)
        if not datastore_name in self.datastores:
            if self.check_datastore_exists:
                self.datastores[datastore_name] = ds_path
            else:
                logging.error('WRITE ERROR! No datastore with that name')
                return False        
        try:
            with open(ds_path, 'a') as ds:
                for row in data:
                    csv.writer(ds).writerow(row)
            return ds_path
        except:
            return False

    def read_data_store(self, datastore_name):
        '''
        >>>read_data_store('test')
        [['col1', 'col2'], ['1', '3'], ['6', '11']]
        '''
        ds_path = self.get_datastore_fullpath(datastore_name)
        if not datastore_name in self.datastores:
            if self.check_datastore_exists:
                self.datastores[datastore_name] = ds_path
            else:
                logging.error('READ ERROR! No datastore with that name')
        with open(ds_path, 'r') as ds:
            return [d for d in csv.reader(ds)]


#%% TESTING
# =============================================================================
# cw = CSVWrangler(location='/Users/chrislauney/temp/')
# pw = PickleFileWrangler(location='/Users/chrislauney/temp/')
# =============================================================================
