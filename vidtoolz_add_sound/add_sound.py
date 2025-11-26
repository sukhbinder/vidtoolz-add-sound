from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, afx


def add_audio_to_video(video_path, audio_path, start_time, original_audio_volume=100):
    # Load the video and audio clips
    video = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)

    # Ensure the sound starts at the specified time
    sound = sound.with_start(start_time)

    # Prepare audio clips to combine
    audio_clips = []
    if video.audio is not None:
        # Adjust original audio volume
        original_audio = video.audio.with_effects(
            [afx.MultiplyVolume(original_audio_volume / 100.0)]
        )
        audio_clips.append(original_audio)
    audio_clips.append(sound)
    clipduration = video.duration
    # Create composite audio
    final_audio = CompositeAudioClip(audio_clips)
    if final_audio.duration < clipduration:
        naudio = final_audio.with_effects([afx.AudioLoop(duration=clipduration)])
    else:
        naudio = final_audio.with_duration(clipduration)  # .audio_fadeout(afadeout)

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
