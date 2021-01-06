import os
import wave
from aip import AipSpeech
import pyaudio
import winsound
import win32com.client
import time


app_id = '16787563'
api_key='BWdUiU6W9w45RnvOOGlYIAKQ'
secret_key ='Yg0UZapvh2QYhna1bB2R2mQuaXgFOBWK'

client = AipSpeech(app_id,api_key,secret_key)

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'myvoices.wav'

def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()
# 录音
def my_record():
    pa = pyaudio.PyAudio()
    # 打开一个新的音频stream
    stream = pa.open(format=pyaudio.paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []  # 存放录音数据

    t = time.time()
    print('正在录音...')
    while time.time() < t + 5:  # 设置录音时间（秒）
        # 循环read，每次read 2000frames
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()

def listen():
  # 读取录音文件
  with open(FILEPATH, 'rb') as fp:
    voices = fp.read()
  try:
    # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
    result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })
    # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
    # print(result)
    # print(result['result'][0])
    # print(result)
    result_text = result["result"][0]
    print("you said: " + result_text)
    return result_text
  except KeyError:
    print("KeyError")

def speak(str):
    speak_out = win32com.client.Dispatch('SAPI.SPVOICE')
    speak_out.Speak(str)
    winsound.PlaySound(str, winsound.SND_ASYNC)

#speak('你好，我是小言！')

while True:
    my_record()
    request_str = listen()
    if request_str == '计算器。':
        os.system("calc")
    elif request_str == '关机。':
        os.system("shutdown -s -t 60")
    elif request_str == '取消关机。':
        os.system("shutdown -a")
    elif request_str == '退出程序。':
        break



