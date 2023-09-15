import pandas  as pd
import re
import  streamlit as st
def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - '
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        'user_message': messages,
        'chat_dates': dates
    })
    df['chat'] = pd.to_datetime(df['chat_dates'], format='%d/%m/%y, %H:%M - ')
    # df.head()

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[2:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    s = pd.Series(df['user'])
# print(s)
    l = len(s)
    for i in range(l):
        if (s[i] == '~'):
            s[i] = 'Qurat'
    df['month'] = df['chat'].dt.month_name()
    df['month_num'] = df['chat'].dt.month
    df['hour'] = df['chat'].dt.hour
    df['minute'] = df['chat'].dt.minute
    df['year'] = df['chat'].dt.year
    df['date'] = df['chat'].dt.date
    df['date'] = df['chat'].dt.date
    df['day_name'] = df['chat'].dt.day_name()
    df.drop(columns=['chat'], inplace=True)

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+ "-" + str(00))
        elif hour == 0:
            period.append(str(00)+ "-" + str(hour+1))
        else:
            period.append(str(hour)+ "-" + str(hour+1))

    df['period']= period




    return df