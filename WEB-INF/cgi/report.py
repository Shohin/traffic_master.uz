#!/usr/bin/env python2
import operator
import cgi, cgitb
import time
import datetime
import sqlite3 as sql

import atexit
import sys
import psutil
import utility as ut

def run():

    form = cgi.FieldStorage() 
    date_start = form.getvalue('start_date')
    date_end = form.getvalue('end_date')
    
    print ('Content-type: text/html\n\n' )
    
    header = "header.html.tpl"
    tpl_header = "".join(open(header,'r').readlines())
    print (tpl_header)
	
    script_js = "script_js.html.tpl"
    tpl_script_js = "".join(open(script_js,'r').readlines())
    print (tpl_script_js)
	
    nav = "nav.html.tpl"
    tpl_nav = "".join(open(nav, 'r').readlines())
    print (tpl_nav)
    
    conn = sql.connect('traffic.db')
    cur = conn.cursor() 
    
    print ("<div class='container'>")
    ut.printPanel('primary', '<center><strong>Hisobot<strong></center>', date_start + ' dan ' + date_end + ' gacha')
    rows = cur.execute("SELECT * FROM traffic WHERE timestamp >= '{}' AND  timestamp <= '{}'".format(date_start,date_end))
    for row in rows:
        ut.printTrafficInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    print  ('</div>')
    footer = "footer.html.tpl"
    tpl_footer = "".join(open(footer,'r').readlines())
    print  (tpl_footer)
run()