import subprocess


# subprocess.Popen('ls -la', shell=True)
subprocess.Popen('-m mlgame -f 120 -i path/to/ml/ml_play_manual.py path/to/TankMan --map_no 3 --sound off --frame_limit 3000', shell=True)
