import streamlit as st 
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Analyze your WhatsApp Chats')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    user_details = df['user'].unique().tolist()
    if 'Group Notification' in user_details:
        user_details.remove('Group Notification')
    
    user_details.sort()
    user_details.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show analysis w.r.t',user_details)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages ,num_links= helper.fetch_states(selected_user ,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['msg'],color = 'maroon') 
        plt.xticks(rotation = 90)
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['date'],daily_timeline['msg'],color = 'purple') 
        plt.xticks(rotation = 90)
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        active_month_df,month_list,month_msg_list,active_day_df,day_list,day_msg_list=helper.activity_map(selected_user,df)

        with col1:
            st.header("Most Active Month")
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'],active_month_df['msg'])
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))],max(month_msg_list),color='green',label='Highest')
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))],min(month_msg_list),color='red',label='Lowest')

            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most Active Day")
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'],active_day_df['msg'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))],max(day_msg_list),color='green',label='Highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))],min(day_msg_list),color='red',label='Lowest')

            plt.xticks(rotation=90)
            st.pyplot(fig)


        #most chatiest user
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x ,percent = helper.most_chaty(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color ='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(percent)

        
        #WordCloud
        st.title("Most Common Words")
        df_wc = helper.create_wordcloud(selected_user,df)

        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Used")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0])
            # ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f") #top 5 emojis with %
            st.pyplot(fig)
        