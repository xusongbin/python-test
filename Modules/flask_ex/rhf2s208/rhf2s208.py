#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, render_template, request, abort

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
