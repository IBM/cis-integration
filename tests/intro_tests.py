import pytest
import os

def no_crn_test():
	with pytest.raises(IndexError) as e_info:
		os.system("cis-integration")