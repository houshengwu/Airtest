import cv2
import ffmpeg
import threading
import time
import numpy as np


class VidWriter:
    def __init__(self, outfile, width, height, mode='ffmpeg', fps=10):
        self.mode = mode
        self.fps = fps
        self.vid_size = max(width, height)
        if self.vid_size % 32 != 0:
            self.vid_size = self.vid_size - self.vid_size % 32+32
        self.cache_frame = np.zeros(
            (self.vid_size, self.vid_size, 3), dtype=np.uint8)
        width, height = self.vid_size, self.vid_size
        if self.mode == "ffmpeg":
            self.process = (
                ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24',
                       s='{}x{}'.format(width, height), framerate=fps)
                .output(outfile, pix_fmt='yuv420p', vcodec='libx264', crf=25,
                        preset="veryfast", framerate=fps)
                .global_args("-loglevel", "error")
                .overwrite_output()
                .run_async(pipe_stdin=True)
            )
            self.writer = self.process.stdin
        elif self.mode == "cv2":
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.writer = cv2.VideoWriter(outfile, fourcc, 5, (width, height))

    def write(self, frame):
        assert len(frame.shape) == 3
        if self.mode == "ffmpeg":
            frame = frame[..., ::-1].astype(np.uint8)
        self.cache_frame[:frame.shape[0], :frame.shape[1], :] = frame
        self.writer.write(self.cache_frame)

    def close(self):
        if self.mode == "ffmpeg":
            self.writer.close()
            self.process.wait()
            self.process.terminate()
        elif self.mode == "cv2":
            self.writer.release()


class ScreenRecorder:
    def __init__(self, outfile, get_frame_func, mode='ffmpeg', fps=7,
                 snapshot_sleep=0.001):
        self.get_frame_func = get_frame_func
        self.tmp_frame = self.get_frame_func()
        self.snapshot_sleep = snapshot_sleep
        width, height = self.tmp_frame.shape[1], self.tmp_frame.shape[0]
        self.writer = VidWriter(outfile, width, height, mode, fps)
        self.stop_flag = False
        self.stop_time = 0

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    def is_stop(self):
        if self.stop_flag:
            return True
        if self.stop_time > 0 and time.time() >= self.stop_time:
            return True
        return False

    def start(self, mode="two_thread"):
        if mode == "one_thread":
            t_stream = threading.Thread(target=self.get_write_frame_loop)
            t_stream.setDaemon(True)
            t_stream.start()
        else:
            t_stream = threading.Thread(target=self.get_frame_loop)
            t_stream.setDaemon(True)
            t_stream.start()
            t_write = threading.Thread(target=self.write_frame_loop)
            t_write.setDaemon(True)
            t_write.start()        

    def stop(self):
        self.stop_flag = True

    def get_frame_loop(self):
        # 单独一个线程持续截图
        try:
            while True:
                self.tmp_frame = self.get_frame_func()
                time.sleep(self.snapshot_sleep)
                if self.is_stop():
                    break
            self.stop_flag = True
        except Exception as e:
            print("record thread error", e)
            self.stop_flag = True
            raise

    def write_frame_loop(self):
        # 按帧率间隔获取图像写入视频
        try:
            duration = 1.0/self.writer.fps
            last_time = time.time()
            self.stop_flag = False
            while True:
                if time.time()-last_time >= duration:
                    self.writer.write(self.tmp_frame)
                    last_time = time.time()
                if self.is_stop():
                    break
                time.sleep(0.0001)
            self.writer.close()
            self.stop_flag = True
        except Exception as e:
            print("write thread error", e)
            self.stop_flag = True
            raise

    def get_write_frame_loop(self):
        # 同时截图并写入视频
        try:
            duration = 1.0/self.writer.fps
            last_time = time.time()
            self.stop_flag = False
            while True:
                now_time = time.time()
                if now_time - last_time >= duration:
                    if now_time - last_time < duration+0.01:
                        self.tmp_frame = self.get_frame_func()
                    self.writer.write(self.tmp_frame)
                    last_time += duration
                if self.is_stop():
                    break
                time.sleep(0.0001)
            self.stop_flag = True
            self.writer.close()
        except Exception as e:
            print("record and write thread error", e)
            self.stop_flag = True
            raise
