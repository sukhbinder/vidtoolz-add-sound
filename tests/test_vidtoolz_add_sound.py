import os
from argparse import ArgumentParser
from pathlib import Path

import pytest
from moviepy import VideoFileClip

import vidtoolz_add_sound as w

# Import the function to be tested
from vidtoolz_add_sound.add_sound import add_audio_to_video, write_clip

# Define paths for test files
HERE = Path(__file__).parent
TEST_OUTPUT_PATH = HERE / "output_test_video.mp4"
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(
        ["test_video.mp4", "audio.mp3", "-s", "5", "-v", "50", "--no-loop"]
    )
    assert result.video == "test_video.mp4"
    assert result.audio == "audio.mp3"
    assert result.start_time == 5
    assert result.volume == 50
    assert result.no_loop is True
    assert result.audio_start_time == 0


def test_plugin(capsys):
    w.addsound_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_realcase_addsound(tmpdir):
    outfile = Path(tmpdir) / "output.mp4"
    testdata = HERE / "test_data"
    video = testdata / "test_video.mp4"
    audio = testdata / "test_audio.mp3"

    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    argv = [str(video), str(audio), "-o", str(outfile)]
    args = parser.parse_args(argv)
    w.addsound_plugin.run(args)
    assert outfile.exists()


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_realcase_addsound_ffmpeg(tmpdir):
    outfile = Path(tmpdir) / "output_ffmpeg.mp4"
    testdata = HERE / "test_data"
    video = testdata / "test_video.mp4"
    audio = testdata / "test_audio.mp3"

    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    argv = [str(video), str(audio), "-o", str(outfile), "-ffmpeg"]
    args = parser.parse_args(argv)
    w.addsound_plugin.run(args)
    assert outfile.exists()


@pytest.fixture(scope="module")
def test_files():
    testdata = HERE / "test_data"
    TEST_VIDEO_PATH = testdata / "test_video.mp4"
    TEST_AUDIO_PATH = testdata / "test_audio.mp3"
    return str(TEST_VIDEO_PATH), str(TEST_AUDIO_PATH)


# Clean up test files
def cleanup_test_files():
    if TEST_OUTPUT_PATH.exists():
        TEST_OUTPUT_PATH.unlink()


def test_add_audio_to_video(test_files):
    # Define the start time for the audio
    TEST_VIDEO_PATH, TEST_AUDIO_PATH = test_files
    start_time = 1

    # Call the function to be tested
    clip = add_audio_to_video(TEST_VIDEO_PATH, TEST_AUDIO_PATH, start_time)
    write_clip(clip, TEST_OUTPUT_PATH)
    # Verify the output file exists
    assert os.path.exists(TEST_OUTPUT_PATH)

    # Load the output video to verify the audio
    output_video = VideoFileClip(TEST_OUTPUT_PATH)
    assert output_video.audio is not None

    # Check the audio start time
    audio_start_time = output_video.audio.start
    assert (
        audio_start_time == 0
    ), f"Expected audio start time {start_time}, but got {audio_start_time}"

    # Clean up the output video
    output_video.close()
    cleanup_test_files()


def test_add_audio_to_video_no_loop(test_files):
    # Define the start time for the audio
    TEST_VIDEO_PATH, TEST_AUDIO_PATH = test_files
    start_time = 1

    # Call the function to be tested
    clip = add_audio_to_video(
        TEST_VIDEO_PATH,
        TEST_AUDIO_PATH,
        start_time,
        original_audio_volume=0,
        loop_audio=False,
    )
    write_clip(clip, TEST_OUTPUT_PATH)
    # Verify the output file exists
    assert os.path.exists(TEST_OUTPUT_PATH)

    # Load the output video to verify the audio
    output_video = VideoFileClip(TEST_OUTPUT_PATH)
    assert output_video.audio is not None

    # check that the audio is not looped
    # We can't simply check the duration, as moviepy will pad the audio to match the video duration.
    # Instead, we check if the audio is silent after the original audio clip's duration.
    # A fadeout is applied, so it won't be perfectly silent, and there can be artifacts.
    audio_sample = output_video.audio.get_frame(4.5)
    assert sum(abs(audio_sample)) < 0.001

    # Clean up the output video
    output_video.close()
    cleanup_test_files()


def test_add_audio_to_video_with_volume(test_files):
    # Define the start time for the audio
    TEST_VIDEO_PATH, TEST_AUDIO_PATH = test_files
    start_time = 1
    volume = 50

    # Call the function to be tested
    clip = add_audio_to_video(
        TEST_VIDEO_PATH, TEST_AUDIO_PATH, start_time, original_audio_volume=volume
    )
    write_clip(clip, TEST_OUTPUT_PATH)
    # Verify the output file exists
    assert os.path.exists(TEST_OUTPUT_PATH)

    # Load the output video to verify the audio
    output_video = VideoFileClip(TEST_OUTPUT_PATH)
    assert output_video.audio is not None

    # Clean up the output video
    output_video.close()
    cleanup_test_files()


def test_add_audio_to_video_with_volume_audio_start(test_files):
    # Define the start time for the audio
    TEST_VIDEO_PATH, TEST_AUDIO_PATH = test_files
    start_time = 1
    volume = 50
    audio_start_time = 2

    # Call the function to be tested
    clip = add_audio_to_video(
        TEST_VIDEO_PATH,
        TEST_AUDIO_PATH,
        start_time,
        original_audio_volume=volume,
        audio_start_time=audio_start_time,
    )
    write_clip(clip, TEST_OUTPUT_PATH)
    # Verify the output file exists
    assert os.path.exists(TEST_OUTPUT_PATH)

    # Load the output video to verify the audio
    output_video = VideoFileClip(TEST_OUTPUT_PATH)
    assert output_video.audio is not None

    # Clean up the output video
    output_video.close()
    cleanup_test_files()
