# Prettify. Run from the stacked.

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
	viewColor = graph.getColorProperty("viewColor")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewSize = graph.getSizeProperty("viewSize")
	birthDate = graph.getIntegerProperty("birthDate")
	commDate = graph.getDoubleProperty("commDate")
	comment_id = graph.getStringProperty("comment_id")
	creation_date = graph.getStringProperty("creation_date")
	intimacy = graph.getDoubleProperty("intimacy")
	manager = graph.getBooleanProperty("manager")
	name = graph.getStringProperty("name")
	numComms = graph.getIntegerProperty("numComms")
	postDate = graph.getStringProperty("postDate")
	title = graph.getStringProperty("title")
	uid = graph.getStringProperty("uid")
	unixDate = graph.getDoubleProperty("unixDate")
	user_name = graph.getStringProperty("user_name")
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewFont = graph.getStringProperty("viewFont")
	viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
	wordCount = graph.getDoubleProperty("wordCount")
	
	# apply the layout
	params = tlp.getDefaultPluginParameters("FM^3 (OGDF)", graph)
	params['Unit edge length'] = 100
	params['Page Format'] = 'Landscape'
	graph.applyLayoutAlgorithm('FM^3 (OGDF)', viewLayout, params)
	params = tlp.getDefaultPluginParameters("Curve edges", graph)
	graph.applyAlgorithm('Curve edges')
	
	# run degree and size map
	params = tlp.getDefaultPluginParameters("Degree", graph)
	params['type'] = 'InOut'
	params['result'] = viewMetric
	# save the degree in its own property. This is for scene setting
	degree = graph.getDoubleProperty('degree')
	for n in graph.getNodes():
		degree[n] = viewMetric[n]
	graph.applyDoubleAlgorithm('Degree', params)
	params = tlp.getDefaultPluginParameters("Size Mapping", graph)
	params['min size'] = 2 
	graph.applySizeAlgorithm('Size Mapping')
	
	# run Louvain and color code
	params = tlp.getDefaultPluginParameters("Louvain", graph)
	params['metric'] = viewMetric
	graph.applyDoubleAlgorithm('Louvain')
	params = tlp.getDefaultPluginParameters("Color Mapping", graph)
	params['colorScale'] = 'Paired_11_from_ColorBrewer,org.png'
	graph.applyColorAlgorithm('Color Mapping')
	
	# set labels 
	params = tlp.getDefaultPluginParameters("To labels", graph)
	params['input'] = user_name
	graph.applyStringAlgorithm('To labels', params)
	white = tlp.Color(255, 255, 255, 255)
	for n in graph.getNodes():
		viewLabelBorderWidth[n] = 0
		viewLabelColor[n] = white

	
