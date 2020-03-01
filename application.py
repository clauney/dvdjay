#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 17:56:08 2020

@author: chrislauney
"""
import datetime
import sys

from flask import Flask, request, redirect, render_template

import datawrangler

#%% LOCAL / DEFAULT CONFIGS
cache_data_filename = 'dvdjay'
run_webapp = False



#%% SCHEMA-Y THINGS


attribute_defs = [
    {'id': 'name', 'name': 'Name', 'required': True, 'type': 'text'},
    {'id': 'year', 'name': 'Year', 'required': False, 'type': 'number'},
    {'id': 'genre', 'name': 'Genre', 'required': False, 'type': 'choice', 'multiple_allowed': True, 'additions_allowed': True,
         'choices': [
             'Action', 'Science Fiction', 'Superhero', 'Animated', 'Suspense', 'Drama'], },
    {'id': 'type', 'name': 'Type', 'required': False, 'type': 'choice', 'multiple_allowed': False, 'additions_allowed': False,
         'choices': [
             'Movie', 'TV Series', 'TV Miniseries'], },
    {'id': 'format', 'name': 'Format', 'required': False, 'type': 'choice', 'multiple_allowed': False, 'additions_allowed': False,
         'choices': [
             'DVD', 'Blu-Ray DVD', 'MP4'], },
    {'id': 'location', 'name': 'Location', 'required': True, 'type': 'choice', 'multiple_allowed': False, 'additions_allowed': False,
         'choices': [
             'Meteor Room DVD Cabinet', 'Heather\'s iMac', 'Meteor Room DVD Folio'], },
    ]

att_ui_stuff = {
    'name': {'example_text': 'e.g., Tron Legacy'},
    '': {},
    }

# =============================================================================
# attribute_rules = { 
#     'genre': {'multiple_allowed': True, 'additions_allowed': True, 'choices': [
#         'Action', 'Science Fiction', 'Superhero', 'Animated', 'Suspense', 'Drama']},
#     'type': {'multiple_allowed': False, 'additions_allowed': False, 'choices': [
#         'Movie', 'TV Series', 'TV Miniseries']},
#     'format': {'multiple_allowed': False, 'additions_allowed': False, 'choices': [
#         'DVD', 'Blu-Ray DVD', 'MP4']},
#     'location': {'multiple_allowed': False, 'additions_allowed': False, 'choices': [
#         'Meteor Room DVD Cabinet', 'Heather\'s iMac', 'Meteor Room DVD Folio']},
#     }
# =============================================================================

attribute_dict = {d.get('id'):{**d, **att_ui_stuff.get(d.get('id'), {})} for d in attribute_defs if d.get('id')}

multiple_allowed = [d.get('id') for d in attribute_defs if d.get('multiple_allowed')]

def refresh_movie_data():
    global current_show_data
    current_show_data = dw.read_data_store(cache_data_filename)

def add_movie(movie_dict):
    global current_show_data
    current_show_data.append(movie_dict)
    update_movie_cache()
    
def update_movie_cache():
    resp = dw.replace_datastore(cache_data_filename, current_show_data)
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
        {'type': 'Movie', 'name': 'Donnie Darko', 'year': '2001', 'genre': [], 'format': 'DVD'},
        {'type': 'Movie', 'name': 'Pearl Harbor', 'year': '2001', 'genre': [], },
        ]
    dw.replace_datastore(cache_data_filename, show_data_test)

current_show_data = dw.read_data_store(cache_data_filename)

#%% INIT FLASK ROUTES
app = Flask(__name__)

@app.route('/')
def index():
    return 'Python App Server'

@app.route('/dvdjay', methods=['GET', 'POST'])
def dvdjay():
    if request.method == 'GET':
        refresh_movie_data()
        return render_template('dvdjay.html',
                               att_defs=attribute_defs,
                               att_dict=attribute_dict,
                               shows=current_show_data,
                               )
    elif request.method == 'POST':
        print('FORM:', request.form)
        action = request.form.get('action')
        if action == 'new_show':
            pass
            new = {k:v for k, v in request.form.items() if v}
            for att in multiple_allowed:
                new[att] = request.form.getlist(att)
            # print('JUST THE FACTS:', new)
            add_movie(new)
        elif action == 'new_list_item':
            listname = request.form.get('list')
            additem = request.form.get('add_item')
            print('adding', additem, 'to list', listname)
            
        return redirect(request.referrer)
    


#%% GO TIME
    
if len(sys.argv) >= 2 and 'true' in sys.argv[1].lower():
    run_webapp = True

if __name__ == '__main__' and run_webapp:
    app.run(debug=True)

