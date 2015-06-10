import utility as ut

def main():

    print ('Content-type: text/html\n\n' )

    header = "header.html.tpl"
    tpl_header = "".join(open(header,'r').readlines())
    print(tpl_header)
    nav = "nav.html.tpl"
    tpl_nav = "".join(open(nav, 'r').readlines())
    print (tpl_nav)
    print ("<div class='container'>")
    ut.printPanel('info','<strong>Dastur:</strong>','Dastur internetni boshqarish uchun yaratilgan')
    ut.printPanel('info','<strong>Muallif:</strong>','Nazarov Uchqun')
    print ("</div>")
    footer = "footer.html.tpl"
    tpl_footer = "".join(open(footer,'r').readlines())
    print(tpl_footer)
	
if __name__ == '__main__':
    main()