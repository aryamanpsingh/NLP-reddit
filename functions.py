import pandas as pd
import requests
import json
import csv
import time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import marshal, types
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
#Store current date and time
now = datetime.datetime.now()


#Get time in UTC format
def get_utc(year,month,date):
    date = datetime.date(year,month,date)
    return int(time.mktime(date.timetuple()))

#Get data from pushshift server
def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    #print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

#Store collected data in a list and then to set
def collectSubData(subm, subStats):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"    
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    
    subData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    #subStats[sub_id] = subData
    return sub_id,subData

#Combines getpushiftdata and collectSubData
def get(query,after,before,sub,subStats):
    data = getPushshiftData(query, after, before, sub)
    # Will run until all posts have been gathered 
    # from the 'after' date up until before date
    while len(data) > 0:
        for submission in data:
            sub_id, stats = collectSubData(submission, subStats)
            subStats[sub_id] = stats
        # Calls getPushshiftData() with the created date of the last submission
        #print(len(data))
        #print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
        data = getPushshiftData(query, after, before, sub)
    
    #print(len(data))
    return subStats

#Get stats for month/week/year
def getWeek(query,sub,Stats):
    Stats = get(query,int(time.time()-days(7)),int(time.time()),sub,Stats)

def getMonth(query,sub,Stats):
    Stats = get(query,int(time.time()-days(30)),int(time.time()),sub,Stats)
                
def getYear(query,sub,Stats):
    Stats = get(query,int(time.time()-days(365)),int(time.time()),sub,Stats)

#Get polarity scores for each headline
def get_polscore(results,subStats):
    for post in subStats:
        pol_score = sia.polarity_scores(subStats[post][0][1])
        pol_score['headline'] = subStats[post][0][1]
        pol_score['date'] = subStats[post][0][5]
        results.append(pol_score)
        
#Divide headlines and scores by month
def getmonthly(daily_df):
    compound = [None]*12
    number = [None]*12
    m = [None]*12
    print(daily_df.shape)
    for i in range(1,13):
        m[i-1] = daily_df[(daily_df.date>(now - datetime.timedelta(days = 365-30*(i-1)))) & (daily_df.date<(now - datetime.timedelta(365-30*(i))))]
        compound[i-1] = m[i-1].mean()['compound']
        number[i-1] = m[i-1].count()['compound']
        
    return compound,number

#Get graphs for yearly stats
def year_graph(term,sub):
    now = datetime.datetime.now()
    dailyStats = {}
    dailyResults = []
    #print("Enter term to find trends for : ")
    #term = input()
    #print("Enter sub to look in : ")
    #sub = input()
    getYear(term,sub,dailyStats)
    get_polscore(dailyResults,dailyStats)
    daily_df = pd.DataFrame.from_records(dailyResults)
    print(daily_df)
    compound,number = getmonthly(daily_df)
    months = np.arange(len(compound))
    dfl = {'compound':compound, 'posts':number, 'month':months}
    df = pd.DataFrame(dfl)
    fig, axs = plt.subplots(ncols=2,figsize=(16,8))
    #print(df)
    #g = sns.FacetGrid(df, col="month")
    #g = (g.map(plt.scatter, "compound", "posts", edgecolor="w"))
    sns.barplot(months,number,ax = axs[0]).set_title('Number of posts / month')
    sns.barplot(months,compound,ax = axs[1]).set_title('Sentiment / month')
    path = "static/"+sub
    if (not os.path.isdir(path)):
        os.makedirs(path)
    path = path+"/"+term+".png"
    fig.savefig(path)
    return path
    fig.legend()

    
#Use Marshal to store binary code of each function in a text file

year_graph_data = marshal.dumps(year_graph.__code__)
get_year_data = marshal.dumps(getYear.__code__);
get_polscore_data = marshal.dumps(get_polscore.__code__);
get_monthly_data = marshal.dumps(getmonthly.__code__);
get_data = marshal.dumps(get.__code__);
get_pushshift_data = marshal.dumps(getPushshiftData.__code__);
collectSubData_data = marshal.dumps(collectSubData.__code__);
get_utc_data = marshal.dumps(get_utc.__code__);




year_graph_file = open('tmp/year_graph.txt', 'wb')
year_graph_file.write(year_graph_data)

get_year_file = open('tmp/get_year.txt', 'wb')
get_year_file.write(get_year_data)

get_polscore_file = open('tmp/get_polscore.txt', 'wb')
get_polscore_file.write(get_polscore_data)

get_monthly_file = open('tmp/get_monthly.txt', 'wb')
get_monthly_file.write(get_monthly_data)

get_file = open('tmp/get.txt', 'wb')
get_file.write(get_data)

get_pushshift_file = open('tmp/get_pushshift.txt', 'wb')
get_pushshift_file.write(get_pushshift_data)

collectSubData_file = open('tmp/collectSubData.txt', 'wb')
collectSubData_file.write(collectSubData_data)

get_utc_file = open('tmp/get_utc.txt', 'wb')
get_utc_file.write(get_utc_data)