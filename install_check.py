import os

# checking to see if "cis-integration" is present in /usr/local/bin
if os.path.isfile("/usr/local/bin/cis-integration"):
    print("Install Successful!")
else:
    print("Install Failed!")