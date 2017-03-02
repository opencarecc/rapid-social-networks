# run this from the stacked graph
# drops Noemi, Nadia and Alberto and study endogenous conversation

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
	viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSize = graph.getSizeProperty("viewSize")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
	
	# initialize the property I need
	user_name = graph.getStringProperty('user_name')
	# create the subgraph and copy all nodes and edges in the stacked graph onto it
	noManagers = graph.addSubGraph('noManagers')	
	for n in graph.getNodes():
		noManagers.addNode(n)
	for e in graph.getEdges():
		noManagers.addEdge(e)
		
	for n2 in noManagers.getNodes():
		if user_name[n2] in ('Nadia', 'Noemi', 'Alberto'):
			noManagers.delNode(n2)
		
	# run the degree algorithm 
	params = tlp.getDefaultPluginParameters("Degree", noManagers)
	params['type'] = 'InOut'
	params['result'] = viewMetric
	noManagers.applyDoubleAlgorithm('Degree', params)
	
	for n3 in noManagers.getNodes():
		if viewMetric[n3] == 0:
			noManagers.delNode(n3)
	
	# computes size of giant component
	params = tlp.getDefaultPluginParameters('Connected Component', noManagers)
	noManagers.applyDoubleAlgorithm('Connected Component', params)
	
	numCC	= 0
	for n in noManagers.getNodes():
		if viewMetric[n] > numCC:
			numCC = viewMetric[n]
			
	sizeGC = 0	
	for i in range (20):
		thisCompSize = 0
		for n in noManagers.getNodes():
			if viewMetric[n] == i:
				thisCompSize += 1
		if thisCompSize > sizeGC:
			sizeGC = thisCompSize
		
	numNodes = graph.numberOfNodes()
	print ('Connected components: ' + str (numCC))
	print ('The giant component has ' + str(sizeGC) + ' nodes (' + str( 100 * sizeGC / float(numNodes)) + '% of total)')
	 
		
