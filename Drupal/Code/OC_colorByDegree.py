# Run from the stacked
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
  birthDate = graph.getIntegerProperty("birthDate")
  commDate = graph.getDoubleProperty("commDate")
  comment_id = graph.getStringProperty("comment_id")
  creation_date = graph.getStringProperty("creation_date")
  degree = graph.getDoubleProperty("degree")
  intimacy = graph.getDoubleProperty("intimacy")
  manager = graph.getBooleanProperty("manager")
  name = graph.getStringProperty("name")
  numComms = graph.getIntegerProperty("numComms")
  postDate = graph.getStringProperty("postDate")
  title = graph.getStringProperty("title")
  uid = graph.getStringProperty("uid")
  unixDate = graph.getDoubleProperty("unixDate")
  user_id = graph.getStringProperty("user_id")
  user_name = graph.getStringProperty("user_name")
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
  wordCount = graph.getDoubleProperty("wordCount")
  
  # compute degree
  params = tlp.getDefaultPluginParameters("Degree", graph)
  params['Type'] = 'In'
  params['metric'] = wordCount
  success = graph.applyDoubleAlgorithm('Degree', degree, params)
  # in the above, 'Degree' refers to the algorythm, degree to the property that stores the result
  
  #color code 
  params = tlp.getDefaultPluginParameters("Color Mapping", graph)
  params['colorScale'] = 'RedYellowGreenBlue.png'
  params['type'] = 'linear'
  params['input property'] = degree
  params ['override maximum value'] = True
  params ['maximum value'] = 20000
  params ['override minimum value'] = True
  params ['minimum value'] = 500
  success = graph.applyColorAlgorithm('Color Mapping', params)

