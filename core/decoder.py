import ffmpeg
import numpy as np

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
                print("未找到视频流")
                return None
            # 获取视频的宽度和高度
            width = int(video_stream['width'])
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
                    break
                # 将字节数据转换为 numpy 数组，并调整形状为视频帧的尺寸
                frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
                frames.append(frame)
            # 关闭 ffmpeg 进程
            process.stdout.close()
            process.wait()
            return frames
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
            return None
        except Exception as e:
            print(f"解码错误: {e}")
            return None