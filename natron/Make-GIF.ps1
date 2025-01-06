ffmpeg -framerate 24 -i distort.%04d.png -vf "scale=800:-1:flags=lanczos,fps=24" distort.gif
