import socket


def isInternetAvailable():
  try:
    host = socket.gethostbyname('www.google.com')
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
def printAlert(alertType, dengerMess1, dengerMess2):
	#aType = 'alert-' + alertType
    print("<div class='alert alert-" + alertType + "' alert-dismissible' role='alert'>")
    print("<button type='button' class='close' data-dismiss='alert' aria-label='Close'>")
    print("<span aria-hidden='true'>")
    print("&times;")
    print("</span>")
    print("</button>")
    print('<strong>')
    print(dengerMess1)
    print('</strong>')
    print(dengerMess2);
    print('</div>')

def printPanel(panelType, headerTitle, title):
    print("<div class='panel panel-" +  panelType + "'>")
    print("<div class='panel-heading'>")
    print("<h3 class='panel-title' id='panel-title'>")
    print(headerTitle)
    print('<a class="anchorjs-link" href="#panel-title">')
    print('<span class="anchorjs-icon">')
    print('</span>')
    print('</a>')
    print('</h3>')
    print('</div>')
    print('<div class="panel-body">')
    print(title)
    print('</div>')
    print('</div>')

def printTD(text):
    print('<td>')
    print(text)
    print('</td>')

def printTH(text):
    print('<th>')
    print(text)
    print('</th>')

def printTableHeader(text):
    print('<div class="panel-heading">')
    print('<center>')
    print('<h1>')
    print(text)
    print('</h1>')
    print('</center>')
    print('</div>')

def printTrafficInfo(name, total_sent_bytes, persecond_sent_bytes, total_receive_bytes, persecond_receive_bytes, total_packet_send, persecond_packet_send, total_packet_receive, persecond_packet_receive):
       
        print('<div class="panel panel-default">')
        printTableHeader(name)
   
        print('<table class="table">')
        print('<tr>')
        printTH('#')
        printTH('Barcha')
        printTH('Sekundiga')
        print('</tr>')
        print('<tr>')
        printTH('Yuborilaytogan baytlar')
        printTD(total_sent_bytes)
        printTD(persecond_sent_bytes)
        print('</tr>')
	    
        print('<tr>')
        printTH('Qabul qilinayotgan baytlar')
        printTD(total_receive_bytes)
        printTD(persecond_receive_bytes)
        print('</tr>')
		
        print('<tr>')
        printTH('Yuborilayotgan paketlar')
        printTD(total_packet_send)
        printTD(persecond_packet_send)
        print('</tr>')
		
        print('<tr>')
        printTH('Qabul qilinaytogan paketlar')
        printTD(total_packet_receive)
        printTD(persecond_packet_receive)
        print('</tr>')
		
        print('</table>')
        print('</div>')