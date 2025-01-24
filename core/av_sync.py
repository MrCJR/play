import time


class AVSync:
    def __init__(self):
        # 初始化上一帧时间
        self.last_frame_time = time.time()

    def sync(self, frame):
        # 简单模拟音视频同步，这里只是控制帧率
        current_time = time.time()
        elapsed_time = current_time - self.last_frame_time
        # 假设帧率为 30fps
        frame_interval = 1 / 30
        if elapsed_time < frame_interval:
            time.sleep(frame_interval - elapsed_time)
        self.last_frame_time = current_time