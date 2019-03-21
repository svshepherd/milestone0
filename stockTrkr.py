# -*- coding: utf-8 -*-
"""
exceptionally unambitious but nonetheless challenging attempt at a complete web app

created on Sun Mar 17 19:13:51 2019
@author: svshepherd
"""

from flask import Flask, render_template, request #redirect # http://flask.pocoo.org/docs/1.0/quickstart/
import requests as req # http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
from json import loads as parse
from datetime import datetime
from bokeh.plotting import figure 
from bokeh.embed import components

stockTrkr = Flask(__name__)

@stockTrkr.route('/', methods=['GET','POST'])
def inStock(): 
    if request.method == 'GET':
        return render_template('index.html', text='', bodyData='')
        
    elif request.method == 'POST':
        try :        
            stock = request.form['stock'].upper()
            # https://www.quandl.com/tools/api
            r = req.get('https://www.quandl.com/api/v3/datasets/WIKI/' + stock + '.json?order=asc&column_index=4')
            if r.status_code != 200:
                raise Exception(r.status_code)
    
            # data processing
            parsed_r = parse(r.text)['dataset']
            infoString = parsed_r['dataset_code'] + ' (' + parsed_r['database_code'] + str(parsed_r['database_id']) + '): ' + parsed_r['start_date'] + ' to ' + parsed_r['end_date']
            dat = parsed_r['data']
            # reorient lists
            days=[]
            eodValue=[]
            for dayRecord in dat :
                days.append(dayRecord[0])
                eodValue.append(dayRecord[1])
            day = [datetime.strptime(day,'%Y-%m-%d') for day in days]
            
            # display            
            p = figure(title=infoString, x_axis_label='date', x_axis_type='datetime')
            p.line(day,eodValue)
            js, html = components(p)

        except : # If the stock isn't valid, handle error by reseting the page
            stock = 'retry'
            js = ''
            html = traceback.print_exception()

        return render_template('index.html', bokehScript=js, text=stock, bodyData=html)
    
    else :
        print('i got all confused i''m sorry can we try again? please tell stephen')
        return render_template('index.html', bokehScript='', text='', bodyData='')
        
if __name__ == '__main__':
	stockTrkr.run(port=33507)
    #stockTrkr.run(debug=True)