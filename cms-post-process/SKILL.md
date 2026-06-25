---
name: cms-post-process
description: Find the most impactful moment in video files with local ffmpeg/ffprobe, then export screenshots and a combined GIF containing all selected moments. Use when Codex needs to post-process CMS video assets, scan a folder or file path containing videos, identify highlight moments, create thumbnails/stills, generate preview GIFs, create a combined highlight GIF, or batch process .mp4, .mov, .mkv, .webm, .avi, .m4v, .wmv, .flv, .mpg, .mpeg, or .3gp files.
---

# CMS Post Process

## Workflow

Use the bundled script for the actual video processing:

```powershell
python <skill-dir>\scripts\process_videos.py <video-or-folder-path>
```

Run it from any working directory. The script uses the computer's installed `ffmpeg` and `ffprobe`, so verify they are on `PATH` if the script reports they are missing.

By default, the script:

- Processes a single video file, or all supported video files directly inside a folder.
- Detects candidate impact moments with ffmpeg scene-change scoring.
- Chooses the highest-scoring scene moment, avoiding the first and last half-second when possible.
- Falls back to the middle of the video if no usable scene score is found.
- Saves one `.jpg` screenshot beside each original source video.
- Creates one short temporary `.gif` clip per video in the chosen output directory.
- Writes `combined_moments.gif` to the original input directory, concatenating the selected moment from every successfully processed video.
- Deletes the individual per-video `.gif` clips after `combined_moments.gif` is created successfully.
- Writes one `cms-post-process-report.json` with selected timestamps and the combined GIF path.

## Options

Use these flags as needed:

```powershell
python <skill-dir>\scripts\process_videos.py <path> --recursive
python <skill-dir>\scripts\process_videos.py <path> --output-dir <output-folder>
python <skill-dir>\scripts\process_videos.py <path> --scene-threshold 0.18
python <skill-dir>\scripts\process_videos.py <path> --gif-width 720 --gif-fps 15
python <skill-dir>\scripts\process_videos.py <path> --moment-seconds 1.5
python <skill-dir>\scripts\process_videos.py <path> --combined-gif-name highlight_reel.gif
python <skill-dir>\scripts\process_videos.py <path> --no-combined-gif
python <skill-dir>\scripts\process_videos.py <path> --overwrite
```

Guidance:

- Use `--recursive` only when the user asks to process subfolders or when the path is clearly a media folder tree.
- Lower `--scene-threshold` when videos have few cuts or slow transitions.
- Raise `--scene-threshold` when too many minor transitions are selected.
- Use `--output-dir` only when temporary per-video GIF clips and the JSON report should be placed somewhere specific. Screenshots still go beside the original videos, and `combined_moments.gif` still goes to the original input directory.
- Keep GIFs around 640-720 px wide unless the user asks for larger files.
- Keep `combined_moments.gif` enabled by default. Use `--no-combined-gif` only when the user explicitly asks for separate clips without a combined file; individual GIF clips are not deleted in that mode.
- Use `--moment-seconds` when the combined GIF should linger longer or move faster through each video.

## Output Naming

For each input video named `example.mp4`, expect:

- `example_moment.jpg`
- `example_moment.gif` only when `--no-combined-gif` is used or combined GIF creation fails before cleanup

For the batch, expect:

- `combined_moments.gif`
- `cms-post-process-report.json`

If a file already exists and `--overwrite` is not used, the script adds a numeric suffix.

## Reporting Back

After processing, tell the user:

- How many videos were processed.
- Where the output folder is.
- Where the combined GIF is.
- Which timestamp was selected for each successful video.
- Any skipped or failed files and the reason.

If the user asks for "the most impactful moment" across a set rather than per video, compare the `score` fields in the JSON report and present the highest-scoring item.
