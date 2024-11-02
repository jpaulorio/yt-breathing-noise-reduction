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

## Rationale

The noise identification logic in the program is designed to detect breathing noises in the audio by analyzing the energy level of short segments. Here’s an explanation of the rationale behind this approach:

1. Characteristics of Breathing Noises:
Low Energy: Breathing noises typically have a lower amplitude (volume) compared to speech or other prominent audio content.
Short and Repetitive: They often occur as short bursts of sound, making them identifiable by their low energy and brief duration.
2. Short-Time Energy Calculation:
The short-time energy (STE) is used to quantify how much "power" or "energy" exists in short segments of the audio signal. This calculation helps in identifying segments that might represent soft sounds like breathing.

### Formula for Short-Time Energy:
The short-time energy (STE) is used to quantify how much "power" or "energy" exists in short segments of the audio signal. This calculation helps in identifying segments that might represent soft sounds like breathing.

#### Formula:
```math
E[n] = \sum_{m=0}^{N-1} |x[m + n]|^2
```
- **$E[n]$**: Energy of the segment starting at sample \( n \).
- **$x[m + n]$**: Amplitude of the audio signal at sample \( m + n \).
- **$N$**: Window size (number of samples).

3. Windowing the Audio Signal:
Window Size (window_size): Determines how many samples are analyzed in each energy calculation. A typical window size (e.g., 2048 samples) is used to capture short bursts of sound while preserving enough detail to differentiate between noises and speech.
Hop Length (hop_length): The step size between consecutive windows. This controls the overlap between windows. A value like 512 samples ensures enough overlap for continuous analysis.
Energy Threshold (energy_threshold): A pre-set value that defines what is considered "low energy". This helps isolate soft sounds (e.g., breathing) from louder content (e.g., speech or music).
4. Logic Behind Noise Identification:
Calculate Energy: The program iterates through the audio signal using the specified window size and hop length, calculating the short-time energy for each segment.
Identify Low-Energy Segments: It checks if the calculated energy for a segment is below the energy_threshold. If so, it marks these segments as potential breathing noise.
Select a Noise Sample: The first detected low-energy segment is returned as a sample of noise. This is used for noise reduction in the noisereduce function.
5. Rationale for Using Short-Time Energy:
Effective for Soft Sound Detection: Short-time energy is a fundamental method for detecting the presence of sound in an audio signal. It is especially effective for identifying soft, continuous noises like breathing because they stand out as low-energy segments when compared to louder parts of the audio.
Simple and Efficient: The method is computationally straightforward and can be implemented with minimal resources. It provides a good balance between performance and accuracy for basic noise detection.
Adaptable: The energy_threshold can be adjusted to suit different types of audio content. This flexibility allows it to be tuned for various scenarios, such as podcasts or interviews, where breathing noises may be more pronounced.
6. Potential Improvements:
While this method is effective for identifying basic breathing noises, it has limitations:

Sensitivity: The threshold needs to be carefully set to avoid false positives (e.g., identifying quiet parts of speech as noise).
Noise Complexity: More complex noise types may require advanced methods like spectral analysis or machine learning to identify accurately.
Why This Approach?
The chosen logic strikes a balance between simplicity and functionality:

Simplicity: Using short-time energy avoids the complexity of spectral or machine learning-based noise detection methods.
Focused Detection: The method is suitable for detecting noises that are consistently low in amplitude, like breathing, without affecting other parts of the audio.
Example of the Identification Process:
Audio Signal: The program processes the audio in chunks defined by the window size.
Energy Calculation: The energy of each chunk is calculated and compared to the threshold.
Noise Sample: If a chunk’s energy falls below the threshold, it is flagged as a potential noise segment.
Output: The first low-energy segment found is used as the noise profile for noise reduction.
Conclusion:
The rationale behind using short-time energy for noise identification is its simplicity, computational efficiency, and suitability for detecting low-energy, repetitive noises like breathing. While it may not capture complex noise profiles, it effectively identifies simple, low-amplitude noise segments for processing.