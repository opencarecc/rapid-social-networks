'''
Run this to build the graph on live data from the new discourse platform
Starts from categories

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
  
  fest = graph.addSubGraph('festival')
  gcat = graph.getSubGraph(8)
  cat = 'workspaces/lote6' # change the cat to draw social networks of different cats
  specialUsers = {'Alberto': 0, 'Nadia': 0, 'Noemi': 0} # keeping track of special users, like community managers
  involved = {}
  allPosts = {} # accumulator of the form {topic:[post0, post1...]}
  numTopics = 0
  numContributions = 0
  words = 0
  nodeMap = {}
  topics = discourse_API_Edgeryders.fetch_topics_from_cat(cat)
  for topic in topics:
      numTopics += 1
      allPosts[topic] = []
      topicPosts = discourse_API_Edgeryders.fetch_posts_in_topic(topic)
      for post in topicPosts:
          numContributions += 1
          allPosts[topic].append(post)  
          words += len(post['raw'].split())
          author = post['username']
          if author in specialUsers:
            specialUsers[author] += 1
          if author not in involved:
              involved[author] ={'username': author, 'user_id': post['user_id']}
  print str(len(involved)) + ' unique participants in the festival convo'
              
  from_cat_graph = {} # build a map of already existing nodes, to keep track of who is who
  for n in graph.getNodes():
    name = user_name.getNodeStringValue(n)
    from_cat_graph[name] = n
  print str(len(from_cat_graph)) + ' nodes in the map'
    
  # build the network. Add nodes first 
  # if the node already exists, it is added only to the subgraph 
  counter1 = 0
  counter2 = 0
  for person in involved:
    if person in from_cat_graph:
      n = from_cat_graph[person]
      fest.addNode(n)
      nodeMap[person] = n
      counter1 += 1
    else:
      n = fest.addNode()
      graph.setNodePropertiesValues(n, {'user_name': involved[person]['username'], 'user_id':involved[person]['user_id'] })
      nodeMap[person] = n
      counter2 += 1
  print str(counter1) + ' nodes added from map'
  print str(counter2) + ' nodes added ex novo'
  # for edges, iterate on allPosts. Within each topic, each post is either a response the post stored in the 'reply_to_user' field.
  # if reply_to_post_number = null, the post is considered a reply to the first post in the topic.
  print 'Adding edges...'
  for topic in allPosts:
    threadPosts = allPosts[topic]
    for post in threadPosts: # this is a list, corresponding to 'posts-stream'
      if post['post_number'] == 1:
        topicStarter = post['username']
      source = nodeMap[post['username']]
      if 'reply_to_user' in post:
        target = nodeMap[post['reply_to_user']]
      else:
        target = nodeMap[topicStarter] # if no user was specified as target, we assume the comment is directed to the initiator of the thread
      e = fest.addEdge(source, target)
      graph.setEdgePropertiesValues(e, {'wordCount':len(post['raw'].split())})
  print 'Contributors: ' + str(len(involved))
  print 'Contributions: ' + str(numContributions) + ' in ' + str(numTopics) + ' topics, with ' + str(words/1000) + 'K words'
  print 
  print 'Adding nodes...'
  end_script = datetime.datetime.now()
  running_time = end_script - start_script
  print ('Executed in ' + str(running_time))        
   
