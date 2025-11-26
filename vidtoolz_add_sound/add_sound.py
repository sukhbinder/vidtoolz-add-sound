from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, afx


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
