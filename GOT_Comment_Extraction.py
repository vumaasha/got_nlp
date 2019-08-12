import praw
import json
import os
from tqdm import tqd

reddit = praw.Reddit(client_id='8CBZy8YsKou-sA',
                     client_secret='VjYHmSpWpeV9VE_8JCnxWdjjfOw',
                     user_agent='android:com.example.myredditapp:v1.2.3 (by /u/AshKay12)',
                     username='********', #Replace your Username and password
                     password='********')

subreddit = reddit.subreddit("gameofthrones")

def extract_comments_from_reddit():
    path = 'extracted_comments/'
    with open("got_reddit_links.json") as json_file:
        episodes = json.load(json_file)
        for episode in tqdm(episodes):
            # Loop through all the links
            for link in episode['links']:

                    # Check if not a episode link
                    if not "Inside Ep" in link:
                        id = episode['links'][link].split("/")
                        id = str(id[3])
                        if os.path.exists(path + id + '.json'):
                            # print("Comments for  " + id + " already exists")
                            continue
                        dataToDump = {}
                        dataToDump['episode_info'] = []
                        dataToDump['episode_info'].append({
                            'season': episode['season'],
                            'episode': episode['episode'],
                            'title': episode['title']
                        })


                        dataToDump['comments'] = []
                        submission = reddit.submission(id)
                        submission.comments.replace_more(limit=None)

                        for comment in submission.comments.list():
                            dataToDump['comments'].append({
                                'parentID': str(comment.parent()),
                                'commentID': str(comment.id),
                                'commentBody': str(comment.body)
                            })

                        with open(path + id+'.json', 'w') as dumpFile:
                            json.dump(dataToDump, dumpFile)

                        # print("comments for " + id + "retrieved")





if __name__ == '__main__':
    extract_comments_from_reddit()















