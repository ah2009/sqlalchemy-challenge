# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

#%%
import json
import flask
from flask import Flask, jsonify

#%%create an engine for the "chinook.sqlite database
engine =create_engine('sqlite:///Resources/hawaii.sqlite')


#%%
app=Flask(__name__)

#%%
print('testing')
@app.route('/api/v1.0/precipitation')
def prcp():
    conn=engine.connect()
   
    one_year_from_latest_record = '2016-08-23'

    query=f'''
        Select
            date, 
            prcp
        From
            measurement
        Where 
            date>= '{one_year_from_latest_record}'
        Group by 
            date
    '''

# Save the query results as a Pandas DataFrame and set the index to the date column

    prcp_df=pd.read_sql(query,conn)
    prcp_df=prcp_df.set_index('date')
    prcp_df.sort_values('date')
    prcp_json=prcp_df.to_json()
    conn.close()
    return prcp_json
#%%
@app.route('/api/v1.0/stations')
def active_stations():
    
    conn = engine.connect()
    
    query = '''
    
        select
            station as station_code,
            count(*) as station_count
        from
            measurement
        group by station_code
        order by 
                station_count DESC
    '''
    active_stations_df=pd.read_sql(query,conn)
    active_stations_df.head(10)
    
    
    conn.close()
    
    return active_stations_json
#%%
@app.route('/api/v1.0/tobs')
def temp_tobs():
    
    conn = engine.connect()

    active_stations_df=pd.read_sql(query,conn)
    active_stations_df.head(10)
    active_stations_df.sort_values('station_count', ascending=False, inplace=True)
    most_active_station=active_stations_df ['station_code'].values[0]

    query = f'''
        SELECT *,
            avg (tobs) as "average temp", 
            min (tobs) as "min temp",
            max (tobs) as "max temp"

    FROM measurement
    where station = "{most_active_station}"

    '''
    temp_tobs_df=pd.read_sql(query,conn)
    temp_tobs_df
    
    conn.close()
    
    return temp_tobs_json
#%%

#%%
if __name__ == '__main__':
    app.run(debug=True)