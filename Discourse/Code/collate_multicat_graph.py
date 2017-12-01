# Creates a subgraph with the stacked edges in each category. 
# This is the graph to visualize

from tulip import tlp

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
  name = graph.getStringProperty("name")
  numComms = graph.getIntegerProperty("numComms")
  postDate = graph.getStringProperty("postDate")
  uid = graph.getStringProperty("uid")
  unixDate = graph.getDoubleProperty("unixDate")
  viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
  birthDate = graph.getIntegerProperty("birthDate")
  category_id = graph.getIntegerProperty("category_id")
  commDate = graph.getDoubleProperty("commDate")
  creation_date = graph.getStringProperty("creation_date")
  intimacy = graph.getDoubleProperty("intimacy")
  manager = graph.getBooleanProperty("manager")
  post_id = graph.getIntegerProperty("post_id")
  user_id = graph.getIntegerProperty("user_id")
  user_name = graph.getStringProperty("user_name")
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
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
  
  graphNames = []
  for sg in graph.getSubGraphs():
    graphNames.append(sg.getName())
  print graphNames  
    
  aCS = graph.addSubGraph('all Cats Stacked')
  
  for name in graphNames:
    g = graph.getSubGraph(name).getSubGraph('stacked')
    for n in g.getNodes():
      aCS.addNode(n)
    for e in g.getEdges():
      aCS.addEdge(e)
    


