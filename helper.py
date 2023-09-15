from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
      # fetch num of messages
    num_messages = df.shape[0]
     # fetch num of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    #fetch the num of media messages
    num_media_msgs = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch links
    links = []
    for message in df ['message']:
        links.extend(extract.find_urls(message))

    return  num_messages, len(words),num_media_msgs, len(links)


def most_busy_users(df):

    x = df['user'].value_counts()
    df = (round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}))

    return x,df
   # name = x.index
   # count= x.values
   # plt.bar(name,count)

def create_wordcloud(selected_user , df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    wc =WordCloud(width=500,height=500,background_color='pink')
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user,df):
    f =  open ('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis =[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.emoji_count(c) > 0])


    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date').count()['message'].reset_index()
    return daily_timeline


def week_activity(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activiy_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period',
                                      values='message',aggfunc='count').fillna(0)


    return user_heatmap