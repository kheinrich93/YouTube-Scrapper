import os
from pytube import YouTube


class VideoGrabber:
    """
    Class used to download video file from youtube.
    """

    def __init__(self, urls_path: str):
        with open(os.path.join(os.getcwd(), urls_path)) as f:
            self.urls = f.readlines()

    def download(self, folder_name):
        for url in self.urls:
            video = YouTube(url)

            # extract vids with low resolution
            vid_list = video.streams.filter(file_extension="mp4").get_by_resolution(
                "360p"
            )

            # save to tmp
            dest_path = os.path.join(os.getcwd(), "videos", folder_name)
            vid_list.download(output_path=dest_path)


VideoGrabber("youtube_urls.txt").download("tedtalk")
