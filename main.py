
from aiogram import Bot, Dispatcher, executor, types
import moviepy.Effect as mp
import os
import io
import tempfile
import aiogram.utils.exceptions

API_TOKEN = "BOT_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

MAX_FILES_SIZE = 50 * 1012 * 1024

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Assalomu aleykum, \nBotga video yuboring va videoning audiosini olasiz.")



def convert_video_to_audio(video_stream : io.BytesIO):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            temp_video_file.write(video_stream.read())
            temp_video_file.flush()
            video = mp.VideoClip(temp_video_file.name)
            audio_path = temp_video_file.name.replace(".mp4", ".mp3")

            video.audio.write_audio(audio_path)

            return audio_path

    except Exception as e:
        print(f"Error processing video file: {e}")
        return None

@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def handle_video(message: types.Message):
    try:
        print("try")
        if message.video.file_size > MAX_FILES_SIZE:
            await message.reply(f"Video hajimi juda katta. Iltimos  kichik hajmdagi video yuboring. \nVideo {MAX_FILES_SIZE}mb dan oshmasligi zarur.")
            return
        video_bytes = await message.video.download(destination_file=io.BytesIO())

        audio_path = convert_video_to_audio(video_bytes)

        if not audio_path:
            await message.reply("Videon yuklashda xatolik yuz berdi. \nBoshqa video fayl yuborib ko`ring")
            return 
        
        with open(audio_path, "rb") as audio:
            await message.answer_audio(audio)

        os.remove(audio_path)    
    except aiogram.utils.exceptions.FileIsTooBig:
        await message.reply("Fayl hajmi katta, iltimos kichik hajimdagi fayl yuboring!")


    except Exception as e:
        await message.reply(f"Xatolik yuz berdi : {e}")







if __name__=="__main__":
    os.makedirs("Video", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
