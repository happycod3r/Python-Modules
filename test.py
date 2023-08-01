import youtube_api_tools

tube = youtube_api_tools.YouTubeAPIClientTools(
    "client_secret_671382908634-hudnrlsnhr3gqresomjga29a33s0chml.apps.googleusercontent.com.json", 
    ["https://www.googleapis.com/auth/youtube.readonly"]
)
rgr_id = "UCZiVfeN-xX_U-xDyDipTB-A"
tube.get_channel_info(rgr_id)
