import os
import subprocess
import argparse
from tqdm import tqdm
import shutil

def main(args):
    
    assert args.input_file and args.output_file
    assert args.base in ["video", "audio"] # We have only two bitrates as the bases

    input_file = args.input_file
    
    print(f"Using {args.base} bitrate as the base")
    print("Splitting the video")
    
    os.makedirs(args.tempdirname, exist_ok=True)
    os.makedirs(f"{args.tempdirname}_o", exist_ok=True)
    
    ffmpeg_command = ['ffmpeg', '-y', '-i', input_file, '-c', 'copy', '-f', 'segment', '-segment_time', str(args.segment_duration), args.tempdirname + '/seg%d.mp4']
    
    ffmpeg_output = subprocess.run(ffmpeg_command, capture_output=True, text=True)
    
    print(f"The video has been split into {args.segment_duration}-second segments in {args.tempdirname}")
    
    mean_bitrate = 0
    num_files = len(os.listdir(args.tempdirname))
    
    pbar = tqdm(os.listdir(args.tempdirname))
    
    for file in pbar:
    
        # Get the full file path
        file_path = os.path.join(args.tempdirname, file)
        
        # Run ffprobe to get the video bitrate of the file
        ffprobe_command = ["ffprobe", "-i", file_path, "-v", "quiet", "-select_streams", "a:0" if args.base == "audio" else "v:0", "-show_entries", "stream=bit_rate", "-print_format", "json"]
        ffprobe_output = subprocess.run(ffprobe_command, capture_output=True, text=True)
        ffprobe_data = ffprobe_output.stdout

        # Parse the ffprobe output to get the video bitrate value
        ffprobe_data = ffprobe_data.strip().split("\n")
        
        bitrate = int(ffprobe_data[-4].split(":")[1].strip().strip(",").replace('"', ''))
        mean_bitrate += bitrate
        
        pbar.set_description(f"Bitrate {bitrate}, mean bitrate {mean_bitrate / num_files}")
    
    pbar.close()
    
    mean_bitrate /= num_files
    print(f"Mean bitrate {mean_bitrate}")
    
    pbar = tqdm(os.listdir(args.tempdirname))
    for file in pbar:
        # Get the full file path
        file_path = os.path.join(args.tempdirname, file)

        # Run ffprobe to get the video bitrate of the file
        ffprobe_command = ["ffprobe", "-i", file_path, "-v", "quiet", "-select_streams", "a:0" if args.base == "audio" else "v:0", "-show_entries", "stream=bit_rate", "-print_format", "json"]
        ffprobe_output = subprocess.run(ffprobe_command, capture_output=True, text=True)
        ffprobe_data = ffprobe_output.stdout

        # Parse the ffprobe output to get the video bitrate value
        ffprobe_data = ffprobe_data.strip().split("\n")
        bitrate = int(ffprobe_data[-4].split(":")[1].strip().strip(",").replace('"', ''))

        # Calculate the ratio of the mean bitrate to the video bitrate
        ratio = mean_bitrate / bitrate if not args.invert else bitrate/mean_bitrate
        
        pbar.set_description(f"Bitrate {bitrate}, ratio {ratio}")

        # Run ffmpeg to change the fps of the video based on the ratio
        ffmpeg_command = ["ffmpeg", '-y', "-i", file_path, "-vf", f"setpts={ratio}*PTS", "-filter:a", f"atempo={1/ratio}", os.path.join(f"{args.tempdirname}_o", file)]
        ffmpeg_output = subprocess.run(ffmpeg_command, capture_output=True, text=True)

    print(f"All the videos have been normalized based on the mean bitrate value of {mean_bitrate} bps")
    
    list_file = 'cavslist.txt'
    with open(list_file, 'w') as f:
        for file in sorted(os.listdir(f"{args.tempdirname}_o")):
            t = f"{args.tempdirname}_o"
            f.write(f"file '{os.path.join(t, file)}'\n")
    
    print(f"Stitching the video to {args.output_file}")
    ffmpeg_command = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_file, '-c:a', 'copy', os.path.join(os.getcwd(), args.output_file)]
    ffmpeg_output = subprocess.run(ffmpeg_command)
    
    os.remove(list_file)
    shutil.rmtree(args.tempdirname)
    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str)
    parser.add_argument("--tempdirname", type=str, default="cavs_temp")
    parser.add_argument("--segment_duration", type=int, default=60)
    parser.add_argument("--output_file", type=str)
    parser.add_argument("--invert", action="store_true")
    parser.add_argument("--base", type=str, default="video")
    args = parser.parse_args()

    main(args)
