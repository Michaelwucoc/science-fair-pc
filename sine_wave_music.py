# -*- coding: utf-8 -*-

import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def play_melody():
    mode = input('请选择模式 (1) 预设参数 (2) 实时输入: ')
    if mode == '1':
        # 获取用户输入
        freq1 = float(input('请输入第一个频率（Hz）：'))
        amp1 = float(input('请输入第一个振幅（0-1）：'))
        freq2 = float(input('请输入第二个频率（Hz）：'))
        amp2 = float(input('请输入第二个振幅（0-1）：'))
        duration = float(input('请输入时长（秒）：'))

        # 生成波形
        wave1 = generate_sine_wave(freq1, amp1, duration)
        wave2 = generate_sine_wave(freq2, amp2, duration)
        melody = wave1 + wave2

        # 显示波形图
        t = np.linspace(0, duration, int(44100 * duration))
        plt.plot(t[:1000], melody[:1000])  # 显示前1000个采样点
        # Set Chinese font
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        plt.title('正弦波波形图')
        plt.xlabel('时间（秒）')
        plt.ylabel('振幅')
        plt.show()

        # 播放声音
        sd.play(melody, samplerate=44100)
        sd.wait()
    else:
        # 实时模式
        duration = float(input('请输入时长（秒）：'))
        sample_rate = 44100
        chunk_size = 1024
        t = np.linspace(0, duration, int(sample_rate * duration))

        # 设置交互模式
        plt.ion()
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title('实时音频波形')
        line, = ax.plot(t[:chunk_size], np.zeros(chunk_size))
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        plt.title('实时正弦波波形图')
        plt.xlabel('时间（秒）')
        plt.ylabel('振幅')
        plt.tight_layout()

        # 创建数据缓冲区
        buffer = np.zeros(chunk_size)

        def callback(indata, frames, time, status):
            if status:
                print(status)
            nonlocal buffer
            buffer = indata[:, 0]

        def update_line(frame):
            line.set_ydata(buffer)
            return line,

        # 创建动画
        ani = FuncAnimation(
            fig, update_line, interval=20, blit=True
        )

        # 创建音频流
        with sd.InputStream(
            channels=1,
            callback=callback,
            samplerate=sample_rate,
            blocksize=chunk_size,
            dtype='float32'
        ):
            plt.show(block=True)
            sd.sleep(int(duration * 1000))

if __name__ == '__main__':
    play_melody()