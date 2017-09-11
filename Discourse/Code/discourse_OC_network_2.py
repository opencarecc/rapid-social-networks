'''
Run this to build the graph on live data from the new discourse platform

Blocks:

=> Call a function in discourse_API_Edgeryders to read all topics in OpenCare, and their subcats. 
   Returns a list of dicts [{topic_id: category_id}]
=> Go through the items of the list. For all topics that are not in the Research subcat, 
   pass the id to a function to read all posts in that cat.
   => Process each post to instantiate an edge, creating the nodes as needed
'''

from tulip import *
import time
import datetime
import discourse_API_Edgeryders
start_script = datetime.datetime.now()

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

  # initialize custom properties
  user_name = graph.getStringProperty('user_name')
  user_id = graph.getIntegerProperty('user_id')
  creation_date = graph.getStringProperty('creation_date')
  wordCount = graph.getDoubleProperty('wordCount')
  post_id = graph.getIntegerProperty('post_id')
  category_id = graph.getIntegerProperty('category_id')
  
  tag = 'project-opencare'
  success = graph.setName(tag)
  involved = {}
  allPosts = {} # accumulator of the form {topic:[post0, post1...]}
  nodeMap = {}
  topics = discourse_API_Edgeryders.fetch_topics_from_tag(tag)
  for topic in topics:
      allPosts[topic] = []
      topicPosts = discourse_API_Edgeryders.fetch_posts_in_topic(topic)
      for post in topicPosts:
          allPosts[topic].append(post)  
          author = post['username']
          if author not in involved:
              involved[author] ={'username': author, 'user_id': post['user_id']}
  # build the network. Add nodes first 
  print 'Adding nodes...'
  for person in involved:
    n = graph.addNode()
    graph.setNodePropertiesValues(n, {'user_name': involved[person]['username'], 'user_id':involved[person]['user_id'] })
    nodeMap[person] = n
  # for edges, iterate on allPosts. Within each topic, each post is either a response the post stored in the 'reply_to_user' field.
  # if reply_to_post_number = null, the post is considered a reply to the first post in the topic.
  print 'Adding edges...'
  for topic in allPosts:
    threadPosts = allPosts[topic]
    for post in threadPosts: # this is a list, corresponding to 'posts-stream'
      if post['post_number'] == 1:
        topicStarter = post['username']
      else:
        source = nodeMap[post['username']]
        if post['reply_to_post_number'] == (1 or null):
          target = nodeMap[topicStarter]
          e = graph.addEdge(source, target)
          graph.setEdgePropertiesValues(e, {'wordCount':len(post['raw'].split())})