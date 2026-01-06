import subprocess

from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, afx


def add_audio_at_time_ffmpeg(input_video, input_audio, start_time, output_file):
    """
    Adds input_audio to input_video starting at start_time (in seconds),
    mixing it with the video's existing audio using ffmpeg.
    """

    delay_ms = int(start_time * 1000)

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        input_video,
        "-i",
        input_audio,
        "-filter_complex",
        f"[1:a]adelay={delay_ms}|{delay_ms}[aud];[0:a][aud]amix=inputs=2[mix]",
        "-map",
        "0:v",
        "-map",
        "[mix]",
        "-c:v",
        "copy",
        output_file,
    ]

    iret = subprocess.run(ffmpeg_cmd, check=True)
    return iret


def add_audio_to_video(
    video_path, audio_path, start_time, original_audio_volume=100, loop_audio=True
):
    video = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)
    clipduration = video.duration

    if loop_audio:
        # new duration for the looping sound clip to fill the video
        loop_duration = clipduration - start_time
        if loop_duration > sound.duration:
            sound = sound.with_effects([afx.AudioLoop(duration=loop_duration)])

    sound = sound.with_start(start_time)

    audio_clips = []
    if video.audio is not None:
        original_audio = video.audio.with_effects(
            [afx.MultiplyVolume(original_audio_volume / 100.0)]
        )
        audio_clips.append(original_audio)
    audio_clips.append(sound)

    final_audio = CompositeAudioClip(audio_clips)
    # trim the whole thing to the video duration
    naudio = final_audio.with_duration(clipduration)

    naudio = naudio.with_effects([afx.AudioFadeOut(1)])

    # Set the video's audio to the combined audio
    video.audio = naudio
    return video


def write_clip(video, output_path):
    # Write the output file
    video.write_videofile(
        output_path,
        codec="libx264",
        temp_audiofile="temp_audio.m4a",
        remove_temp=True,
        audio_codec="aac",
    )
    video.close()
