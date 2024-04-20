import pygame
from moviepy.editor import VideoFileClip

def play_intro_video():
    # Path to the intro video
    video_path = 'menu/intro.mp4'
    # Load the video
    clip = VideoFileClip(video_path)
    video_size = clip.size

    # Initialize pygame
    pygame.init()
    # Play video
    clip.preview()

    # Close the video window
    clip.close()

