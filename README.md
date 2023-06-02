# content-aware-video-speedup
 Speedups or slowdowns the video according to the bitrate of its parts

## Note

The last ffmpeg stitching line results in a buggy video, so use a software like KDENLive to stitch the fragments together.

Usage:

`python .\cavs.py --input_file .\video0.mp4 --segment_duration 5 --output_file norma.mp4 --base audio`

where 'segment_duration' is the duration of each splitted part in seconds and you can set up the base bitrate to either 'video' or 'audio'.
