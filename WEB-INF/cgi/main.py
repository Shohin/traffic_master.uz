import socket
import utility as ut
#from __future__ import print_function
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import psutil

def main():

    print ('Content-type: text/html\n\n' )

    header = "header.html.tpl"
    tpl_header = "".join(open(header,'r').readlines())
    print(tpl_header)
    nav = "nav.html.tpl"
    tpl_nav = "".join(open(nav, 'r').readlines())
    print (tpl_nav)
    print ("<div class='container'>")
    if ut.isInternetAvailable():
        ut.printAlert('info', 'Internet mavjud!', '')#print('<h1>Internet mavjud emas!</h1>')#print("<meta http-equiv='refresh' content='0; url=http://localhost:8080/traffic_master.uz/cgi-bin/traffic.py' />")#tr.run
    else:
	    ut.printAlert('danger', 'Internet mavjud emas!', 'Internet sozlamalarini tekshirib ko`ring!')#print('<h1>Internet mavjud emas!</h1>')
	
    ut.printPanel('info','<strong>Sizning IP adresingiz:</strong>',socket.gethostbyname(socket.gethostname()))
    #run()
    print ("</div>")
    footer = "footer.html.tpl"
    tpl_footer = "".join(open(footer,'r').readlines())
    print(tpl_footer)




af_map = {
    #socket.AF_INET: 'IPv4',
    #socket.AF_INET6: 'IPv6',
    #psutil.AF_LINK: 'MAC',
}

duplex_map = {
    #psutil.NIC_DUPLEX_FULL: "full",
    #psutil.NIC_DUPLEX_HALF: "half",
    #psutil.NIC_DUPLEX_UNKNOWN: "?",
}


def run():
    stats = psutil.net_if_stats()
    for nic, addrs in psutil.net_if_addrs().items():
      print('<div class="panel panel-default">')
      ut.printTableHeader(nic + ' tarmog`ining xususiyatlari')
      print('<table class="table">')
      print('<tr>')
      ut.printTH('Tezligi')
      ut.printTH('Duplex')
      ut.printTH('MTU')
      ut.printTH('isUp')
      print('</tr>')
      print('<tr>')
      ut.printTD(stats[nic].speed)
      ut.printTD(duplex_map[stats[nic].duplex])
      ut.printTD(stats[nic].mtu)
      ut.printTD("yes" if stats[nic].isup else "no")
      print('</tr>')
      for addr in addrs:
            print('<tr>')
            print('<td>')
            print("    %-8s" % af_map.get(addr.family, addr.family), end="")
            print('</td>')
            ut.printTD(" address   : %s" % addr.address)
            ut.printTD("             broadcast : %s" % addr.broadcast)
            ut.printTD("             netmask   : %s" % addr.netmask)
            print('</tr>')
      print('</table>')
      print('</div>')

	
if __name__ == '__main__':
    main()
