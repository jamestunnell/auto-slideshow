#!/usr/bin/python

from slideshow_app import SlideshowApp
from slideshow_program import SlideshowProgram
import argparse
import os.path

parser = argparse.ArgumentParser()

parser.add_argument('--slide_time_ms', type=int, default=3000,
                     help="default time between slides, in milliseconds (only \
                     applicable when slideshow contains no songs)")

parser.add_argument('--root_dir', type=str, default=os.path.join(os.path.dirname(__file__),"travel"),
                    help="root directory of slideshow program")

parser.add_argument('--hide', action='store_true', 
                    help="Do not display slideshow images")

parser.add_argument('--no_auto_start', action='store_true', 
                    help="Automatically restart the slideshow when its over.")

parser.add_argument('--auto_restart', action='store_true', 
                    help="Automatically restart the slideshow when its over.")

args = parser.parse_args()

if __name__ == '__main__':
    print("Running slideshow with opts: %s" % vars(args))
    auto_start = not args.no_auto_start
    
    program = SlideshowProgram(
        args.root_dir,
        slide_time_ms=args.slide_time_ms,
        auto_restart=args.auto_restart)
    viewer = SlideshowApp(
        program,
        auto_start=auto_start)
    viewer.MainLoop()
