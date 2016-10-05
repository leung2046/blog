# coding=utf-8

import os

from flask import Flask
from flask import render_template
from flask import request

import sqlite3
import time

app = Flask(__name__)


@app.route('/')
def show_index():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute('select id, title from art')
	title_list = c.fetchall()
	print title_list
	return render_template('index.html', title_list = title_list)

@app.route('/admin')
def write_article():
	return render_template('write.html')

@app.route('/publish_article',methods=['POST'])
def publish_article():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute('create table if not exists art(title text, content text, time REAL, id INTEGER PRIMARY KEY autoincrement)')
	save_tuple = (
		request.form['title'], 
		request.form['content'], 
		time.time()
	)
	print save_tuple
	c.execute('insert into art(title, content, time) values(?, ?, ?)', save_tuple)
	conn.commit()
	return 'ok'

@app.route('/article/<article_id>/')
def show_article(article_id):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute('select title, time, content from art where id=%s' % article_id)
	article_data = c.fetchone()
	return render_template('article.html', title=article_data[0], time=article_data[1], content=article_data[2])

app.run()

