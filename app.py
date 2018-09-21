import os

import pandas as pd
import numpy as np
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import geopandas as gpd

from decimal import *

app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///db/airbnb.sqlite", echo=False)

@app.route("/")
def welcome():
    a = "<h1>These are the valid endpoints in this project</h1>"
    b = "<a href='http://127.0.0.1:5000/index'><h3>/index</h3></a>"
    c = "<a href='http://127.0.0.1:5000/listingsall'><h3>/listingsall</h3>"
    d = "<a href='http://127.0.0.1:5000/listings-json'><h3>/listings-json</h3>"
    e = "<a href='http://127.0.0.1:5000/coord-json'><h3>/coord-json</h3>"
    f = "<a href='http://127.0.0.1:5000/pie-json'><h3>/pie-json</h3>"
    g = "<a href='http://127.0.0.1:5000/map-geojson'><h3>/map-geojson</h3>"
    h = "<a href='http://127.0.0.1:5000/summary-json'><h3>/summary-json</h3>"
    i = "<a href='http://127.0.0.1:5000/maxprice-json'><h3>/maxprice-json</h3>"
    j = "<a href='http://127.0.0.1:5000/list-count-json'><h3>/list-count-json</h3>"
    k = "<a href='http://127.0.0.1:5000/bedroomprice-json'><h3>/bedroomprice-json</h3>"
    l = "<a href='http://127.0.0.1:5000/avail-json'><h3>/avail-json</h3>"

    return a+b+c+d+e+g+h+i+j+k+l

@app.route("/index")
def get_landing():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    coord_df = response_df[["longitude","latitude","price","picture_url","bedrooms"]]
    
    return_file = json.loads(coord_df.to_json(orient='records'))
    
    return render_template('index.html',data=return_file)

@app.route("/newbar")
def newbar():
    return render_template('newbar.html')


@app.route("/listingsall")
def listingsall():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    returnjson = json.loads(response_df.to_json(orient='records'))
    
    return render_template('listings.html',data=returnjson)

@app.route("/listings-json")
def listings_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    returnjson = json.loads(response_df.to_json(orient='records'))
    
    return jsonify(returnjson)

@app.route("/coord-json")
def coord_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    return_file = json.loads(response_df[["longitude","latitude","price"]].to_json(orient='records'))
    return jsonify(return_file)

@app.route("/pie-json")
def pie_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    return_file = json.loads(response_df[["neighbourhood","id"]].to_json(orient='records'))
    return jsonify(return_file)

# @app.route("/map-geojson")
# def get_mapdata():

#    #01 Read in data
#    path = "static/data/filtered_listings.csv"
#    data = pd.read_csv(path)
#    geodata =gpd.read_file('static/data/neighbourhoods.geojson')

#    #02 Create the summmary stats and add to JSON file
#    summarydata = data.groupby('neighbourhood').mean()
#    summarydata.reset_index(inplace = True )
#    geodata = pd.merge(geodata, summarydata, how = 'left', on = 'neighbourhood')

#    # 03 Convert back to Dictionary and JSONIFY
#    geodict = json.loads(geodata.to_json(na = 'null'))

#    #04 Render to site
#    return jsonify(geodict)

@app.route("/map-geojson")
def get_mapdata():

  #01 Read in data
  path = "static/data/filtered_listings.csv"
  data = pd.read_csv(path)
  geodata =gpd.read_file('static/data/neighbourhoods.geojson')
  #clean up neighbourgood names
  geodata['neighbourhood'].replace('Outer Richmond','Richmond District',inplace=True)
  geodata['neighbourhood'].replace('Inner Richmond','Richmond District',inplace=True)
  geodata['neighbourhood'].replace('West of Twin Peaks','Twin Peaks',inplace=True)

  #02 Create the summmary stats and add to JSON file
  summarydata = data.groupby('neighbourhood').mean()
  summarydata.reset_index(inplace = True )

  #clean up neighbourgood names
  summarydata['neighbourhood'].replace('Haight-Ashbury','Haight Ashbury',inplace=True)
  summarydata['neighbourhood'].replace('Mission District','Mission',inplace=True)
  summarydata['neighbourhood'].replace('SoMa','South of Market',inplace=True)
  summarydata['neighbourhood'].replace('Presidio Heights','Presidio Heights',inplace=True)
  summarydata['neighbourhood'].replace('Oceanview','Ocean View',inplace=True)
  summarydata['neighbourhood'].replace('The Castro','Castro/Upper Market',inplace=True)
  summarydata['neighbourhood'].replace('Sea Cliff','Seacliff',inplace=True)
  summarydata['neighbourhood'].replace('Downtown','Downtown/Civic Center',inplace=True)
  summarydata['neighbourhood'].replace('Western Addition/NOPA','Western Addition',inplace=True)
  summarydata['neighbourhood'].replace('Sea Cliff','Seacliff',inplace=True)

  geodata = pd.merge(geodata, summarydata, how = 'left', on = 'neighbourhood')

  # 03 Convert back to Dictionary and JSONIFY
  geodict = json.loads(geodata.to_json(na = 'null'))

  #04 Render to site
  return jsonify(geodict)


@app.route("/summary-json")
def get_summary():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    price_df = response_df[["property_type","price"]]

    grouped_df = price_df.groupby('property_type', as_index=False).price.agg(['min','mean','max'])
    #grouped_df['mean'] = grouped_df['mean'].map('{:,.2f}'.format)
    grouped_df.reset_index(inplace = True )
    return_file = json.loads(grouped_df.to_json(orient='index'))
    #print(type(return_file))  #it's a string
    return jsonify(return_file)
    
@app.route("/list-count-json")
def list_byarea():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    grouped_df = response_df.groupby('neighbourhood', as_index=False).price.agg(['count'])
    #grouped_df['mean'] = grouped_df['mean'].map('{:,.2f}'.format)
    grouped_df.reset_index(inplace = True )
    grouped_df = grouped_df.rename(columns={'count': 'value'})
    return_file = json.loads(grouped_df.to_json(orient='index'))
    #print(type(return_file))  #it's a string
    return jsonify(return_file)

@app.route("/maxprice-json")
def maxprice():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    new_df = response_df.groupby('neighbourhood', as_index=False).price.agg("max")
    new_df.reset_index(inplace = True )
    new_df = new_df.rename(columns={'price': 'value'})
    return_file = json.loads(new_df.to_json(orient='index'))
    #print(type(return_file))  #it's a string
    return jsonify(return_file)

@app.route("/bedroomprice-json")
def bedroomprice():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    new_df = response_df.groupby('bedrooms', as_index=False).price.agg("count")
    new_df.reset_index(inplace = True )
    new_df = new_df.rename(columns={'price': 'value'})
    return_file = json.loads(new_df.to_json(orient='index'))
    return jsonify(return_file)

@app.route("/avail-json")
def availability():
    #01 Read in data
    path = "static/data/calendar.csv"
    data = pd.read_csv(path, encoding="ISO-8859-1")

    grouped = data.groupby(['date','available']).count()
    grouped = grouped.drop(labels='price', axis=1)

    grouped = grouped.reset_index()
    grouped = grouped.rename(columns={'listing_id': 'count'})

    return_file = json.loads(grouped.to_json(orient='index'))
    return jsonify(return_file)

if __name__ == "__main__":
    app.run()