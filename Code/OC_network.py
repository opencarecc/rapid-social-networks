# Run this to build the graph on live data

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
import requests
import datetime
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
	user_id = graph.getStringProperty('user_id')
	creation_date = graph.getStringProperty('creation_date')
	wordCount = graph.getDoubleProperty('wordCount')
	comment_id = graph.getStringProperty("comment_id")
	title = graph.getStringProperty('title')

	involved = {} # a map of user ids 
	nodeMap = {} # Ben's map trick

	# start by building a map of posts-to-authors based on post Id ('post_id')
	allPosts = {}
	postWords = 0
	checklistPosts = []
	response = requests.get('https://edgeryders.eu/opencare/content')
	posts = response.json()
	for item in posts['nodes']:
		author = item['node']['user_id']
		allPosts[item['node']['post_id']] = author
		if author not in involved:
			involved[author] = {'name': item['node'] ['user_name'], 'uid': item['node']['user_id']}
		nid = item['node']['post_id']
		if nid not in checklistPosts:
			checklistPosts.append(nid)
			fullText = item['node']['content']
			words = fullText.split()
			postWords += len(words)
	print ('posts: ' + str(len(allPosts)) + ', with ' + str(postWords/1000) + 'k words') 
			
	
	# same thing with comments, but with comment ID ('comment_id')
	allComments = {}	
	commentsWords = 0
	checklistComments = []		
	response = requests.get('https://edgeryders.eu/opencare/comments') # only comments give rise to an edge
	comments = response.json()
	for item in comments['nodes']:
		author = item['node']['user_id']
		allComments[item['node']['comment_id']] = author
		if author not in involved:
			involved[author] = {'name': item['node']['user_name'], 'uid': item['node']['user_id']}
		cid = item['node']['comment_id']
		if cid not in checklistComments:
			checklistComments.append(cid)
			fullText = item['node']['content']
			words = fullText.split()
			commentsWords += len(words)
		
	print ('comments: ' + str(len(allComments)) + ', with ' + str(commentsWords/1000) + 'K words')
	print ('users: ' + str(len(involved)))
	
	# count comments by Noemi, Nadia, Alberto

	teamComms = {'Noemi': 0, 'Nadia': 0, 'Alberto': 0}
	checklistTeam = []
	for person in teamComms: 
		for item in comments['nodes']:
			if item ['node']['user_name'] == person:
				if item ['node']['comment_id'] not in checklistTeam:
					teamComms [person] += 1
					checklistTeam.append(item ['node']['comment_id'])
		print ('comments by ' + person + ': ' + str (teamComms[person]))

	
	# add the nodes, starting from the 'involved' dictionary 
	for user in involved:
		n = graph.addNode()
		user_name [n] = involved[user]['name']
		user_id [n] = involved[user]['uid']
		nodeMap[involved[user]['uid']] = n # nodeMap maps from user ids to nodes
	
		
	# now we can determine source and target of each edge
	
	checkList = [] # MySQL returns several times the same comment. 
	# Making sure there is no double counting
	for item in comments['nodes']: 
		cid = item ['node']['comment_id'] 
		if cid not in checkList:
			checkList.append(cid) 
			source = nodeMap[item['node']['user_id']]
			pid = item['node']['parent_comment_id']
			nid = item['node']['post_id']

			if pid == '0' :
				target = nodeMap[allPosts[nid]]
				e = graph.addEdge(source, target)
				creation_date[e] = item ['node'] ['creation_date']
				wordCount[e] = len(item['node']['content'].split())
				user_name[e] = item['node']['user_name']
				comment_id [e] = cid
				title [e] = item['node']['title']
			else:
				try:
					parentCommentAuthor = allComments[pid]
					target = nodeMap[parentCommentAuthor]
					e = graph.addEdge(source, target)
					creation_date[e] = item ['node'] ['creation_date']
					wordCount[e] = len(item['node']['content'].split())
					user_name[e] = item['node']['user_name']
					comment_id [e] = cid
					title [e] = item['node']['title']

				except KeyError: # deleted comments etc.
					try:
						target = nodeMap[allPosts[nid]] # do as if pid == 0
						e = graph.addEdge(source, target)
						wordCount[e] = len(item['node']['content'].split())
						user_name[e] = item['node']['user_name']
						comment_id [e] = cid
						title [e] = item['node']['title']

						
					except KeyError: 
						pass

	end_script = datetime.datetime.now()
	running_time = end_script - start_script
	print ('Executed in ' + str(running_time))		
		
	    
