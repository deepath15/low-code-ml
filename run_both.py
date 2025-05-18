import subprocess

# Start imageToCode.py
p1 = subprocess.Popen(['python', 'imageToCode.py'])

# Start server.py
p2 = subprocess.Popen(['python', 'server.py'])

# Wait for both to finish (they won't, unless you stop them)
p1.wait()
p2.wait()