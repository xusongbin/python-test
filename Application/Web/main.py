#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
# from gpio import Led

app = Flask(__name__)
# led = Led()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['led'] == 'on':
            # led.set('ON')
            print('get web open the led')
        elif request.form['led'] == 'off':
            # led.set('OFF')
            print('get web close the led')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
