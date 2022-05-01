#!/usr/bin/env bash
# https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg/37478183
#set -e
#mkdir -p out
#youtube-dl https://www.youtube.com/watch?v=MeUiaxaRMK8
#mv 央視水滸傳配樂\ 1998\ Water\ Margin\ Theme-MeUiaxaRMK8.mkv out/in.mkv
#ffmpeg -i out/in.mkv -q:a 0 -map a out/in.flac
cp in.txt out/
grep -E '^file ' in.txt | sed -E 's/^file //; s/\..*//' | while read f; do
  echo $f
  convert -thumbnail 1280x720 -background black -gravity center -extent 1280x720 "$(command ls -1 ../$f.* | grep -v .xcf | head -n1)" "out/$f.jpg"
done
cd out
ffmpeg -y -f concat -i in.txt -ss 0:36.5 -i in.flac -c:v libx264 -c:a libvorbis -shortest -r 30 -pix_fmt yuv420p water.mp4
