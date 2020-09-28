# coding: utf-8
from datetime import datetime
from PIL import ImageGrab
import numpy as np
import cv2
import time


class RecordAudio():
    def __init__(self, fps):
        # 录制结束标识
        self.flag = False
        # 帧率
        self.fps = int(fps)
        # 捕获开始时间戳
        self.start_time = int(time.time())
        # 捕获结束时间戳
        self.end_time =None
        # 定义文件名
        self.audio_name = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.avi'

    def _get_screen_size(self):
        # 获取屏幕对象
        curScreen = ImageGrab.grab()
        height, width = curScreen.size
        return height, width

    def _record_audio(self):
        # 录屏主逻辑
        height, width = self._get_screen_size()
        # 创建视频对象
        video = cv2.VideoWriter(self.audio_name, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (height, width))
        print("开始录制")
        while True:
            curr_time = int(time.time())
            # 录屏半小时
            if curr_time >= self.start_time+18:
                break
            try:
                captureImage = ImageGrab.grab()
            except:
                pass
            # 截取当前屏幕
            frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
            # 写入视频文件
            video.write(frame)
        print("录制结束")
        self.end_time = curr_time
        self.release(video)

    def start_record(self):
        # 录屏对外入口
        self._record_audio()
        return self.audio_name

    def release(self, video):
        # 释放录屏对象
        video.release()
        cv2.destroyAllWindows()

    """用来配置视频清晰度"""
    # def __del__(self):
    #     video = cv2.VideoCapture(self.audio_name)
    #     fps = video.get(cv2.CAP_PROP_FPS)
    #     Count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    #     size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #     print('帧率=%.1f' % fps)
    #     print('帧数=%.1f' % Count)
    #     print('分辨率', size)
    #     print('视频时间=%.3f秒' % (int(Count) / fps))
    #     print('录制时间=%.3f秒' % (self.end_time - self.start_time))
    #     print('推荐帧率=%.2f' % (fps * ((int(Count) / fps) / (self.end_time - self.start_time))))
