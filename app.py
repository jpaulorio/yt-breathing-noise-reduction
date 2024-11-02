import yt_dlp
import os
import librosa
import soundfile as sf
import noisereduce as nr
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np

def download_youtube_video(url, output_path='original_video'):
    print("Downloading YouTube video...")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Video download complete.")

def download_youtube_audio(url, output_path='original_audio'):
    print("Extracting audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Rename the file if it has a double extension (e.g., .wav.wav)
    for ext in ['wav', 'webm', 'mp3', 'm4a']:
        if os.path.exists(f'{output_path}.{ext}'):
            os.rename(f'{output_path}.{ext}', f'{output_path}.wav')
            break

    print("Audio extraction complete.")

def identify_breathing_noise(y, sr, window_size=2048, hop_length=512, energy_threshold=0.02):
    print("Identifying breathing noises...")
    energy = np.array([
        sum(abs(y[i:i + window_size]**2))
        for i in range(0, len(y) - window_size, hop_length)
    ])
    breathing_indices = np.where(energy < energy_threshold)[0]
    
    if len(breathing_indices) == 0:
        print("No low-energy (potential breathing) segments detected.")
        return None
    
    start_sample = breathing_indices[0] * hop_length
    end_sample = start_sample + window_size
    return y[start_sample:end_sample]

def reduce_breathing_noise(input_path, output_path='processed_audio.wav'):
    print("Loading audio...")
    y, sr = librosa.load(input_path, sr=None)
    noise_sample = identify_breathing_noise(y, sr)
    
    if noise_sample is None:
        print("Breathing noise profile not detected. Skipping noise reduction.")
        return

    print("Applying noise reduction...")
    reduced_audio = nr.reduce_noise(y=y, sr=sr, y_noise=noise_sample, prop_decrease=1.0)
    
    print("Saving processed audio...")
    sf.write(output_path, reduced_audio, sr)
    print("Noise reduction complete. Saved as:", output_path)

def combine_video_audio(video_path, audio_path, output_path='output_video.mp4'):
    print("Combining video with processed audio...")
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video_with_new_audio = video.set_audio(audio)
    video_with_new_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
    print("Video with processed audio saved as:", output_path)

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    
    download_youtube_video(video_url, output_path='original_video')
    download_youtube_audio(video_url, output_path='original_audio')

    reduce_breathing_noise('original_audio.wav', output_path='processed_audio.wav')
    
    combine_video_audio('original_video.webm', 'processed_audio.wav', output_path='final_video.mp4')
