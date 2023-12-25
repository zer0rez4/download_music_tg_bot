import telebot, os, gtts
from telebot import types
from moviepy.editor import *
from pytube import YouTube

token = '6908533859:AAH8m1Fc_nhdEBokTZxxaY0H6c0FTEyQeAk'

bot = telebot.TeleBot(token)

start_markup = types.ReplyKeyboardMarkup(row_width=1)
start_markup.add(types.KeyboardButton(text='Звук из видео'), types.KeyboardButton(text='Озвучить текст'), types.KeyboardButton(text='Видео/аудио с Ютуба'))

youtube_markup = types.ReplyKeyboardMarkup(row_width=1)
youtube_markup.add(types.KeyboardButton(text='Видео (со звуком)'), types.KeyboardButton(text='Видео (без звука)'), types.KeyboardButton(text='Только звук'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}! Выбери, что хочешь сделать', reply_markup=start_markup)


@bot.message_handler(content_types=['text'])
def main_work(message):
    if message.text == 'Звук из видео':
        msg = bot.send_message(message.chat.id, 'Пришлите видео, из которого нужно получить аудио')
        bot.register_next_step_handler(msg, download_audio)
    if message.text == 'Озвучить текст':
        msg = bot.send_message(message.chat.id, 'Напишите текст для озвучки')
        bot.register_next_step_handler(msg, voice_text)
    if message.text == 'Видео/аудио с Ютуба':
        bot.send_message(message.chat.id, 'Выберите опции\nМаксимальная длительность видео - 10 минут', reply_markup=youtube_markup)

    if message.text == 'Видео (со звуком)':
        msg = bot.send_message(message.chat.id, 'Отравьте ссылку на видео')
        bot.register_next_step_handler(msg, youtube_video_audio)
    if message.text == 'Видео (без звука)':
        bot.send_message(message.chat.id, 'Данная функция в разработке')
    if message.text == 'Только звук':
        msg = bot.send_message(message.chat.id, 'Отравьте ссылку на видео')
        bot.register_next_step_handler(msg, youtube_audio)
        

def download_audio(message):
    if message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'{message.from_user.id}_video.mp4', 'wb') as file:
            file.write(downloaded_file)
        video = VideoFileClip(f'{message.from_user.id}_video.mp4')
        video.audio.write_audiofile(f'{message.from_user.id}_audio.mp3')
        with open(f'{message.from_user.id}_audio.mp3', 'rb') as audio_file:   
            bot.send_audio(message.chat.id, audio_file)
        
        os.remove(f'{message.from_user.id}_audio.mp3')
        #os.remove(f'{message.from_user.id}_video.mp4')
        
    else:
        bot.send_message(message.chat.id, 'Неверный тип файла, попробуйте снова')

def voice_text(message):
    if message.content_type == 'text':
        t1 = gtts.gTTS(message.text, lang='ru')
        t1.save(f'{message.from_user.id}_audio.mp3')
        with open(f'{message.from_user.id}_audio.mp3', 'rb') as audio_file:   
            bot.send_audio(message.chat.id, audio_file)

    else:
        bot.send_message(message.chat.id, 'Неверный тип файла, попробуйте снова')



def youtube_video_audio(message):
    try:
        yt = YouTube(message.text)
        if yt.length <= 600:
            ys = yt.streams.get_highest_resolution()
            ys.download(filename=f'{message.from_user.id}_video.mp4')

            with open(f'{message.from_user.id}_video.mp4', 'rb') as audio_file:   
                bot.send_video(message.chat.id, audio_file)

            os.remove(f'{message.from_user.id}_video.mp4')
        else:
            bot.send_message(message.chat.id, 'Видео больше 10 минут')
    except:
        bot.send_message(message.chat.id, 'Неверный тип файла, попробуйте снова')

def youtube_audio(message):
    try:
        yt = YouTube(message.text)
        if yt.length <= 600:
            ys = yt.streams.get_audio_only()
            ys.download(filename=f'{message.from_user.id}_audio.mp3')

            with open(f'{message.from_user.id}_audio.mp3', 'rb') as audio_file:   
                bot.send_video(message.chat.id, audio_file)

            os.remove(f'{message.from_user.id}_audio.mp3')
        else:
            bot.send_message(message.chat.id, 'Видео больше 10 минут')
    except:
        bot.send_message(message.chat.id, 'Неверный тип файла, попробуйте снова')


bot.polling(non_stop=True)

