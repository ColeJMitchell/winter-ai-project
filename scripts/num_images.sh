#!/bin/bash
color=$1
piece=$2
# Script to count the number of images in a directory
find "/home/cole/github/winter-ai-project/training_data/${color}_${piece}/" -type f \( -iname "*.jpg" \) | wc -l