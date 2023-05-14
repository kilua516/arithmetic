#!/usr/bin/python

import random
import string
import random
import pyttsx3
import subprocess

from datetime import datetime
from pydub import AudioSegment
from fpdf import FPDF

file_name = "十以内加减和表内乘法_间隔0.5秒_语速1.2倍"
count_per_practice = 30
total_practice = 10

import pyttsx3
def num2chinese(num):
    # 数字转中文，仅支持到千亿级别，可根据需要自行扩展
    chn_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    chn_units = ['', '十', '百', '千', '万', '十', '百', '千', '亿']
    num_str = str(num)
    num_len = len(num_str)
    result = ''
    zero_flag = True
    for i in range(num_len):
        idx = int(num_str[i])
        if idx == 0:
            if num_len == 1:
                result = chn_nums[0]
            elif not zero_flag and num_len-i-1 < 4 and (num_len-i-1)%4 == 0:
                result += chn_units[num_len-i-1]
                zero_flag = True
        else:
            if zero_flag == True and idx == 1 and num_len == 2:
                result += chn_units[num_len-i-1]
                zero_flag = False
            else:
                result += chn_nums[idx] + chn_units[num_len-i-1]
                zero_flag = False
    return result


def audio_out(audio_file, audio_list, rand_a, rand_b, rand_op):
    duration = 500
    if rand_op == "+":
        op_voice = "加"
#       if (rand_a > 10) and (rand_b > 10):
#           duration = 6000
    elif rand_op == "-":
        op_voice = "减"
#       if (rand_a > 10) and (rand_b > 10):
#           duration = 6000
    elif rand_op == "*":
        op_voice = "乘"
    elif rand_op == "/":
        op_voice = "除以"
#       if (rand_a > 10):
#           duration = 5000

    audio_tmp_file = "audio_tmp.mp3"
    engine.save_to_file("%s%s%s"%(num2chinese(rand_a), op_voice, num2chinese(rand_b)), audio_tmp_file)
    print("%s%s%s"%(num2chinese(rand_a), op_voice, num2chinese(rand_b)))
    engine.runAndWait()
    subprocess.call(['ffmpeg', '-i', audio_tmp_file, '-ac', '2', '-ar', '44100', '-codec:a', 'libmp3lame', '-y', audio_file])
    audio_list.append(AudioSegment.from_mp3(audio_file))
    audio_list.append(AudioSegment.silent(duration))

def print_out(out, rand_a, rand_b, rlt, rand_op):
    if rand_op == "+":
        op_str = '+'
    elif rand_op == "-":
        op_str = '-'
    elif rand_op == "*":
        op_str = '×'
    elif rand_op == "/":
        op_str = '÷'

    print("%-2u%s%-2u=%s\t"%(rand_a, op_str, rand_b, rlt))
    out.write("%-2u%s%-2u=%s\t"%(rand_a, op_str, rand_b, rlt))
    question = ("%-2u%s%-2u=%s\t"%(rand_a, op_str, rand_b, rlt))
    pdf.cell(50, 10.5, question)

# Initialize tts engine
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('engine', 'sapi5')
engine.setProperty('zh-CH', 'voice_ked_dengxuetong.pronunciation_dict={"乘": "cheng"}')

voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id, voice.name)

# 创建PDF对象
pdf = FPDF()
# 添加页面
pdf.add_page()
# 设置字体和字号
pdf.set_font("Arial", size=16)

cnt = 0
practice_initialized = 0

while(1):
    if practice_initialized == 0:
        practice_initialized = 1
        time_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        out_file = open("out_%s.txt"%(time_str), "w")
        audio_file = "%s_%s.mp3"%(file_name, time_str)
        audio_list = []

        pdf.cell(100, 10.5, '=================')
        pdf.ln();
        pdf.cell(100, 10.5, time_str)
        pdf.ln();
        pdf.cell(100, 10.5, '=================')
        pdf.ln();

    # 随机选择加减乘除
#   rand_op = random.choice(["+", "-", "*", "/"])
    rand_op = random.choice(["+", "-", "*"])
#   rand_op = "+"                     # add

    if rand_op == "+":
        rand_a = random.randint(1,10)
        rand_b = random.randint(1,10)
        rlt = rand_a + rand_b
        if (rlt >= 0) and (rlt <= 10):
            print_out(out_file, rand_a, rand_b, rlt, rand_op)
            audio_out(audio_file, audio_list, rand_a, rand_b, rand_op)
            cnt = cnt + 1
        else:
            continue
    elif rand_op == "-":
        rand_a = random.randint(1,10)
        rand_b = random.randint(1,10)
        rlt = rand_a - rand_b
        if (rlt >= 0) and (rlt <= 10):
            print_out(out_file, rand_a, rand_b, rlt, rand_op)
            audio_out(audio_file, audio_list, rand_a, rand_b, rand_op)
            cnt = cnt + 1
        else:
            continue
    elif rand_op == "*":
        rand_a = random.randint(1,9)
        rand_b = random.randint(1,9)
        rlt = rand_a * rand_b
        if (rand_a < 10) and (rand_b < 10) and (rlt <= 100):
            print_out(out_file, rand_a, rand_b, rlt, rand_op)
            audio_out(audio_file, audio_list, rand_a, rand_b, rand_op)
            cnt = cnt + 1
        else:
            continue
    elif rand_op == "/":
        rand_a = random.randint(1,19)
        rand_b = random.randint(1,9)
        rlt = rand_a * rand_b
        if (rand_a < 10) and (rand_b < 10) and (rlt <= 100):
            print_out(out_file, rlt, rand_b, rand_a, rand_op)
            audio_out(audio_file, audio_list, rlt, rand_b, rand_op)
            cnt = cnt + 1
        else:
            continue

    if (cnt % count_per_practice) % 4 == 0:
        pdf.ln()
        out_file.write('\n')
    if (cnt % count_per_practice) == 0:
        practice_initialized = 0
        out_file.write('\n')
        out_file.close()

        output = audio_list[0]
        for i in range(1, len(audio_list)):
            output += audio_list[i]

        output.export(audio_file, format = 'mp3')
    if cnt >= (count_per_practice * total_practice):
        break

pdf.output("%s.pdf"%(file_name))

