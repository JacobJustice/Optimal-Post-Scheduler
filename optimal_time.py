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
timeframe = input("For how long do you want to check? (hour, day, week, month, year, all)  ")

# make subreddit object and prepare to get the top posts
subreddit = reddit.subreddit(desired_subreddit)
top_posts = subreddit.top(timeframe, limit=many_posts)

print("Checking the top", many_posts,"posts of the " + timeframe + " on r/" + desired_subreddit, "...")

#get top submissions
submissions = [submission for submission in top_posts]

weekdays = [
"Sunday",
"Monday",
"Tuesday",
"Wednesday",
"Thursday",
"Friday",
"Saturday"]
print("Done getting posts")

print("Processing posts...")
days_hours = [[0 for h in range(0,24)] for d in range(0,7)]
list_of_days = []
list_of_hours = []
for submission in submissions:
    # make datetime object
    dt = datetime.fromtimestamp(submission.created_utc)
    weekday = dt.date().weekday()
    hour = dt.time().hour
    list_of_days.append(weekday)
    list_of_hours.append(hour)
    days_hours[weekday][hour] += 1



# (day, hour)
# 0-indexing
best_time = (0,0)
for i, day in enumerate(days_hours):
    print(weekdays[i], day)
    for j, hour in enumerate(day):
        if hour > days_hours[best_time[0]][best_time[1]]:
            best_time = (i,j)


print("The best time to post in r/"+ desired_subreddit, "is", weekdays[best_time[0]], "around", best_time[1]+1)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,4))
if timeframe != 'all':
    plt.title("Submission Time of Top " + str(len(submissions)) + " Submissions of the " + timeframe + " on r/" + desired_subreddit)
else:
    plt.title("Submission Time of Top " + str(len(submissions)) + " Submissions of all time on r/" + desired_subreddit)

plt.hist2d(list_of_hours, list_of_days, bins=[range(24),range(8)])

plt.colorbar().set_label('Number of top posts')

plt.xlabel('Hour of the day (24hr)')
plt.xticks(range(24), [x for x in range(1,25)])

#plt.ylabel('Day of the week', verticalalignment='center')
plt.yticks([y+.5 for y in range(7)],labels=[weekdays[y] for y in range(0,7)])

plt.show()

