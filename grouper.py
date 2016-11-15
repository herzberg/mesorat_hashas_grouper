import re
import networkx as nx


def main():
	filename = 'mesorat_hashas.csv'
	links = loadCsv(filename)
	links = standarizeLinks(links)
	links.sort()
	#print links?
	G = nx.Graph()
	G.add_edges_from(links)
	print("nodes:", G.number_of_nodes())
	print("edges:", G.number_of_edges())
	connected = nx.connected_components(G)
	allConnected = []
	for c in connected:
		allConnected.append(c)
	allConnected.sort(key = len, reverse=True)
	for c in allConnected:
		print(c)

### dividing and standarizing 
def dividePath(path):
	split = re.split(' ([0-9].*)',path)
	mesachta = split[0]
	end = None
	if('-' in split[1]):
		start, end = split[1].split('-')
	else:
		start = split[1]
	startDaf, startLine = start.split(':')
	if(end):
		if(':' in end):
			endDaf, endLine = end.split(':')
		else:
			endDaf = startDaf
			endLine = end
	else:
		endDaf, endLine = startDaf, startLine


	tup = (mesachta, (startDaf,int(startLine)), (endDaf, int(endLine)))
	return tup

def normalizeLinesToEveryX(pathTup, x): #this is a basc filter to match links that are basically the same.. it needs some work
	(mesachta, (startDaf,startLine), (endDaf, endLine))  = pathTup
	startLine = startLine - (startLine % x)
	endLine = endLine - (endLine % x)
	return (mesachta, (startDaf,startLine), (endDaf, endLine))

def removeEndFromSide(tup):
	(mesachta, (startDaf, startLine), (endDaf, endLine))	 = tup
	tup = (mesachta, startDaf, startLine)
	return tup

def standarizedSide(side):
	tup = dividePath(side)
	tup = normalizeLinesToEveryX(tup, 5)
	tup = removeEndFromSide(tup) #this makes B 21a:23-22a:44 into just B 21a:23
	return tup

def standarizeLinks(links):
	allLinks = []
	for link in links:
		link = [link[0], link[1]]
		link.sort()
		#print(link)
		tup = (standarizedSide(link[0]), standarizedSide(link[1]))
		#print(tup)
		allLinks.append(tup)
	return allLinks

def loadCsv(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	links = []
	for line in lines:
		split = line.split(',')
		links.append(split)
	return links

#############################



if __name__ == '__main__':
	main()