# -*- coding: utf-8 -*-
"""Common Functions Including Cache and Database"""

from __future__ import unicode_literals

from django.http import HttpResponse
from Database.dbOperation import Database
from BaseScripts.plotFunc import scatter_public_private
import json


def state_univ(request):
    """Return A JSON Containing National University Data."""
    state = request.GET['state']
    state_list = state.split(',')
    output = []
    db_operator = Database()
    for state_abbr in state_list:
        result_list = db_operator.get_state_univ(state_abbr=state_abbr)
        result_list = [dict(ID=result[0],
                            Name=result[1],
                            Ranking=result[2],
                            State=result[3],
                            City=result[4],
                            Type=result[5],
                            FoundYear=result[6],
                            Endowment=result[7],
                            TuitionAndFeesInState=result[8],
                            TuitionAndFeesOutOfState=result[9],
                            Enrollment=result[10],
                            MedianStartingSalary=result[11],
                            StudentFacultyRatio=result[12],
                            FemalePercentage=round(result[13] * 100, 1) if result[13] is not None else None
                            ) for result in result_list]
        output += result_list
    return HttpResponse(json.dumps(output))


def state_gdp(request):
    """Return A JSON Containing GDP Data."""
    state = request.GET['state']
    print()
    state_list = state.split(',')
    output = []
    db_operator = Database()
    for state_abbr in state_list:
        result = db_operator.get_state_gdp(state_abbr=state_abbr)
        result = dict(Name=result[0],
                      Y1997=result[1],
                      Y1998=result[2],
                      Y1999=result[3],
                      Y2000=result[4],
                      Y2001=result[5],
                      Y2002=result[6],
                      Y2003=result[7],
                      Y2004=result[8],
                      Y2005=result[9],
                      Y2006=result[10],
                      Y2007=result[11],
                      Y2008=result[12],
                      Y2009=result[13],
                      Y2010=result[14],
                      Y2011=result[15],
                      Y2012=result[16],
                      Y2013=result[17],
                      Y2014=result[18],
                      Y2015=result[19],
                      Y2016=result[20]
                      )
        output.append(result)
    print(json.dumps(output, indent=4))
    return HttpResponse(json.dumps(output))


def scatter_pp(request):
    """Plot"""
    cor = request.GET['cor']
    x_axis = cor.split(',')[0]
    y_axis = cor.split(',')[1]
    scatter_public_private(x_axis=x_axis, y_axis=y_axis)
    return HttpResponse("OK")
