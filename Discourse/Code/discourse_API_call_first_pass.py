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

def fetch_category_ids(names, exceptionNames):
    '''
    (list of str) => list of ints
    calls the discourse APIs. It returns a single list of all category ids in names, and all their subcategories.
    Take out exceptionNames (subcategories that we do not need, like 'OpenCare Research')
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
        if cat['name'] in names:
            cats.append(cat['id']) # adding the id of the specified category, like 'OpenCare'
            if cat['subcategory_ids']:
                for subcat in cat['subcategory_ids']:
                    subcatCall = 'https://edgeryders.eu/c/' + str(subcat) + '/show.json'
                    subcatResponse = requests.get(subcatCall)
                    subcatInfo = subcatResponse.json()
                    if subcatInfo['category']['name'] not in exceptionNames: # this takes care of the exceptions
                        cats.append(subcat) # adding the ids of all subcategories, like 'OpenInsulin' sub 'OpenCare'
                        
    print (str(len(cats)) + ' category ids retrieved.')           
    return cats
    
def fetch_topic_ids(categories):
    '''
    (list of ints) => list of ints
    calls the discourse APIs. It returns a single list of all topic ids in the categories we want.
    '''
    print ('Fetching topic ids..')
    tops = [] # the accumulator
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop

    for cat in categories:    
        while len(topicList) > 0:
            call = 'https://edgeryders.eu/c/' + str(cat) + '.json?page=' + str(i)
            response = requests.get(call)
            catTopics = response.json()
            topicList = catTopics['topic_list']['topics']
            for topic in topicList:
                tops.append(topic['id'])
            i +=1 
    
    print (str(len(tops)) + ' topic ids retrieved.')    
    return tops
    
def fetch_posts_in_topic(id):
    '''
    (int) => list of dicts
    calls the Discourse APis. Returns a list of dicts in topic id. Each dict contains raw data in one post.
    '''
    
    allPosts = [] # accumulator
    call = 'https://edgeryders.eu/t/' + str(id) + '.json?include_raw=1' # the field "raw" is handy for word count, but not included by default.
    response = requests.get(call)
    topic = response.json()
    for post in topic['post_stream']['posts']:
        thisPost = {} # this becomes the item in the allPosts list
        thisPost['post_id'] = post['id']
        thisPost['username'] = post['username']
        thisPost['user_id'] = post['user_id']
        thisPost['raw'] = post['raw']
        thisPost['post_number'] = post['post_number']
        thisPost['reply_to_post_number'] = post['reply_to_post_number']
        allPosts.append(thisPost)
    return allPosts
            
        
        
        
            
if __name__ == '__main__':
    # OpenCare = fetch_category_ids(['OpenCare'], ['OpenCare Research'])
    # print (OpenCare)
    # cc = fetch_posts([8])
    # print (cc)
    posts = fetch_posts_in_topic(6540)
    print (len(posts))
    print (posts [0])
