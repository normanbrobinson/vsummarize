#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.concatenate import concatenate
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def summarize(filepath, new_filename, hotclips):
    """
    Inputs a filepath for a video and generates a new shorter video
    in that same filepath.
    """
    # Only open the file once!
    video = VideoFileClip(filepath)

    chunks = [ video.subclip(start, end)
               for (start, end) in hotclips]

    final_clip = concatenate(chunks)

    # txt_clip = ( TextClip("Generated by vSummarize",
    #                      fontsize=20, color='white')
    #             .set_pos('bottom')
    #             .set_duration(5))
    # final_clip = CompositeVideoClip([summarized_video, txt_clip])

    # Use the to_videofile default codec, libx264
    # libx264 is much better than mpeg4, and still writes .mp4
    # Use the fps of the original video.
    final_clip.to_videofile(new_filename,
                            fps=video.fps,
                            audio_codec='mp3')

if __name__ == '__main__':
    summarize("TbQm5doF_Uc.mp4",
              "finished_from_video.mp4",
              hotclips = [(1,5), (15,20), (35,40)])
