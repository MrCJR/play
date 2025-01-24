import subprocess
import cv2
import numpy as np


class VideoDecoder:
    def __init__(self, file_path):
        self.file_path = file_path
        # 使用 FFmpeg 进行解码
        self.command = ['ffmpeg', '-i', file_path, '-c:v', 'rawvideo', '-pix_fmt', 'bgr24', '-f', 'image2pipe', '-']
        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取视频的宽度和高度
        cap = cv2.VideoCapture(file_path)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

    def decode_frame(self):
        try:
            # 读取一帧数据
            raw_image = self.process.stdout.read(self.width * self.height * 3)
            if not raw_image:
                return None
            # 将数据转换为 numpy 数组
            image = np.frombuffer(raw_image, dtype=np.uint8)
            image = image.reshape((self.height, self.width, 3))
            return image
        except Exception as e:
            print(f"解码出错: {e}")
            return None