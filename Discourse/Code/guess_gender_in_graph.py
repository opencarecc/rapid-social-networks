# -*- coding:utf-8 -*-
# creates a list of usernames and guesses their gender
# run from any graph


import gender_guesser.detector
dttr = gender_guesser.detector.Detector()
genders = {}


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
  birthDate = graph.getIntegerProperty("birthDate")
  category_id = graph.getIntegerProperty("category_id")
  commDate = graph.getDoubleProperty("commDate")
  creation_date = graph.getStringProperty("creation_date")
  intimacy = graph.getDoubleProperty("intimacy")
  manager = graph.getBooleanProperty("manager")
  name = graph.getStringProperty("name")
  numComms = graph.getIntegerProperty("numComms")
  postDate = graph.getStringProperty("postDate")
  post_id = graph.getIntegerProperty("post_id")
  uid = graph.getStringProperty("uid")
  unixDate = graph.getDoubleProperty("unixDate")
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

# the logic is simple
# I build a list of user names (one per line) (I iterated on the Tulip graph exported from graphryder)
# I go through the list and run gender°guesser
# you first need to deal with the fact that some user names contain spaces (as in Bridget McKenzie),
# or a period (as in silviad.ambrosio)
#
# you ask guesser to guess on all parts of the name
# you need to deal with situations where you'd get both male and female (happens twice on my data)

  for node in graph.getNodes():
    n = user_name[node].strip()
    while n != '':
  		if ' ' in n:
  			nns = n.split(' ', '_')
  			gns = []
  			for nn in nns:
  				gns.append(dttr.get_gender(nn))
  			print('Guessing from ', nns, ' = ', gns)
  			if 'male' in gns:
  				try:
  					genders['male'] += 1
  				except KeyError:
  					genders['male'] = 1
  
  				if 'female' in gns:
  					genders['male'] -= 1
  
  					try:
  						genders['hermaphrodite'] += 1
  					except KeyError:
  						genders['hermaphrodite'] = 1
  
  			elif 'female' in gns:
  
  				try:
  					genders['female'] += 1
  				except KeyError:
  					genders['female'] = 1
  
  			else:
  				try:
  					genders['unknown'] += 1
  				except KeyError:
  					genders['unknown'] = 1
  		elif '.' in n:
  			nns = n.split('.')
  			gns = []
  			for nn in nns:
  				gns.append(dttr.get_gender(nn))
  			print('Guessing from ', nns, ' = ', gns)
  			if 'male' in gns:
  				try:
  					genders['male'] += 1
  				except KeyError:
  					genders['male'] = 1
  
  				if 'female' in gns:
  					genders['male'] -= 1
  
  					try:
  						genders['hermaphrodite'] += 1
  					except KeyError:
  						genders['hermaphrodite'] = 1
  
  			elif 'female' in gns:
  				try:
  					genders['female'] += 1
  				except KeyError:
  					genders['female'] = 1
  
  			else:
  				try:
  					genders['unknown'] += 1
  				except KeyError:
  					genders['unknown'] = 1
  		else:
  			nns = [n]
  			gns = []
  			for nn in nns:
  				gns.append(dttr.get_gender(nn))
  			print('Guessing from ', nns, ' = ', gns)
  			if 'male' in gns:
  				try:
  					genders['male'] += 1
  				except KeyError:
  					genders['male'] = 1
  
  				if 'female' in gns:
  					genders['male'] -= 1
  
  					try:
  						genders['hermaphrodite'] += 1
  					except KeyError:
  						genders['hermaphrodite'] = 1
  
  			elif 'female' in gns:
  				try:
  					genders['female'] += 1
  				except KeyError:
  					genders['female'] = 1
  
  			else:
  				try:
  					genders['unknown'] += 1
  				except KeyError:
  					genders['unknown'] = 1
  print(genders)
  
