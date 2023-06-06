# content-aware-video-speedup
 Speedups or slowdowns the video according to the bitrate of its parts

## Note

The last ffmpeg stitching line results in a buggy video, so use a software like KDENLive to stitch the fragments together.

Usage:

`python .\cavs.py --input_file .\video0.mp4 --segment_duration 5 --output_file norma.mp4 --base audio --scale_exponent 1.2`

where 'segment_duration' is the duration of each splitted part in seconds and you can set up the base bitrate to either 'video' or 'audio'.

## Applications

May be useful to slow down videos parts with haphazard editing (video bitrate) or to speed up the dull parts of lectures (audio bitrate)

### Example

https://www.youtube.com/watch?v=3t678W5zfMA

Result:

![image](https://github.com/kabachuha/content-aware-video-speedup/assets/14872007/b68cb4e8-0301-40f6-b6ca-7a8bc68afea6)
