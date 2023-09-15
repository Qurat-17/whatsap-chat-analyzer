import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp-chat-analyzer")

uploaded_file= st.sidebar.file_uploader("choose a file")
if uploaded_file  is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
   # st.text(data)
    df = preprocessor.preprocess(data);
    st.subheader("Preprocessed Chat Data")

    st.dataframe(df)
    print(df)
        #st.table(df)
    #fetch unique users in group
    user_list = df['user'].unique().tolist()
   # user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics ")

        #Stats Area
        num_messages,words, num_media_msgs ,num_links = helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("shared messages")
            st.title(num_media_msgs)
        with col4:
            st.header("links shared")
            st.title(num_links)
            
        # monthly timeline
        st.title("monthly timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color ='brown')
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = ['green','yellow','pink','red','purple','brown','skyblue'])
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)


        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activiy_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = ['yellow','pink'])
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)

        st.title("weekly activity map")
        user_heatmap =helper.activity_heatmap(selected_user,df)
        fig, ax =plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        if selected_user == 'overall':
            st.title("most busy person")
            x ,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                c = ["red", "green", "yellow", "purple", "brown"]
                ax.bar(x.index, x.values,color= c)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title(' Most common words')
        most_common_df = helper.most_common_words(selected_user,df)
        fig , ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        #st.dataframe(most_common_df)    //data frame for most commonly used words

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1,col2 , col3 = st.columns(3)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            st.title(" emoji ")

            fig , ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct ='%0.2f')
            st.pyplot(fig)
        with col3:
            st.title("most frequent emoji ")
            #x = helper.emoji_helper(selected_user, df)
            fig, ax = plt.subplots()
            c=["red","green","yellow","purple","brown"]
            ax.bar(emoji_df[0].head(), emoji_df[1].head(),color=c)
            st.pyplot(fig)

