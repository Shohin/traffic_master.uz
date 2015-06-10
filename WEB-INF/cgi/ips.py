import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

import psutil
import utility as ut

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

print ('Content-type: text/html\n\n')
header = "header.html.tpl"
tpl_header = "".join(open(header,'r').readlines())
print(tpl_header)
nav = "nav.html.tpl"
tpl_nav = "".join(open(nav, 'r').readlines())
print (tpl_nav)
print ("<div class='container'>")

print('<div class="panel panel-default">')
ut.printTableHeader('IP addresslar')

print("<table class='table'>")

print('<tr>')

ut.printTH('Protokol')
ut.printTH('Lokal manzil')
ut.printTH('IP manzil')
ut.printTH('Status')
ut.printTH('PID')
ut.printTH('Dastur nomi')

print('</tr>')

proc_names = {}
for p in psutil.process_iter():
    try:
        proc_names[p.pid] = p.name()
    except psutil.Error:
        pass
for c in psutil.net_connections(kind='inet'):
    laddr = "%s:%s" % (c.laddr)
    raddr = ""
    if c.raddr:
        raddr = "%s:%s" % (c.raddr)
    print('<tr>')
	
    ut.printTD(proto_map[(c.family, c.type)])
    ut.printTD(laddr)
    ut.printTD(raddr)
    ut.printTD(c.status)
    ut.printTD(c.pid)
    ut.printTD(proc_names.get(c.pid, '?')[:15])

    print('</tr>')
	
	#print(templ % (proto_map[(c.family, c.type)],laddr,raddr or AD,c.status,c.pid or AD,proc_names.get(c.pid, '?')[:15],))

print('</table>')

print('</div>')

print ("</div>")
footer = "footer.html.tpl"
tpl_footer = "".join(open(footer,'r').readlines())
print(tpl_footer)