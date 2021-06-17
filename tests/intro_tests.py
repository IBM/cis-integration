import pytest
import os

def no_crn_test():
	os.system("cd ..")
	with pytest.raises(IndexError) as e_info:
		os.system("cis-integration")