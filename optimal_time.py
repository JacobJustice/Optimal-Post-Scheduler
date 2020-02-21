import json
import praw

from datetime import datetime

with open('userinfo.json') as jsonfile:
    jsondata = json.load(jsonfile)
    client_id = jsondata['client_id']
    client_secret = jsondata['client_secret']
    user_agent = jsondata['user_agent']
    username = jsondata['username']
    password = jsondata['password']

reddit = praw.Reddit(client_id=client_id
                    ,client_secret=client_secret
                    ,user_agent=user_agent
                    ,username=username
                    ,password=password)

desired_subreddit = input("What subreddit would you like to check?  ")
many_posts = int(input("How many posts do you want to check?  "))

# make subreddit object and prepare to get the top 100 posts
subreddit = reddit.subreddit(desired_subreddit)
top_posts = subreddit.top('all', limit=many_posts)

print("Checking the top", many_posts,"posts of the month on ", desired_subreddit, "...")

#get top 1000 submissions
submissions = [submission for submission in top_posts]

print("Done getting posts")

print("Processing posts...")
days_hours = [[0 for h in range(0,24)] for d in range(0,7)]
for submission in submissions:
    # make datetime object
    dt = datetime.fromtimestamp(submission.created_utc)
    days_hours[dt.date().weekday()][dt.time().hour] += 1

weekdays = {
0:"Sunday",
1:"Monday",
2:"Tuesday",
3:"Wednesday",
4:"Thursday",
5:"Friday",
6:"Saturday"}

# (day, hour)
# 0-indexing
best_time = (0,0)
for i, day in enumerate(days_hours):
    print(weekdays[i], day)
    for j, hour in enumerate(day):
        if hour > days_hours[best_time[0]][best_time[1]]:
            best_time = (i,j)

print("The best time to post in r/pics is ", weekdays[best_time[0]], "around", best_time[1]+1)

