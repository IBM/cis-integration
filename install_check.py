'''
DISCLAIMER OF WARRANTIES:
Permission is granted to copy this Tools or Sample code for internal use only, provided that this
permission notice and warranty disclaimer appears in all copies.

THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
import os
from src.common.functions import Color

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