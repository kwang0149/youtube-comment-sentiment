labels = ['Neutral Sentiment','Positive Sentiment','Negative Sentiment','Insulting the Government or Public Aegncy','Insulting or Defaming Others','Threatening Others','Alluding to the Tribe, Religion, Race, and intergroup']
def predict(result,labels):
  indices = tf.math.top_k(result, k=2).indices.numpy()[0]
  # 'indices' now contains the indices of the top two maximum values
  index1 = indices[0]
  index2 = indices[1]
  index3 = index1
  if index1==2 and index2 == 1:
    index3 = index2
  result = []
  result.append(labels[index1])
  result.append(labels[index2])
  result.append(labels[index3])
  return result




def comment_data(youtube_link):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAKCGnFw_ZbCwAbUgrfEJvwZJ-EZ1NgZxI"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId= extract_video_id(youtube_link),
        maxResults=1000
    )
    response = request.execute()
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['textDisplay']
        ])
    df=pd.DataFrame(comments,columns=['author','published_at','updated_at','like_count','comment'])
    first_choice_sentiments = []
    second_choice_sentiments = []
    final_sentiments = []
    for comment in df['comment']:
      result = model.predict([comment])
      sentiment = predict(result,labels)
      first_choice_sentiments.append(sentiment[0])
      second_choice_sentiments.append(sentiment[1])
      final_sentiments.append(sentiment[2])
    df['first_choice_sentiment'] = first_choice_sentiments
    df['second_choice_sentiment'] = second_choice_sentiments
    df['final_sentiment'] = final_sentiments
    return df