import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser
import chardet
import sys

mystrip = lambda linkstr: cuturl(linkstr.strip(' \t\n')).rstrip('/')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.linkslist = []
        self.basepage = ''

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
        # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined.
                if name == "href":
                    #print name, "=",value
                    value = mystrip(value) 
                    if len(value) == 0:
                        continue
                    if value[0] == '/':
                        #self.linkslist.append(self.basepage + value)
                        value = self.basepage + value
                    self.linkslist.append(value)

# Removes everything in the url after the first appearence of # or ?.
def cuturl(s):
    aux = urlparse(s)
    return aux.netloc+aux.path

# Gets the html of the current webpage. Basic encoding handling.
def gethtml(page):
    print 'Processing ',page
    try:
        response = urllib2.urlopen('http://' + page)
    except urllib2.URLError, e:
        raise SystemExit(str(e.reason))
    pagecharset = response.headers.getparam('charset')
    src = response.read()
    if pagecharset == None:
        aux = chardet.detect(src)
        pagecharset == aux['encoding']
        if pagecharset == None:
            pagecharset = 'UTF-8'

    return src.decode(pagecharset,'replace')
    #return src.decode(pagecharset)

# Reads input file. One link per line.
def readfile(weblist_file):
    with open(weblist_file,'r') as f:
        weblist = []
        for line in f:
            line = mystrip(line)
            weblist.append(line)

    return weblist

def getpageneighbours(weblist,linkslist):
    ret = []
    for l in linkslist:
        if l in weblist:
            ret.append(weblist.index(l))
            #print l
    return ret

# Generates directed graph with web pages' relations.
def generategraph(weblist):
    ret = []
    for i in range(len(weblist)):
        actualpage = weblist[i]
        html = gethtml(actualpage)
        parser = MyHTMLParser()
        parser.basepage = actualpage
        parser.feed(html)
        # Remove duplicates from the list
        parser.linkslist = list(set(parser.linkslist))
        # Remove self-references.
        try:
            parser.linkslist.remove(actualpage)
        except ValueError:
            pass

        neighb = getpageneighbours(weblist,parser.linkslist)
        ret.append(neighb)
        #print neighb
    return ret

# writes the directed graph. Vertices are numbered from 1 to npages. 
def writegraph(graph,graph_file):
    nlinks = 0
    for i in range(len(graph)):
        nlinks += len(graph[i])
    with open(graph_file,'w') as f:
        #f.write(str(len(graph))+'\n')
        #f.write(str(nlinks)+'\n')
		f.write(str(len(graph)) + ' ' + str(nlinks) + ' \n') 
		for i in range(len(graph)):
			for j in range(len(graph[i])):
				f.write(str(i+1) + ' ' + str(graph[i][j]+1) + '\n')

def hasduplicates(weblist):
    return len(weblist) != len(set(weblist))

if __name__ == '__main__':
	if len(sys.argv) == 3:
		# Get input and output files
		weblist_file = sys.argv[1].strip()
		graph_file = sys.argv[2].strip()

		# Read input file
		weblist = readfile(weblist_file)

		if hasduplicates(weblist):
			raise SystemExit('Input file has duplicated web pages')

		# Generate graph
		graph = generategraph(weblist)
        
		# Write output file
		writegraph(graph,graph_file)

		for i in range(len(graph)):
			print (i+1),weblist[i]
			print '[',
			for j in range(len(graph[i])):
				print str(graph[i][j]+1),
			print ']'

	else:
		print 'Usage: python webparser.py weblist.in graph.out'
