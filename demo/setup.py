import argparse
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from .utils import *
import os
import sys
from demo import Demo

if __name__ == "__main__":
    print("setup")
    parser = argparse.ArgumentParser(description='Demo configurations.')
    parser.add_argument('--input', default='./demo/images/human_face', type=str, help='Path to the directory containing input images')
    parser.add_argument('--result', default='./demo/results/human_face', type=str, help='Path to the directory for saving results')
    parser.add_argument('--checkpoint', default='./pretrained/pretrained_celeba/checkpoint030.pth', type=str, help='Path to the checkpoint file')
    parser.add_argument('--output_size', default=128, type=int, help='Output image size')
    parser.add_argument('--gpu', default=True, action='store_true', help='Enable GPU')
    parser.add_argument('--detect_human_face', default=True, action='store_true', help='Enable automatic human face detection. This does not detect cat faces.')
    parser.add_argument('--render_video', default=True, action='store_true', help='Render 3D animations to video')
    args = parser.parse_args()

    model = Demo(args)