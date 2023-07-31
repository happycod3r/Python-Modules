import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube3
import os

class YouTubeAPIClient:
    """
        A 'client_secret.json' file is needed in order for this class to be functional.
        Or should I say ... classy ....
        
        Required Python modules:
            google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client
                
        Keep in mind that you need to have the proper OAuth 2.0 authentication set up and the 
        permissions to manage playlists for an account. Below is a step-by-step guide on how to
        obtain a client_secret.json file. 
        
        Please also note that the steps for setting up OAuth 2.0 authentication and using the 
        client_secret.json file might change over time. For the latest and most detailed 
        instructions, you should refer to the official Google API documentation for the YouTube 
        API and OAuth 2.0 authentication for Python.
        
        1) Google Cloud Console:

            To use the YouTube API or any other Google API, you need to create a project on the 
            Google Cloud Console and enable the APIs you want to use.
            
        2) OAuth 2.0 Credentials:
        
            After creating the project and enabling the YouTube API, you need to create OAuth 2.0 
            credentials. These credentials are used to identify your application and to 
            authenticate and authorize access to the API. The credentials contain a client ID, 
            client secret, and other information.
                
        3) Download Client Secret:

            Once you create OAuth 2.0 credentials, you can download the client_secret.json file 
            from the Google Cloud Console. This file contains the client ID and client secret, 
            which are used in the authentication process.
            
        4) Authentication Flow:
        
            When you run your Python application that interacts with the YouTube API, it will 
            prompt the user to authenticate their Google account through a web browser (if necessary). 
            The client_secret.json file is used during this authentication flow to identify your 
            application and establish a secure connection.
            
        5) Access Tokens:

            After the user grants permission to your application, the authentication server provides 
            your application with an access token. This access token is used in API requests to 
            prove that your application has been granted permission to access the user's resources.

        6) Protecting Client Secret:
            
            The client_secret.json file contains sensitive information (client secret), so it should 
            be kept confidential and not shared or exposed publicly. It is important to store the 
            client_secret.json file securely on the server-side of your application.
            
        When you use the Google API Client Library for Python to interact with the YouTube API, you'll 
        need to set up the OAuth 2.0 authentication flow and provide the path to the client_secret.json 
        file in your code to initiate the authentication process.
        
    """
    def __init__(self) -> None:
        """
            Initializes the YouTubeAPIClient object.
        """
        self.youtube = youtube3.YoutubeClient("./client_secret_671382908634-hudnrlsnhr3gqresomjga29a33s0chml.apps.googleusercontent.com.json")

    #//////////// AUTHENTICATION ////////////
    
    def get_authenticated_service(self):
        """
            Sets up the OAuth 2.0 flow using the client_secret.json file. This method will 
            handle user authentication and token retrieval. The access token is used to authorize 
            API requests on behalf of the user.
        """
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("client_secret_671382908634-hudnrlsnhr3gqresomjga29a33s0chml.apps.googleusercontent.com.json", scopes)
        credentials = flow.run_local_server(port=8080)
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    #//////////// PLAYLISTS ////////////
    
    def search_playlists(self, query, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="playlist",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_user_playlists(self):
        """
            This method uses the playlists().list method to retrieve the user's playlists. 
            Using the 'mine=True' parameter indicates that we want to retrieve playlists belonging 
            to the authenticated user.
        """
        service = self.get_authenticated_service()
        try:
            request = service.playlists().list(
                part="snippet",
                mine=True,
                maxResults=10
            )
            response = request.execute()

            for playlist in response["items"]:
                print(playlist["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def create_playlist(self, title, description, privacy_status="public"):
        service = self.get_authenticated_service()
        try:
            request = service.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )
            response = request.execute()
            print(f"Playlist '{response['snippet']['title']}' created with ID: {response['id']}")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def delete_playlist(self, playlist_id):
        service = self.get_authenticated_service()

        try:
            service.playlists().delete(
                id=playlist_id
            ).execute()

            print(f"Playlist with ID {playlist_id} has been deleted.")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def add_video_to_playlist(self, playlist_id, video_id):
        service = self.get_authenticated_service()

        try:
            request = service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()

            print(f"Video '{video_id}' added to the playlist with ID: {response['snippet']['playlistId']}")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def remove_video_from_playlist(playlist_item_id):
        service = get_authenticated_service()

        try:
            service.playlistItems().delete(
                id=playlist_item_id
            ).execute()

            print(f"Video with ID {playlist_item_id} removed from the playlist.")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_my_playlists(self, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.playlists().list(
                part="snippet",
                mine=True,
                maxResults=max_results
            )
            response = request.execute()

            for playlist in response["items"]:
                print(playlist["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_playlist_items(self, playlist_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def update_playlist(self, playlist_id, title, description):
        service = self.get_authenticated_service()
        try:
            request = service.playlists().update(
                part="snippet",
                body={
                    "id": playlist_id,
                    "snippet": {
                        "title": title,
                        "description": description
                    }
                }
            )
            response = request.execute()
            print(f"Playlist '{response['snippet']['title']}' updated.")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    #//////////// VIDEOS ////////////
    
    def get_related_videos(self, video_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                relatedToVideoId=video_id,
                type="video",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def get_all_video_details(self, video_id):
        service = self.get_authenticated_service()

        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            print(f"Title: {video['snippet']['title']}")
            print(f"Channel: {video['snippet']['channelTitle']}")
            print(f"Published At: {video['snippet']['publishedAt']}")
            print(f"Duration: {video['contentDetails']['duration']}")
            print(f"Views: {video['statistics']['viewCount']}")
            print(f"Likes: {video['statistics']['likeCount']}")
            print(f"Dislikes: {video['statistics']['dislikeCount']}")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_video_title(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['snippet']['title']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def get_videos_channel_title(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['snippet']['channelTitle']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def get_video_published_at(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['snippet']['publishedAt']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def get_video_duration(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['contentDetails']['duration']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
       
    def get_video_view_count(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['statistics']['viewCount']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
      
    def get_video_like_count(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['statistics']['likeCount']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
      
    def get_video_dislike_count(self, video_id):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            return video['statistics']['dislikeCount']
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
       
    def get_video_categories(self, region_code="US"):
        service = self.get_authenticated_service()

        try:
            request = service.videoCategories().list(
                part="snippet",
                regionCode=region_code
            )
            response = request.execute()

            for item in response["items"]:
                print(f"{item['id']} - {item['snippet']['title']}")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    def get_videos_by_category(self, category_id, region_code="US", max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                videoCategoryId=category_id,
                regionCode=region_code,
                type="video",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_trending_videos(self, region_code="US", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_videos_by_tag(self, tag, region_code="US", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=tag,
                regionCode=region_code,
                type="video",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    def get_videos_by_language(self, language_code, region_code="US", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                regionCode=region_code,
                relevanceLanguage=language_code,
                type="video",
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    def search_videos(self, query, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")        

    def search_videos_by_order(self, query, order="relevance", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                order=order,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_category(self, query, category_id, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoCategoryId=category_id,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_definition(self, query, definition="any", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoDefinition=definition,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_duration(self, query, duration="any", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoDuration=duration,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")    

    def search_videos_by_license(self, query, license_type="any", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoLicense=license_type,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def search_videos_by_type(self, query, video_type="any", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type=video_type,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_embeddable_videos(self, query, embeddable="true", max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoEmbeddable=embeddable,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_location(self, query, location, location_radius, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                location=location,
                locationRadius=location_radius,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_language(self, query, language_code, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                relevanceLanguage=language_code,
                maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def search_videos_by_published_date(self, query, published_after, published_before, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                publishedAfter=published_after,
                publishedBefore=published_before,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    #//////////// CHANNELS ////////////

    def get_channel_info(self, channel_id):
        service = self.get_authenticated_service()

        try:
            request = service.channels().list(
                part="snippet,statistics",
                id=channel_id
            )
            response = request.execute()

            channel = response["items"][0]
            print(f"Channel Title: {channel['snippet']['title']}")
            print(f"Subscriber Count: {channel['statistics']['subscriberCount']}")
            print(f"Video Count: {channel['statistics']['videoCount']}")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_channel_videos(self, channel_id, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            maxResults=max_results
            )
            response = request.execute()
            for item in response["items"]:
                print(item["snippet"]["title"])
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_featured_channels(self, channel_id):
        service = self.get_authenticated_service()

        try:
            request = service.channels().list(
                part="snippet,brandingSettings",
                id=channel_id
            )
            response = request.execute()

            featured_channels = response["items"][0]["brandingSettings"]["channel"]["featuredChannelsUrls"]
            for channel_url in featured_channels:
                print(channel_url)

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_channel_sections(self, channel_id):
        service = self.get_authenticated_service()

        try:
            request = service.channelSections().list(
                part="snippet",
                channelId=channel_id
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"] )

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_channel_subscribers(self, channel_id):
        service = self.get_authenticated_service()

        try:
            request = service.channels().list(
                part="statistics",
                id=channel_id
            )
            response = request.execute()

            subscriber_count = response["items"][0]["statistics"]["subscriberCount"]
            print(f"Channel '{channel_id}' has {subscriber_count} subscribers.")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_channel_activity(self, channel_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.activities().list(
                part="snippet",
                channelId=channel_id,
                maxResults=max_results
            )
            response = request.execute()

            for activity in response["items"]:
                print(activity["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_channel_related_channels(self, channel_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.channels().list(
                part="snippet",
                relatedToChannelId=channel_id,
                type="channel",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def search_channels(self, query, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="channel",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    #//////////// COMMENTS ////////////
    
    def get_video_comments(self, video_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_comment_replies(self, comment_id, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.comments().list(
                part="snippet",
                parentId=comment_id,
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["textDisplay"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def post_video_comment(self, video_id, comment_text):
        service = self.get_authenticated_service()
        try:
            request = service.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": comment_text
                            }
                        }
                    }
                }
            )
            response = request.execute()

            print("Comment posted successfully!")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")    

    def reply_to_comment(self, parent_comment_id, reply_text):
        service = self.get_authenticated_service()
        try:
            request = service.comments().insert(
                part="snippet",
                body={
                    "snippet": {
                        "parentId": parent_comment_id,
                        "textOriginal": reply_text
                    }
                }
            )
            response = request.execute()

            print("Reply posted successfully!")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def update_comment(self, comment_id, updated_text):
        service = self.get_authenticated_service()
        try:
            request = service.comments().update(
                part="snippet",
                body={
                    "id": comment_id,
                    "snippet": {
                        "textOriginal": updated_text
                    }
                }
            )
            response = request.execute()

            print("Comment updated successfully!")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def delete_comment(self, comment_id):
        service = self.get_authenticated_service()
        try:
            service.comments().delete(
                id=comment_id
            ).execute()

            print("Comment deleted successfully!")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    #//////////// LIVE BROADCASTS/STREAMING ///////////

    def get_live_streams(self, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.liveStreams().list(
                part="snippet",
                maxResults=max_results
            )
            response = request.execute()

            for stream in response["items"]:
                print(stream["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_live_broadcasts(self, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.liveBroadcasts().list(
                part="snippet",
                maxResults=max_results
            )
            response = request.execute()

            for broadcast in response["items"]:
                print(broadcast["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def search_live_broadcasts(self, query, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                eventType="live",
                maxResults=max_results
            )
            response = request.execute()

            for item in response["items"]:
                print(item["snippet"]["title"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
      
    def get_live_chat_messages(self, live_chat_id, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="snippet",
                maxResults=max_results
            )
            response = request.execute()

            for message in response["items"]:
                print(message["snippet"]["displayMessage"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    def get_live_chat_moderators(self, live_chat_id, max_results=10):
        service = self.get_authenticated_service()
        try:
            request = service.liveChatModerators().list(
                liveChatId=live_chat_id,
                part="snippet",
                maxResults=max_results
            )
            response = request.execute()

            for moderator in response["items"]:
                print(moderator["snippet"]["moderatorDetails"]["displayName"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
     
    def get_live_chat_bans(self, live_chat_id, max_results=10):
        service = self.get_authenticated_service()

        try:
            request = service.liveChatBans().list(
                liveChatId=live_chat_id,
                part="snippet",
                maxResults=max_results
            )
            response = request.execute()

            for ban in response["items"]:
                print(ban["snippet"]["bannedUserDetails"]["displayName"])

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def insert_live_chat_message(self, live_chat_id, message_text):
        service = self.get_authenticated_service()
        try:
            request = service.liveChatMessages().insert(
                part="snippet",
                body={
                    "snippet": {
                        "liveChatId": live_chat_id,
                        "type": "textMessageEvent",
                        "textMessageDetails": {
                            "messageText": message_text
                        }
                    }
                }
            )
            response = request.execute()

            print("Live chat message sent successfully!")

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_all_live_chat_details(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _details = (
                chat['liveChatId'], 
                chat['liveChatType'], 
                chat['title'], 
                chat['description'],
                chat['isModerated'], 
                chat['scheduledStartTime'], 
                status['actualStartTime'],
                status['lifeCycleStatus'], 
                status['activeLiveChatId'], 
                status['concurrentViewers'],
                status['activeParticipants']
            )
            return _details
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            
    def get_live_chat_id(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _id = chat['liveChatId']
            return _id
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_type(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _type = chat['liveChatType']
            return _type
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_title(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _title = chat['title']
            return _title
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_description(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _description = chat['description']
            return _description
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def is_live_chat_moderated(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _is_moderated = chat['isModerated']
            return _is_moderated
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_live_chat_scheduled_start_time(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _description = chat['scheduledStartTime']
            return _description
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_actual_start_time(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _actual_start_time = status['actualStartTime']
            return _actual_start_time
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_life_cycle_status(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _life_cycle_status = status['lifeCycleStatus']
            return _life_cycle_status
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_active_live_chat_id(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _active_chat_id = status['activeLiveChatId']
            return _active_chat_id
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
    
    def get_live_chat_concurrent_viewers(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _concurrent_viewers = status['concurrentViewers']
            return _concurrent_viewers
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    def get_live_chat_active_participants(self, live_chat_id):
        service = self.get_authenticated_service()
        try:
            request = service.liveChat().list(
                id=live_chat_id,
                part="snippet,id,status,snippet.type,status.activeLiveChatId,status.actualStartTime,status.scheduledStartTime,status.concurrentViewers,status.activeParticipants,snippet.liveChatId,snippet.liveChatType,snippet.title,snippet.description,snippet.isModerated,snippet.scheduledStartTime,snippet.actualStartTime"
            )
            response = request.execute()
            chat = response["items"][0]["snippet"]
            status = response["items"][0]["status"]
            _active_participants = status['activeParticipants']
            return _active_participants
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

    
    
    
    