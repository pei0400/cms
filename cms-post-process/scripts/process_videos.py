#!/usr/bin/env python3
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


VIDEO_EXTENSIONS = {
    ".3gp",
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
    ".wmv",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find impactful moments in videos and export screenshots, GIF clips, and one combined GIF."
    )
    parser.add_argument("path", help="Video file or folder containing video files.")
    parser.add_argument(
        "--output-dir",
        help=(
            "Folder for per-video GIF previews and report. Screenshots are always saved "
            "beside their source videos, and the combined GIF is always saved to the "
            "original input directory."
        ),
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process videos in subfolders when the input path is a folder.",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.15,
        help="Minimum ffmpeg scene score to consider. Lower finds subtler moments.",
    )
    parser.add_argument(
        "--gif-width",
        type=int,
        default=640,
        help="GIF width in pixels. Height preserves aspect ratio.",
    )
    parser.add_argument(
        "--gif-fps",
        type=int,
        default=12,
        help="GIF frame rate.",
    )
    parser.add_argument(
        "--moment-seconds",
        type=float,
        default=1.0,
        help="Seconds to include from each selected moment in GIF outputs.",
    )
    parser.add_argument(
        "--combined-gif-name",
        default="combined_moments.gif",
        help="Filename for the combined GIF containing every selected moment.",
    )
    parser.add_argument(
        "--no-combined-gif",
        action="store_true",
        help="Skip creating the combined GIF.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files.",
    )
    return parser.parse_args()


def require_tool(name):
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} was not found on PATH")
    return path


def run_command(cmd):
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(message)
    return completed.stdout, completed.stderr


def discover_videos(input_path, recursive):
    path = Path(input_path).expanduser().resolve()
    if path.is_file():
        return [path] if path.suffix.lower() in VIDEO_EXTENSIONS else []
    if not path.is_dir():
        raise FileNotFoundError(f"Path does not exist: {path}")
    iterator = path.rglob("*") if recursive else path.iterdir()
    return sorted(
        file
        for file in iterator
        if file.is_file() and file.suffix.lower() in VIDEO_EXTENSIONS
    )


def get_duration(ffprobe, video):
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video),
    ]
    stdout, _ = run_command(cmd)
    try:
        duration = float(stdout.strip())
    except ValueError as exc:
        raise RuntimeError(f"Could not read duration for {video.name}") from exc
    if not math.isfinite(duration) or duration <= 0:
        raise RuntimeError(f"Invalid duration for {video.name}")
    return duration


def get_dimensions(ffprobe, video):
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0:s=x",
        str(video),
    ]
    stdout, _ = run_command(cmd)
    match = re.search(r"(\d+)x(\d+)", stdout)
    if not match:
        raise RuntimeError(f"Could not read dimensions for {video.name}")
    width = int(match.group(1))
    height = int(match.group(2))
    if width <= 0 or height <= 0:
        raise RuntimeError(f"Invalid dimensions for {video.name}")
    return width, height


def detect_scene_candidates(ffmpeg, video, threshold):
    # metadata=print emits frame blocks containing pts_time and lavfi.scene_score.
    filtergraph = f"select='gte(scene,{threshold})',metadata=print"
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-i",
        str(video),
        "-vf",
        filtergraph,
        "-an",
        "-f",
        "null",
        "-",
    ]
    _, stderr = run_command(cmd)

    candidates = []
    current_time = None
    for line in stderr.splitlines():
        time_match = re.search(r"pts_time:([0-9.]+)", line)
        if time_match:
            current_time = float(time_match.group(1))
            continue
        score_match = re.search(r"lavfi\.scene_score=([0-9.]+)", line)
        if score_match and current_time is not None:
            candidates.append(
                {"time": current_time, "score": float(score_match.group(1))}
            )
            current_time = None
    return candidates


def choose_moment(candidates, duration):
    minimum = 0.5 if duration > 1.5 else 0.0
    maximum = max(minimum, duration - 0.5)
    usable = [
        candidate
        for candidate in candidates
        if minimum <= candidate["time"] <= maximum
    ]
    if usable:
        return max(usable, key=lambda candidate: candidate["score"]), "scene-score"
    fallback_time = min(max(duration / 2.0, 0.0), max(duration - 0.01, 0.0))
    return {"time": fallback_time, "score": None}, "duration-midpoint"


def safe_stem(video):
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", video.stem).strip("._-")
    return stem or "video"


def unique_path(path, overwrite):
    if overwrite or not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def export_screenshot(ffmpeg, video, timestamp, output_path, overwrite):
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y" if overwrite else "-n",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]
    run_command(cmd)


def export_gif(ffmpeg, video, start_time, output_path, width, fps, moment_seconds, overwrite):
    scale = f"scale={width}:-1:flags=lanczos"
    palette_filter = (
        f"fps={fps},{scale},split[s0][s1];"
        "[s0]palettegen=max_colors=128[p];"
        "[s1][p]paletteuse=dither=bayer:bayer_scale=5"
    )
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y" if overwrite else "-n",
        "-ss",
        f"{start_time:.3f}",
        "-t",
        f"{moment_seconds:.3f}",
        "-i",
        str(video),
        "-vf",
        palette_filter,
        "-loop",
        "0",
        str(output_path),
    ]
    run_command(cmd)


def export_combined_gif(
    ffmpeg,
    results,
    output_path,
    width,
    height,
    fps,
    moment_seconds,
    overwrite,
):
    if not results:
        return None

    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n"]
    for result in results:
        cmd.extend(
            [
                "-ss",
                f"{result['gif_start_seconds']:.3f}",
                "-t",
                f"{moment_seconds:.3f}",
                "-i",
                result["video"],
            ]
        )

    filters = []
    labels = []
    for index in range(len(results)):
        label = f"v{index}"
        filters.append(
            f"[{index}:v]fps={fps},"
            f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
            f"setsar=1[{label}]"
        )
        labels.append(f"[{label}]")

    joined = "".join(labels)
    filtergraph = (
        ";".join(filters)
        + f";{joined}concat=n={len(results)}:v=1:a=0,"
        "split[s0][s1];"
        "[s0]palettegen=max_colors=128[p];"
        "[s1][p]paletteuse=dither=bayer:bayer_scale=5"
    )
    cmd.extend(["-filter_complex", filtergraph, "-loop", "0", str(output_path)])
    run_command(cmd)
    return output_path


def remove_individual_gifs(results, combined_gif):
    deleted = []
    cleanup_failures = []
    combined_path = Path(combined_gif).resolve()

    for result in results:
        gif_path = Path(result["gif"])
        try:
            if gif_path.resolve() == combined_path:
                continue
            if gif_path.exists():
                gif_path.unlink()
                deleted.append(str(gif_path))
                result["gif_deleted_after_combined"] = True
            else:
                result["gif_deleted_after_combined"] = False
                result["gif_cleanup_note"] = "file was already missing"
        except OSError as exc:
            result["gif_deleted_after_combined"] = False
            result["gif_cleanup_error"] = str(exc)
            cleanup_failures.append({"gif": str(gif_path), "error": str(exc)})

    return deleted, cleanup_failures


def process_video(ffmpeg, ffprobe, video, output_dir, args):
    if args.moment_seconds <= 0:
        raise RuntimeError("--moment-seconds must be greater than zero")
    duration = get_duration(ffprobe, video)
    candidates = detect_scene_candidates(ffmpeg, video, args.scene_threshold)
    moment, method = choose_moment(candidates, duration)
    timestamp = moment["time"]
    gif_start = max(
        0.0,
        min(timestamp - (args.moment_seconds / 2.0), max(duration - args.moment_seconds, 0.0)),
    )

    base = safe_stem(video)
    screenshot = unique_path(video.parent / f"{base}_moment.jpg", args.overwrite)
    gif = unique_path(output_dir / f"{base}_moment.gif", args.overwrite)

    export_screenshot(ffmpeg, video, timestamp, screenshot, args.overwrite)
    export_gif(
        ffmpeg,
        video,
        gif_start,
        gif,
        args.gif_width,
        args.gif_fps,
        args.moment_seconds,
        args.overwrite,
    )

    return {
        "video": str(video),
        "duration_seconds": round(duration, 3),
        "selected_timestamp_seconds": round(timestamp, 3),
        "gif_start_seconds": round(gif_start, 3),
        "score": None if moment["score"] is None else round(moment["score"], 6),
        "selection_method": method,
        "candidate_count": len(candidates),
        "screenshot": str(screenshot),
        "gif": str(gif),
    }


def default_output_dir(input_path):
    path = Path(input_path).expanduser().resolve()
    return path.parent if path.is_file() or path.suffix.lower() in VIDEO_EXTENSIONS else path


def original_input_dir(input_path):
    path = Path(input_path).expanduser().resolve()
    return path.parent if path.is_file() or path.suffix.lower() in VIDEO_EXTENSIONS else path


def main():
    args = parse_args()
    try:
        ffmpeg = require_tool("ffmpeg")
        ffprobe = require_tool("ffprobe")
        videos = discover_videos(args.path, args.recursive)
        output_dir = (
            Path(args.output_dir).expanduser().resolve()
            if args.output_dir
            else default_output_dir(args.path)
        )
        original_dir = original_input_dir(args.path)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        failures = []
        for video in videos:
            try:
                results.append(process_video(ffmpeg, ffprobe, video, output_dir, args))
                print(f"OK {video.name}")
            except Exception as exc:
                failures.append({"video": str(video), "error": str(exc)})
                print(f"FAILED {video.name}: {exc}", file=sys.stderr)

        combined_gif = None
        deleted_individual_gifs = []
        gif_cleanup_failures = []
        if results and not args.no_combined_gif:
            source_width, source_height = get_dimensions(ffprobe, Path(results[0]["video"]))
            combined_height = max(2, round(args.gif_width * source_height / source_width))
            if combined_height % 2:
                combined_height += 1
            combined_path = unique_path(
                original_dir / args.combined_gif_name,
                args.overwrite,
            )
            combined_gif = str(
                export_combined_gif(
                    ffmpeg,
                    results,
                    combined_path,
                    args.gif_width,
                    combined_height,
                    args.gif_fps,
                    args.moment_seconds,
                    args.overwrite,
                )
            )
            deleted_individual_gifs, gif_cleanup_failures = remove_individual_gifs(
                results,
                combined_gif,
            )
            for cleanup_failure in gif_cleanup_failures:
                print(
                    f"WARNING could not delete {cleanup_failure['gif']}: {cleanup_failure['error']}",
                    file=sys.stderr,
                )

        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "input_path": str(Path(args.path).expanduser().resolve()),
            "output_dir": str(output_dir),
            "original_output_dir": str(original_dir),
            "scene_threshold": args.scene_threshold,
            "moment_seconds": args.moment_seconds,
            "combined_gif": combined_gif,
            "deleted_individual_gifs": deleted_individual_gifs,
            "gif_cleanup_failures": gif_cleanup_failures,
            "processed_count": len(results),
            "failure_count": len(failures),
            "results": results,
            "failures": failures,
        }
        report_path = output_dir / "cms-post-process-report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        print(json.dumps(report, indent=2))
        return 0 if results or not videos else 2
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
