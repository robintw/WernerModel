rm -rf /tmp/*.png
x=1; for i in *png; do counter=$(printf %03d $x); ln "$i" /tmp/img"$counter".png; x=$(($x+1)); done
ffmpeg -f image2 -i /tmp/img%03d.png Video.mpg
ffmpeg -f image2 -i /tmp/img%03d.png -r 10 VideoSlow.avi
