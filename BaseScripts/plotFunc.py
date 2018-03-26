# -*- coding: utf-8 -*-
"""Plotting Functions"""

import plotly.plotly as py
from plotly.graph_objs import *
from Database.dbOperation import Database
from plotly.exceptions import PlotlyRequestError
from BaseScripts.secret_file import mapbox_access_token


def bar_state_univ(limit=20):
    """Bar Plot - States with Most National Universities"""
    if limit not in list(range(1, 31)):
        print('Invalid Input')
        return

    db_operator = Database()
    result_list = db_operator.get_university_count(limit)

    data = [Bar(x=[result[0] for result in result_list],
                y=[result[1] for result in result_list],
                marker=dict(line=dict(color='rgb(0,0,0)',
                                      width=1.5)))]
    layout = Layout(xaxis=dict(tickangle=-45,
                               tickfont=dict(size=10)),
                    yaxis=dict(tickfont=dict(size=15)),
                    title='Top {} States with Most National Universities'.format(limit))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='barplot-state-univ')
    except PlotlyRequestError:
        print('Account limit reached')


def scatter_university_gdp(input_phrase='Total Endowment'):
    """Scatter Plot - Relationship between GDP & National University Amount"""
    input_range = ['Total Endowment (Million)', 'Average Endowment (Million)', 'Total Enrollment', 'Average Enrollment',
                   'Average Tuition in State', 'Average Tuition out of State', 'Average Median Starting Salary',
                   'Average Student Faculty Ratio', 'Average Female Percentage']
    if input_phrase not in input_range:
        input_phrase = 'Total Endowment'

    db_operator = Database()
    result_list = db_operator.get_university_gdp(additional_variable=input_phrase)

    if input_phrase == 'Average Student Faculty Ratio':
        text_format = '{0} ({1})<br>{2}: {3}:1'
    elif input_phrase == 'Average Female Percentage':
        text_format = '{0} ({1})<br>{2}: {3: 3.0%}'
    else:
        text_format = '{0} ({1})<br>{2}: {3}'
    text = [text_format.format(result[1], result[0], input_phrase, result[3]) for result in result_list]

    data = [Scatter(x=[result[2] for result in result_list],
                    y=[result[3] for result in result_list],
                    text=text,
                    marker=dict(sizeref=2. * max([result[4] for result in result_list]) / (100 ** 2),
                                size=[result[4] for result in result_list],
                                color=[result[4] for result in result_list],
                                colorscale='Viridis',
                                sizemode='area',
                                showscale=True,
                                colorbar=dict(title=input_phrase,
                                              titlefont=dict(size=15),
                                              tickfont=dict(size=15))),
                    mode='markers')]
    layout = Layout(xaxis=dict(tickfont=dict(size=15),
                               title='National University',
                               titlefont=dict(size=20)),
                    yaxis=dict(tickfont=dict(size=15),
                               title='GDP of State (Million $)',
                               titlefont=dict(size=20)),
                    title='Relationship between GDP & National University',
                    titlefont=dict(size=25))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='scatter-gdp-univ')
    except PlotlyRequestError:
        print('Account limit reached')


def scatter_public_private(x_axis='Enrollment', y_axis='MedianStartingSalary'):
    """Scatter Plot - Clustering of Private & Public University"""
    axis_range = ['FoundYear', 'Endowment(M)', 'TuitionAndFeesInState', 'TuitionAndFeesOutOfState', 'Enrollment',
                  'MedianStartingSalary', 'StudentFacultyRatio', 'FemalePercentage', 'Tuition Difference']
    if x_axis not in axis_range:
        x_axis = 'Enrollment'
    if y_axis not in axis_range:
        y_axis = 'MedianStartingSalary'

    db_operator = Database()
    result_list = db_operator.get_public_private(x_axis=x_axis, y_axis=y_axis)

    trace1 = Scatter(x=[result[0] for result in result_list if result[2] == 'Private'],
                     y=[result[1] for result in result_list if result[2] == 'Private'],
                     text=[result[3] for result in result_list if result[2] == 'Private'],
                     marker=dict(size=12,
                                 color='#258039'),
                     mode='markers',
                     name='Private')

    trace2 = Scatter(x=[result[0] for result in result_list if result[2] == 'Public'],
                     y=[result[1] for result in result_list if result[2] == 'Public'],
                     text=[result[3] for result in result_list if result[2] == 'Public'],
                     marker=dict(size=12,
                                 color='#F5BE41'),
                     mode='markers',
                     name='Public')

    data = [trace1, trace2]
    layout = Layout(xaxis=dict(tickfont=dict(size=15),
                               title=x_axis,
                               titlefont=dict(size=20)),
                    yaxis=dict(tickfont=dict(size=15),
                               title=y_axis,
                               titlefont=dict(size=20),
                               showline=True),
                    title='Clustering of Private & Public University',
                    titlefont=dict(size=25),
                    legend=dict(font=dict(size=20),
                                x=0.88,
                                y=0.97))
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='scatter-public-private')
    except PlotlyRequestError:
        print('Account limit reached')


def line_gdp(abbr_list):
    """Scatter Plot - GDP"""
    if len(abbr_list) > 10:
        print('Too Many States')
        return

    db_operator = Database()

    data = []
    for state_abbr in abbr_list:
        result = db_operator.get_state_gdp(state_abbr=state_abbr)

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
    db_operator = Database()
    result_list = db_operator.get_gps_data(state_abbr=state_abbr)

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


def histogram_difference_tuition():
    """Plot Histogram Showing Difference between In-State and Out-of-State Tuition and Fees of Public Universities"""
    db_operator = Database()
    result_list = db_operator.get_tuition_difference()

    data = [Bar(x=['0', '0 ~ 5,000', '5,000 ~ 10,000', '10,000 ~ 15,000', '15,000 ~ 20,000', '20,000 ~ 25,000',
                   '25,000 ~ 30,000', '> 30,000'],
                y=[len([result for result in result_list if result == 0]),
                   len([result for result in result_list if 0 < result <= 5000]),
                   len([result for result in result_list if 5000 < result <= 10000]),
                   len([result for result in result_list if 10000 < result <= 15000]),
                   len([result for result in result_list if 15000 < result <= 20000]),
                   len([result for result in result_list if 20000 < result <= 25000]),
                   len([result for result in result_list if 25000 < result <= 30000]),
                   len([result for result in result_list if result > 30000])],
                marker=dict(line=dict(color='rgb(0,0,0)',
                                      width=1.5)))]
    layout = Layout(xaxis=dict(tickfont=dict(size=15)),
                    yaxis=dict(tickfont=dict(size=15)),
                    title='Difference between In-State and Out-of-State Tuition and Fees of Public Universities')
    fig = Figure(data=data, layout=layout)

    try:
        py.plot(fig, filename='barplot-tuition-difference')
    except PlotlyRequestError:
        print('Account limit reached')


# scatter_public_private(x_axis='Tuition Difference', y_axis='StudentFacultyRatio')
# scatter_public_private()
# scatter_university_gdp()
# mapbox_univ('CA')
histogram_difference_tuition()
