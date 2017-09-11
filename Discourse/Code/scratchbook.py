import discourse_API_Edgeryders

topics = discourse_API_Edgeryders.fetch_topics_from_tag('citizen-science')
involved = {}
for topic in topics:
    topicPosts = discourse_API_Edgeryders.fetch_posts_in_topic(topic)
    for post in topicPosts:

        author = post['username']
        if author not in involved:
            involved[author] ={'username': author, 'user_id': post['user_id']}

print involved
print len(involved)
    