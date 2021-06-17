import pytest
import os

def no_crn_test():
	with pytest.raises(IndexError, match=r"You did not specify a CIS CRN.")) as e_info:
		os.system("cis-integration")