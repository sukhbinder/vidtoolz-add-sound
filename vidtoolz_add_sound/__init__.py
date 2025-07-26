import vidtoolz
import os

from vidtoolz_add_sound.add_sound import add_audio_to_video, write_clip


def create_parser(subparser):
    parser = subparser.add_parser("addsound", description="Add sound to a video")
    # Add subprser arguments here.
    parser.add_argument(
        "video", type=str, help="Video file to which sound has to be added."
    )
    parser.add_argument("audio", type=str, help="Sound file to add")
    parser.add_argument(
        "-s",
        "--start-time",
        type=int,
        default=3,
        help="Time in seconds where audio has to be added",
    )
    parser.add_argument(
        "-o", "--output", default=None, type=str, help="Sound file to add"
    )
    return parser


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_sound.mp4")


class ViztoolzPlugin:
    """Add sound to a video"""

    __name__ = "addsound"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        output = determine_output_path(args.video, args.output)
        clip = add_audio_to_video(args.video, args.audio, args.start_time)
        write_clip(clip, output)
        print(f"{output} written.")

    def hello(self, args):
        # this routine will be called when "vidtoolz "addsound is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


addsound_plugin = ViztoolzPlugin()
