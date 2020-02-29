#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 17:56:08 2020

@author: chrislauney
"""
import datetime

from flask import Flask, request, render_template

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


movie_data = [
    {'type': 'Movie', 'title': 'Donnie Darko', 'year': '2001', 'genre': [], 'format': 'DVD'},
    {'show_type': 'Movie', 'title': 'Pearl Harbor', 'year': '2001', 'genre': [], },
    ]




app = Flask(__name__)


@app.route('/')
def index():
    return 'Python App Server'

@app.route('/appinfo')
def appinfo():
    return render_template('appinfo.html')




if __name__ == '__main__':
    app.run(debug=True)

