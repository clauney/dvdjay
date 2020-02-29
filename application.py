#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 17:56:08 2020

@author: chrislauney
"""
import datetime
import sys

from flask import Flask, request, render_template

import datawrangler

#%% LOCAL / DEFAULT CONFIGS
cache_data_filename = 'dvdjay'
run_webapp = False



#%% SCHEMA-Y THINGS
attribute_defs = [
    {'id': 'name', 'name': 'Name', 'required': True, 'type': 'text'},
    {'id': 'year', 'name': 'Year', 'required': False, 'type': 'number'},
    {'id': 'genre', 'name': 'Genre', 'required': False, 'type': 'choice', 'multiple_allowed': True, 'choices': ['Action', 'Science Fiction', 'Superhero', 'Animated', 'Suspense', 'Drama'], 'additions_allowed': True},
    {'id': 'type', 'name': 'Type', 'required': False, 'type': 'choice', 'multiple_allowed': False, 'choices': ['Movie', 'TV Series', 'TV Miniseries'], 'additions_allowed': False},
    {'id': 'format', 'name': 'Format', 'required': False, 'type': 'choice', 'multiple_allowed': False, 'choices': ['DVD', 'Blu-Ray DVD', 'MP4'], 'additions_allowed': False},
    {'id': 'location', 'name': 'Location', 'required': True, 'type': 'choice', 'multiple_allowed': False, 'choices': ['Meteor Room DVD Cabinet', 'Heather\'s iMac', 'Meteor Room DVD Folio'], 'additions_allowed': False},
    ]

attribute_choices = {
    'genre': {'multiple_allowed': True, 'additions_allowed': True, 'choices': ['Action', 'Science Fiction', 'Superhero', 'Animated', 'Suspense', 'Drama']},
    'type': {'multiple_allowed': False, 'additions_allowed': False, 'choices': ['Movie', 'TV Series', 'TV Miniseries']},
    'format': {'multiple_allowed': False, 'additions_allowed': False, 'choices': ['DVD', 'Blu-Ray DVD', 'MP4']},
    'location': {'multiple_allowed': False, 'additions_allowed': False, 'choices': ['Meteor Room DVD Cabinet', 'Heather\'s iMac', 'Meteor Room DVD Folio']},
    }


def get_movie_data():
    return dw.read_data_store(cache_data_filename)

def post_movie_data(data):
    resp = dw.replace_datastore(cache_data_filename, data)
    if resp:
        return True
    else:
        return False


#%% INIT DATA BACKEND
dw = datawrangler.PickleFileWrangler(location='./')

if not dw.check_datastore_exists(cache_data_filename):
    dw.create_datastore(cache_data_filename)

show_data_existing = dw.read_data_store(cache_data_filename)

show_data = show_data_existing if show_data_existing else {}

if not show_data:
    show_data_test = [
        {'show_type': 'Movie', 'title': 'Donnie Darko', 'year': '2001', 'genre': [], 'format': 'DVD'},
        {'show_type': 'Movie', 'title': 'Pearl Harbor', 'year': '2001', 'genre': [], },
        ]
    dw.replace_datastore(cache_data_filename, show_data_test)

current_show_data = dw.read_data_store(cache_data_filename)

#%% INIT FLASK ROUTES
app = Flask(__name__)

@app.route('/')
def index():
    return 'Python App Server'

@app.route('/appinfo')
def appinfo():
    return render_template('appinfo.html')


#%% GO TIME
    
if len(sys.argv) >= 2 and 'true' in sys.argv[1].lower():
    run_webapp = True

if __name__ == '__main__' and run_webapp:
    app.run(debug=True)

