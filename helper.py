from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]

    num_messages = df.shape[0]
    words =[]
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    links =[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    x= df['user'].value_counts().head()
    df =round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'%'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    
    temp = df[df['user'] !='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words=[]
    for msg in temp['message']:
        words.extend(msg.split())

    wc= WordCloud(width=500, height=500, min_font_size=10 , background_color='black')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    temp = df[df['user'] !='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words=[]
    for msg in temp['message']:
        words.extend(msg.split())
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_util(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend([d for d in msg if d in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    
    timeline= df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] +"-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline 

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]

    daily_timeline= df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] ==  selected_user]
    return df['month'].value_counts()