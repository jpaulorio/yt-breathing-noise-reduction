# yt-breathing-noise-reduction

## Pre-requisites

Python 3.12.7

## Running

```
pip install -r requirements.txt

python app.py
```

## Sample output

```
Enter the YouTube video URL: https://www.youtube.com/watch?v=abc123
Downloading YouTube video...
[youtube] Extracting URL: https://www.youtube.com/watch?v=abc123
[youtube] abc123: Downloading webpage
[youtube] abc123: Downloading ios player API JSON
[youtube] abc123: Downloading mweb player API JSON
[youtube] abc123: Downloading m3u8 information
[info] abc123: Downloading 1 format(s): 248+251
[download] Destination: original_video.f248.webm
[download] 100% of   90.68MiB in 00:00:22 at 4.12MiB/s
[download] Destination: original_video.f251.webm
[download] 100% of   31.09MiB in 00:00:08 at 3.70MiB/s
[Merger] Merging formats into "original_video.webm"
Deleting original file original_video.f248.webm (pass -k to keep)
Deleting original file original_video.f251.webm (pass -k to keep)
Video download complete.
Extracting audio...
[youtube] Extracting URL: https://www.youtube.com/watch?v=abc123
[youtube] abc123: Downloading webpage
[youtube] abc123: Downloading ios player API JSON
[youtube] abc123: Downloading mweb player API JSON
[youtube] abc123: Downloading m3u8 information
[info] abc123: Downloading 1 format(s): 251
[download] Destination: original_audio.webm
[download] 100% of   31.09MiB in 00:00:13 at 2.29MiB/s
[ExtractAudio] Destination: original_audio.wav
Deleting original file original_audio.webm (pass -k to keep)
Audio extraction complete.
Loading audio...
Identifying breathing noises...
Applying noise reduction...
Saving processed audio...
Noise reduction complete. Saved as: processed_audio.wav
Combining video with processed audio...
Moviepy - Building video final_video.mp4.
MoviePy - Writing audio in final_videoTEMP_MPY_wvf_snd.mp4
MoviePy - Done.
Moviepy - Writing video final_video.mp4

Moviepy - Done !
Moviepy - video ready final_video.mp4
Video with processed audio saved as: final_video.mp4
```