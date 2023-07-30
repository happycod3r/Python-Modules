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
            
    def get_video_details(self, video_id):
        service = self.get_authenticated_service()

        try:
            request = service.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            video = response["items"][0]
            print(f"Title: {video['snippet']['title']}")
            print(f"Duration: {video['contentDetails']['duration']}")
            print(f"Views: {video['statistics']['viewCount']}")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")

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
