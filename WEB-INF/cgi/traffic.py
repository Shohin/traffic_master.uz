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


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)

def poll(interval):
    """Retrieve raw stats within an interval window."""
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    return (tot_before, tot_after, pnic_before, pnic_after)
	
def getTrafficInfo(tot_before, tot_after, pnic_before, pnic_after):
    
    printTotalTrafficInfo(bytes2human(tot_after.bytes_sent), bytes2human(tot_after.bytes_recv), tot_after.packets_sent, tot_after.packets_recv)

    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    for name_connection in nic_names:
        stats_before = pnic_before[name_connection]
        stats_after = pnic_after[name_connection]
        
        total_sent_bytes = bytes2human(stats_after.bytes_sent)
        persecond_sent_bytes = bytes2human(stats_after.bytes_sent - stats_before.bytes_sent)
        total_receive_bytes = bytes2human(stats_after.bytes_recv)
        persecond_receive_bytes = bytes2human(stats_after.bytes_recv - stats_before.bytes_recv)
        
        total_packet_send = stats_after.packets_sent
        persecond_packet_sent = stats_after.packets_sent - stats_before.packets_sent
		
        total_packet_receive = stats_after.packets_recv
        persecond_packet_receive = stats_after.packets_recv - stats_before.packets_recv
		
        connec = sql.connect('traffic.db')
        c = connec.cursor() 
        c.execute('''CREATE TABLE IF NOT EXISTS traffic (name_connection text, total_sent_bytes text, persecond_sent_bytes text, total_reseive_bytes text, persecond_reseive_bytes text, total_sent_packeges text, persecond_sent_packeges text, total_receive_packeges text, persecond_receive_packeges text, timestamp text)''')
        insertSQL(c, name_connection, total_sent_bytes, persecond_sent_bytes, total_receive_bytes, persecond_receive_bytes, total_packet_send, persecond_packet_sent, total_packet_receive, persecond_packet_receive, (time.strftime("%Y-%m-%d")))
        connec.commit();
        ut.printTrafficInfo(name_connection, total_sent_bytes, persecond_sent_bytes, total_receive_bytes, persecond_receive_bytes, total_packet_send, persecond_packet_sent, total_packet_receive, persecond_packet_receive)
		

def printTotalTrafficInfo(total_baytes_sent, total_baytes_receive, total_packet_sent, total_packet_receive):
    #total bytes
    print('<div class="panel panel-default">')
    ut.printTableHeader('Barcha baytlar')
   
    print('<table class="table">')
    
    print('<tr>')
    ut.printTH('Yuborilaytogan')
    ut.printTH('Qabul qilinaytogan')
    print('</tr>')
    print('<tr>')
    ut.printTD(total_baytes_sent)
    ut.printTD(total_baytes_receive)
    print('</tr>')
    
    print('</table>')
    print('</div>')
	
	#total packetes
    print('<div class="panel panel-default">')
    ut.printTableHeader('Barcha paketlar')
   
    print('<table class="table">')
    
    print('<tr>')
    ut.printTH('Yuborilaytogan')
    ut.printTH('Qabul qilinaytogan')    
    print('</tr>')
    print('<tr>')
    ut.printTD(total_packet_sent)
    ut.printTD(total_packet_receive)
	
    print('</tr>')
    print('</table>')
    print('</div>')
		


def runNetNop():
    try:
        interval = 0
        args = poll(interval)
        getTrafficInfo(*args)
        interval = 1
    except (KeyboardInterrupt, SystemExit):
        pass

def createDB():
    connec = sql.connect('traffic.db')
    c = connec.cursor() 
    c.execute('''CREATE TABLE IF NOT EXISTS traffic (name_connection text, total_sent_bytes text, persecond_sent_bytes text, total_reseive_bytes text, persecond_reseive_bytes text, total_sent_packeges text, persecond_sent_packeges text, total_receive_packeges text, persecond_receive_packeges text, timestamp text)''')
    return c
	
def insertSQL(cur, name_connection, total_sent_bytes, persecond_sent_bytes, total_reseive_bytes, persecond_reseive_bytes, total_sent_packeges, persecond_sent_packeges, total_receive_packeges, persecond_receive_packeges, timestamp):
    params = (name_connection, total_sent_bytes, persecond_sent_bytes, total_reseive_bytes, persecond_reseive_bytes, total_sent_packeges, persecond_sent_packeges, total_receive_packeges, persecond_receive_packeges, timestamp)
    cur.execute("INSERT INTO traffic VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

def run():
    date_start = (time.strftime("%Y-%m-%d"))
    date_end =(time.strftime("%Y-%m-%d"))

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
	
    print ("<div class='container'>")
    
    print('<div class="panel panel-default">')
    ut.printTableHeader('Hisobot olish')
	
    print('<table class="table">')
    print ("<form action='report.py' method='POST'>")
    print('<tr>')
    #ut.printTD('<b>Text ko`rinishda</b>')
    ut.printTD('<b>Dan: </b> <input name="start_date" size="32" type="date" id="datepicker" value="{}" >'.format(date_start))
    ut.printTD ('<b>Gacha: </b> <input name="end_date" size="32" type="date" id="datepicker" value="{}" >'.format(date_end))
    ut.printTD ("<button class='btn btn-primary'>Ro`yxatni olish</button>")
    print('</tr>')
    print ("</form>")
    #print ("<form action='graph.py' method='POST'>")
    #print('<tr>')
    #print('<th colspan="3">Grafik ko`rinishda</th>')
    #ut.printTD ("<button class='btn btn-primary'>Grafikni olish</button>")
    #print('</tr>')
    #print ("</form>")
    print('</table>')
    print('</div>')
    runNetNop()
    footer = "footer.html.tpl"
    tpl_footer = "".join(open(footer,'r').readlines())
    print  (tpl_footer)
run()