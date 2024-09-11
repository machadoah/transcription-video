import argparse
from loguru import logger
import whisper
import os
import yt_dlp as ytdlp


def download_audio(video_url: str, audio_path: str) -> str:
    output_dir = './audios'
    os.makedirs(output_dir, exist_ok=True)

    full_audio_path = os.path.join(output_dir, f"{audio_path}.mp4")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': full_audio_path,
        'noplaylist': True,
    }

    try:
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        logger.info(f"Downloaded {full_audio_path}")
    except Exception as e:
        logger.error(f"Failed to download audio: {e}")
    return full_audio_path


def transcribe_audio(audio_path: str) -> str:
    model = whisper.load_model('base')
    result = model.transcribe(audio_path)
    return result['text']


def main():
    parser = argparse.ArgumentParser(description='Download audio and transcribe from YouTube')

    parser.add_argument('--url', type=str, required=True, help='YouTube video URL')
    parser.add_argument('--path', type=str, default='audio', help='Output file name (without extension)')

    args = parser.parse_args()

    try:
        full_audio_path = download_audio(args.url, args.path)
    except Exception as e:
        logger.error(f"Error during audio download: {e}")
        return

    try:
        transcription = transcribe_audio(full_audio_path)
        logger.success('Transcription success!')
        print("Transcription:\n", transcription)
    except Exception as e:
        logger.error(f"Error during transcription: {e}")


if __name__ == '__main__':
    main()
