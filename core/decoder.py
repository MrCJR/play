import ffmpeg
import numpy as np

# 解码器类，用于对视频文件进行解码
class Decoder:
    def __init__(self):
        pass

    def decode(self, filename, playing):
        try:
            # 使用 ffmpeg.probe 获取视频文件的元信息
            probe = ffmpeg.probe(filename)
            # 查找视频流信息
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                # 若未找到视频流，返回 None
                return None
            # 获取视频的宽度
            width = int(video_stream['width'])
            # 获取视频的高度
            height = int(video_stream['height'])
            # 启动 ffmpeg 进程进行解码，将输出以原始视频格式（RGB24）输出到标准输出流
            process = (
                ffmpeg
                .input(filename)
                .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run_async(pipe_stdout=True)
            )
            # 存储解码后的视频帧
            frames = []
            while playing:
                # 从标准输出流读取视频帧数据
                in_bytes = process.stdout.read(width * height * 3)
                if not in_bytes:
                    # 若读取不到数据，跳出循环
                    break
                # 将字节数据转换为 numpy 数组，并调整形状为视频帧的尺寸
                frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
                # 将视频帧添加到列表中
                frames.append(frame)
            return frames
        except Exception as e:
            # 捕获异常并打印错误信息
            print(f"解码错误: {e}")
            return None