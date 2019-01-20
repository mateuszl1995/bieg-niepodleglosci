import urllib.request

opener = urllib.request.FancyURLopener({})
url = "http://cybermoon.pl/wiedza/wspolrzedne/wspolrzedne_polskich_miejscowosci_"
chars = ['a', 'b', 'c', 'cc', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'll',
         'm', 'n', 'o', 'p', 'r', 's', 'ss', 't', 'u', 'v', 'w', 'z',
         'zz', 'zzz']
contents = {}
for char in chars:
    print(char)
    f = opener.open(url + char + '.html')
    contents[char] = f.read()
    contents[char] = contents[char].decode("ISO-8859-2")
	
######################################################################

import os
path = './data/geolocations/'
for char in chars:
    with open(path + char + '.html', 'wb') as w:
        w.write(str.encode(contents[char], 'ISO-8859-2'))
		
######################################################################

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if self.state == 1 and tag == 'table':
            self.state = 2

    def handle_endtag(self, tag):
        if self.state == 2 and tag == 'table':
            self.state = 3
        elif self.state == 2 and tag == 'tr':
            pass#self.locations += '\r\n'

    def handle_data(self, data):
        if self.state == 0 and data == 'Ż':
            self.state = 1
        elif self.state == 2:
            self.locations += (data + ';')

parser = MyHTMLParser()
parser.locations = ''
for char in chars:
    print(char)
    html = contents[char]
    html = html.replace(' &deg;N&nbsp;&nbsp;', '').replace(' &deg;E', '')
    parser.state = 0
    parser.feed(html)