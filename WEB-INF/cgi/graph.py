#!/usr/bin/env python2
import cgi
import time
import sqlite3 as sql
import pygal 
def time_to_seconds(dt):
  a=dt.split()
  t=a[1]
  h, m, s = [int(i) for i in t.split(':')]
  return (h,m,s)

def main():
    print ('Content-type: text/html\n\n')
    print ('<link href="/stat/css/bootstrap.css" media="all" rel="stylesheet">')

    form = cgi.FieldStorage() 
    date_start = form.getvalue('start_date')
    date_end = form.getvalue('end_date')
    
    connec = sql.connect('traffic.db')
    cur = connec.cursor() 
 
    tm=[]
    ltm=[]
    val=[]
    #cur.execute("SELECT * FROM traffic WHERE timestamp >= '{}' AND  timestamp <= '{}'".format(date_start,date_end))
    cur.execute("SELECT * FROM traffic")
    rows = cur.fetchall()
    for row in rows:
        tm.append(50)
        val.append(20)
        print(row[1])
     
    tm.reverse()
    val.reverse()
    #start_val=val[0]
    for i in range(len(val)):
        val[i]=val[i]

    for i in tm:
        ti=time.strptime(i[11:18],'%H:%M:%S')
        i="{}:{}".format(ti[3],ti[4])
        ltm.append(i)


    line_chart = pygal.Line(width=1600)
    line_chart.title = 'Traffic usage at {}'.format(date_start)
    line_chart.x_labels = map(str, ltm)
    line_chart.add('', val)
    line_chart.render_to_file('stat.svg')


    print ("<html>")
    print (""" <body>
        <figure>
              <embed type="image/svg+xml" src="/stat/tmp/stat.svg" />
                  </figure>
                    </body>""")
    print ("</html>")
 
if __name__ == '__main__':
    main()
