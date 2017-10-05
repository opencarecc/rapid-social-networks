'''
In Discourse:

- All contributions are called 'posts', whether they start a thread or not.
- Forum threads are called 'topics'
- Topics belong to 'categories'.
- The response to a GET call on posts returns the id of the topic that the post belongs to.
- The same response also contain and indication of the parent post.
- The response to a GET call on topic returns the id of the category that the topic belongs to.

- a call of the kind https://discourse.example.com/t/{topic_id}.json returns the whole topic, with all its posts

'''

import requests
import time
import sys

def fetch_category_ids(name, exceptionNames = []):
    '''
    (str, list of str) => list of dicts
    calls the discourse APIs. It returns a list of all categories and their subcategories, in the form
    
    [ {category_id: 46; category_slug: "parentCategoryName/subcategoryName"}, ...]
    
    Take out exceptionNames (subcategories that we do not need, like 'OpenCare Research')
    Tests OK
    '''
    print ('Fetching category ids...')
    cats = [] # the accumulator 
    exceptCats = [] # the accumulator for the exceptions

    call = 'https://edgeryders.eu/categories.json'
    response = requests.get(call)
    allCats = response.json()
    catList = allCats['category_list']['categories'] # this is a list of dicts

    # now grab the categories themselves and their subcategories
    for cat in catList:
        if cat['name'] == name:
            catItem ={} # the element to append to the accumulator. It takes the form {category_id: slug}
            catItem['id'] = cat['id'] 
            catItem['slug'] = cat['slug']
            cats.append(catItem) # adding the dict of the specified category, like 'OpenCare'
            if cat['subcategory_ids']:
                for subcat in cat['subcategory_ids']:
                    catItem2 = {} # the element to append to the accumulator. This time it refers to the subcategory
                    subcatCall = 'https://edgeryders.eu/c/' + str(subcat) + '/show.json'
                    time.sleep(3)
                    subcatResponse = requests.get(subcatCall)
                    subcatInfo = subcatResponse.json()
                    if subcatInfo['category']['name'] not in exceptionNames: # this takes care of the exceptions
                        catItem2['id'] = subcat
                        catItem2['slug'] = cat['slug'] + '/' + subcatInfo['category']['slug']
                        cats.append(catItem2) # adding the ids of all subcategories, like 'OpenInsulin' sub 'OpenCare'
                        
    print (str(len(cats)) + ' category ids retrieved.')           
    return cats
    
def fetch_topics_from_cat(cat):
    '''
    (dict) => list of ints
    calls the discourse APIs. Accepts as an input the output of fetch_category_ids
    It returns a single list of all topic ids in the categories we want. 
    '''
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i) 
        print 'Reading posts: page ' + str(i)
        time.sleep(3)
        response = requests.get(call)
        catTopics = response.json()
        topicList = catTopics['topic_list']['topics']
        for topic in topicList:
            tops.append(topic['id'])
        # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
        # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break 
        i +=1     
    print (str(len(tops)) + ' topic ids retrieved.')    
    return tops
    
def fetch_topics_from_tag(tag):
    '''
    (str) => list of ints
    calls the discourse APIs. Accepts as an input a tag.
    It returns a single list of all topic ids in the categories we want.
    '''
    print ('Fetching topic ids..')
    tops = [] # the accumulator
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop   
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = 'https://edgeryders.eu/tags/' + str(tag) + '.json?page=' + str(i)
        time.sleep(1)
        response = requests.get(call)
        tagTopics = response.json()
        topicList = tagTopics['topic_list']['topics']
        for topic in topicList:
            tops.append(topic['id'])
            # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
            # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break
        i += 1
    print (str(len(tops)) + ' topics retrieved.')    
    return tops
    
def fetch_posts_in_topic(id):
    '''
    (int) => list of dicts
    calls the Discourse APis. Returns a list of dicts in topic id. Each dict contains raw data in one post.
    It also contains the usernames of the source and the target of each post.
    When the target is not specified, we assume it to be the person who authored the first post in the topic.
    '''
    allPosts = [] # accumulator
    pageCounter = 1
    postList = ['something'] # need this as a condition to start the while loop
    while len(postList) > 0:
      call = 'https://edgeryders.eu/t/' + str(id) + '.json?page=' + str(pageCounter) + '&include_raw=1' # the field "raw" is handy for word count, but not included by default.
      time.sleep(1)
      topic = requests.get(call).json()
      postList = topic['post_stream']['posts']
      print 'Reading ' + str(len(postList)) + ' posts from topic ' + str(id)
      for post in postList:
          if post['post_number'] == 1:
              topic_author = post['username'] 
      for post in postList:        
          thisPost = {} # this becomes the item in the allPosts list
          thisPost['post_id'] = post['id']       
          thisPost['username'] = post['username']
          thisPost['user_id'] = post['user_id']
          thisPost['created_at'] = post['created_at']
          thisPost['raw'] = post['raw']
          thisPost['post_number'] = post['post_number']        
          if post['reply_to_post_number'] == None:
              thisPost['reply_to_post_number'] = 1
              thisPost['target_username'] = topic_author
          else:
              thisPost['reply_to_post_number'] = post['reply_to_post_number']
              if 'reply_to_user' in post:
                thisPost['target_username'] = post['reply_to_user']['username']
              else:
                thisPost['target_username'] = topic_author              
          allPosts.append(thisPost)
                # before we move on, we use the "reply_to_post" reference, which refers to the in-topic post_number,
      # to add an "absolute" reference to the post_id of the parent post. Also add reference to the username of the author of the parent post.
      for item1 in allPosts:
           for item2 in allPosts:
               if item1['reply_to_post_number'] == item2['post_number']:
                   item1['reply_to_post_id'] = item2['post_id']
      if len(postList) < 20: # if we have fewer than 20 posts, there can be no other page in the topic. No point making an empty call to the APIs, so...
        break
      else:
        pageCounter += 1

    return allPosts
            
        
        
        
            
if __name__ == '__main__':
    greetings = 'Hello world'
    lf = [{'id': 8, 'slug': 'opencare'}]
    # oneTopic = fetch_posts_in_topic(8)
    # print oneTopic
##    oc = fetch_topic_ids(lf)
##    cc = fetch_topic_ids(openCare)
##    print len(cc)
##    print (cc)
    tops = fetch_topics_from_cat('docs/assembl')
    print tops
    moreTops = fetch_topics_from_tag('diy')
    print moreTops

