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
import discourse_API_Edgeryders as api
start_script = datetime.datetime.now()



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

  	# initialize custom properties
  	user_name = graph.getStringProperty('user_name')
  	user_id = graph.getIntegerProperty('user_id')
  	creation_date = graph.getStringProperty('creation_date')
  	wordCount = graph.getDoubleProperty('wordCount')
  	post_id = graph.getIntegerProperty('post_id')
  	category_id = graph.getIntegerProperty('category_id')
  	
  	success = graph.setName('all_ER_network')
    
    # initialize accumulators
  	involved = {} # a map of user ids 
  	nodeMap = {} # Ben's map trick. I use username as a reference, because of the way discourse APIs are made.
  	# start  by building a list of cats       
  	catList = []
  	topicsCounter = 0 # need this outside the main loop
  	allPosts = {} # we need a map of posts-to-authors based on post_id
  	words = 0
  	checklistPosts = [] 
  	# just in case the APIs return duplicates
  	# the following is to keep track of the comments by core team members
  	teamPosts = {'noemi': 0, 'nadia': 0, 'alberto': 0, 'johncoate': 0, 'matthias': 0}
  	checklistTeam = []   
    
    # get categories 
  	catList = api.fetch_top_level_categories()
  	print str (len(catList)) + ' top-level categories'
    
  	# iterate over categories, collecting topics and posts	
  	for cat in catList:
  		print '-------------------------------'
  		print 'Now fetching ' + cat
  		print '-------------------------------'
  	  	topics = api.fetch_topics_from_cat (cat)
  	  	posts = [] # the list containing all posts
  	  	for topic in topics:
  	  		topicsCounter += 1
  	  		topicPosts = api.fetch_posts_in_topic(topic)
  	  		time.sleep(.1)
  	  		for item in topicPosts:
  					post_id = item['post_id']
  					if post_id not in checklistPosts:
  						checklistPosts.append(post_id)
  						posts.append(item)
  						words += len(item['raw'].split())
  						author = item['username']
  						allPosts[item['post_id']] = author
  						if author not in involved:
  							involved[author] = {'username': author, 'user_id': item['user_id']}
  						for teamMember in teamPosts:
  							if author == teamMember:
  								teamPosts[teamMember] += 1
  		print ('topics: ' + str(topicsCounter))
  		print ('posts: ' + str(len(allPosts)) + ', with ' + str(words/1000.0) + 'K words') 
  		for person in teamPosts: 
  			print ('comments by ' + person + ': ' + str (teamPosts[person]))
	    
      ####  From here we build the network based on posts, a list of dictionaries

	print involved   
	print ('Adding nodes...')
	for user in involved:
		n = graph.addNode()
		user_name [n] = involved[user]['username']
		user_id [n] = involved[user]['user_id']
		nodeMap[involved[user]['username']] = n # nodeMap maps from user ids to nodes	
		
	# the source and target of each edge are already in the item referring to each post in posts
	
	checkList = [] # MySQL returns several times the same comment. 
	# Making sure there is no double counting
	for item in posts: 
		pid = item ['post_id'] 
		if pid not in checkList:
			checkList.append(pid) 
			source = nodeMap[item['username']]
			target = nodeMap[item['target_username']]
			e = graph.addEdge(source, target)
			creation_date[e] = item ['created_at']
			wordCount[e] = len(item['raw'].split())
			user_name[e] = item['username']
			try:
				post_id[e] = pid
			except TypeError:
				pass

	end_script = datetime.datetime.now()
	running_time = end_script - start_script
	print ('Executed in ' + str(running_time))		
		
	    
