# -*- coding: utf-8 -*-
"""Plotting Functions"""

import sqlite3
import plotly.plotly as py
from plotly.graph_objs import *
from commonFunc import db_name
from plotly.exceptions import PlotlyRequestError
from secret_file import mapbox_access_token


def bar_most_states(num=20):
    """Bar Plot - States with Most National Universities"""
    if num not in list(range(1, 31)):
        print('Invalid Input')
        return

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = '''SELECT StateName, COUNT(n.*) FROM National_University AS n 
                   JOIN State_Abbr AS s 
                       ON n.State = s.StateAbbr 
                   GROUP BY State 
                   ORDER BY COUNT(*) DESC 
                   LIMIT {}'''.format(num)
    cur.execute(statement)
    result_list = cur.fetchall()

    data = [Bar(x=[result[0] for result in result_list],
                y=[result[1] for result in result_list],
                marker=dict(line=dict(color='rgb(0,0,0)',
                                      width=1.5)))]
    layout = Layout(xaxis=dict(tickangle=-45,
                               tickfont=dict(size=10)),
                    title='Top {} States with Most National Universities'.format(num))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='barplot-state')
    except PlotlyRequestError:
        print('Account limit reached')


def scatter_gdp_univ():
    """Scatter Plot - Relationship between GDP & National University Amount"""
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = '''SELECT State, COUNT(ID), Y2016, SUM(Enrollment), SUM([Endowment(M)]) FROM National_University 
                   JOIN State_Abbr
                       ON State = StateAbbr
                   JOIN GDP_State
                       ON StateName = Area
                   GROUP BY State'''
    cur.execute(statement)
    result_list = cur.fetchall()

    data = [Scatter(y=[result[1] for result in result_list],
                    x=[result[2] for result in result_list],
                    text=[result[0] for result in result_list],
                    marker=dict(sizeref=2. * max([result[3] for result in result_list]) / (100 ** 2),
                                size=[result[3] for result in result_list],
                                color=[result[4] for result in result_list],
                                colorscale='Viridis',
                                sizemode='area',
                                showscale=True,
                                colorbar=dict(title='Endowment<br>(Million $)',
                                              titlefont=dict(size=15),
                                              tickfont=dict(size=15))),
                    mode='markers')]
    layout = Layout(yaxis=dict(tickfont=dict(size=15),
                               title='National Univerity',
                               titlefont=dict(size=20)),
                    xaxis=dict(tickfont=dict(size=15),
                               title='GDP of State',
                               titlefont=dict(size=20)),
                    title='Relationship between GDP & National University<br>( Circlr Size - Total Enrollment )',
                    titlefont=dict(size=25))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='scatter-gdp-univ')
    except PlotlyRequestError:
        print('Account limit reached')


def scatter_enroll_salary():
    """Scatter Plot - Clustering of Private & Public University"""
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = '''SELECT Enrollment, MedianStartingSalary, Type, Name FROM National_University'''
    cur.execute(statement)
    result_list = cur.fetchall()

    trace1 = Scatter(y=[result[1] for result in result_list if result[2] == 'Private'],
                     x=[result[0] for result in result_list if result[2] == 'Private'],
                     text=[result[3] for result in result_list if result[2] == 'Private'],
                     marker=dict(size=12,
                                 line=dict(width=2),
                                 color='rgb(128,208,87)'),
                     mode='markers',
                     name='Private')

    trace2 = Scatter(y=[result[1] for result in result_list if result[2] == 'Public'],
                     x=[result[0] for result in result_list if result[2] == 'Public'],
                     text=[result[3] for result in result_list if result[2] == 'Public'],
                     marker=dict(size=12,
                                 line=dict(width=2),
                                 color='rgb(125,212,249)'),
                     mode='markers',
                     name='Public')

    data = [trace1, trace2]
    layout = Layout(yaxis=dict(tickfont=dict(size=15),
                               title='Median Starting Salary',
                               titlefont=dict(size=20)),
                    xaxis=dict(tickfont=dict(size=15),
                               title='Enrollment',
                               titlefont=dict(size=20),
                               showline=True),
                    title='Clustering of Private & Public University',
                    titlefont=dict(size=25),
                    legend=dict(font=dict(size=20),
                                x=0.88,
                                y=0.97))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='scatter-enroll-salary')
    except PlotlyRequestError:
        print('Account limit reached')


def scatter_gdp(abbr_list):
    """Scatter Plot - GDP"""
    if len(abbr_list) > 10:
        print('Too Many States')
        return

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    data = []
    for state_abbr in abbr_list:
        statement = '''SELECT * FROM GDP_State 
                       JOIN State_Abbr
                           ON Area = StateName
                       WHERE StateAbbr = \'{}\''''.format(state_abbr)
        cur.execute(statement)
        result = cur.fetchone()

        if result is None:
            print('No Result')
            continue

        data.append(Scatter(x=list(range(1996, 2017)),
                            y=result[1:],
                            mode='lines+markers',
                            name=state_abbr))

    layout = Layout(xaxis=dict(tickfont=dict(size=15),
                               title='Year',
                               titlefont=dict(size=20)),
                    yaxis=dict(tickfont=dict(size=15),
                               title='GDP',
                               titlefont=dict(size=20)),
                    title='GDP')
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='scatter-gdp')
    except PlotlyRequestError:
        print('Account limit reached')


def get_axis_info(lat_list, lon_list):
    """Return Axis Setting Dictionary"""
    min_lat = float(sorted(lat_list, key=lambda x: float(x))[0])
    max_lat = float(sorted(lat_list, key=lambda x: float(x))[-1])
    min_lon = float(sorted(lon_list, key=lambda x: float(x))[0])
    max_lon = float(sorted(lon_list, key=lambda x: float(x))[-1])

    max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
    padding = max_range * .10

    axis_dict = dict(
        center_lat=(max_lat + min_lat) / 2,
        center_lon=(max_lon + min_lon) / 2,
        lat_axis=[min_lat - padding, max_lat + padding],
        lon_axis=[min_lon - padding, max_lon + padding]
    )

    return axis_dict


def mapbox_univ(state_abbr):
    """Plot National Universities on Map through Mapbox"""
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = '''SELECT Name, Latitude, Longitude FROM National_University
                   WHERE State = \'{}\''''.format(state_abbr)
    cur.execute(statement)
    result_list = cur.fetchall()

    lat_list = []
    lon_list = []
    name_list = []
    for result in result_list:
        if (result[1] is not None) and (result[2] is not None):
            lat_list.append(result[1])
            lon_list.append(result[2])
            name_list.append(result[0])

    axis_dict = get_axis_info(lat_list, lon_list)

    data = Data([Scattermapbox(name="National Universities",
                               lat=lat_list,
                               lon=lon_list,
                               text=name_list,
                               mode="markers",
                               marker=Marker(size=10))])
    layout = Layout(title="National Universities in " + state_abbr,
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(lat=axis_dict["center_lat"],
                                    lon=axis_dict["center_lon"]),
                        zoom=5,
                        pitch=0))
    fig = dict(data=data, layout=layout)

    try:
        py.plot(fig, filename='National Universities in ' + state_abbr)
    except PlotlyRequestError:
        print('Account limit reached')


scatter_enroll_salary()
# scatter_gdp_univ()
# mapbox_univ('MI')
