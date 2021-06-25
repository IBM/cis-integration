import os
from src.functions import Color

first_check = False
second_check = False
# checking to see if "cis-integration" is present in /usr/local/bin
if os.path.isfile("/usr/local/bin/cis-integration"):
    print(Color.GREEN+"Install Successful!"+Color.END)
else:
    first_check = True
    print(Color.RED+"ERROR: Install Failed! cis-integration command line tool was not found in /usr/local/bin/"+Color.END)

# checking to see if "ci" is present in /usr/local/bin
if os.path.isfile("/usr/local/bin/ci"):
    print(Color.GREEN+"Install Successful!"+Color.END)
else:
    second_check = True
    print(Color.RED+"ERROR: Install Failed! ci (alias) command line tool was not found in /usr/local/bin/"+Color.END)

if first_check or second_check:
    print(Color.YELLOW+"If a permission issue was encountered trying running the installation script as \"sudo ./install.sh\""+Color.END)