import os
import math
import datetime

import cv2


class FrameExtractor:
    """
    Class used for extracting frames from a video file.
    """

    def __init__(self, video_name: str):
        video_folder = os.path.join(os.getcwd(), "videos", video_name)
        self.video_path = os.path.join(video_folder, os.listdir(video_folder)[0])
        self.vid_cap = cv2.VideoCapture(self.video_path)
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS)) + 1

    def get_video_duration(self):
        duration = self.n_frames / self.fps
        print(f"Duration: {datetime.timedelta(seconds=duration)}")
        return duration

    def get_n_images(self, every_x_frame: float) -> int:
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(
            f"Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images."
        )
        return n_images

    def get_frame_every_x_sec(self, frame_every_x_sec: float) -> int:
        n_images = math.floor(self.n_frames / (frame_every_x_sec * self.fps))
        print(
            f"Extracting a frame every {frame_every_x_sec}s would result in {n_images} images."
        )
        return n_images

    def get_uniform_extract(self, n_images: int) -> int:
        t_delta = math.floor(self.n_frames / self.fps / n_images)
        print(f"Extracting a frame every {t_delta}s, resulting in {n_images} images.")
        return t_delta

    def extract_frames(
        self,
        extract_method: str,
        value: float,
        img_name: str,
        dest_name: str = None,
        img_ext=".png",
    ) -> None:
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_path)

        if dest_name is None:
            dest_name = os.getcwd()
        else:
            if not os.path.isdir(os.path.join("images", dest_name)):
                os.mkdir(os.path.join("images", dest_name))
                print(f"Created the following directory: {dest_name}")

        if extract_method == "frame-delta":
            interesting_frames = value
        elif extract_method == "t-uniform":
            interesting_frames = math.ceil(self.n_frames / value)
        elif extract_method == "t-delta":
            interesting_frames = value * self.fps

        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():
            success, image = self.vid_cap.read()

            if not success:
                break

            if frame_cnt % interesting_frames == 0:
                img_path = os.path.join(
                    "images",
                    dest_name,
                    "".join([img_name, "_", str(img_cnt), img_ext]),
                )
                cv2.imwrite(img_path, image)
                img_cnt += 1

            frame_cnt += 1

        self.vid_cap.release()
        cv2.destroyAllWindows()


# extract methods: 't-delta',' frame-delta' , 't-uniform'
FrameExtractor("tedtalk").extract_frames(
    extract_method="t-uniform", value=10, img_name="image", dest_name="tedtalk"
)
