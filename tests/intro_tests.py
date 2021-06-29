# import pytest
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# from src.create_edge_function import EdgeFunctionCreator

# def test_no_crn():
# 	output = os.system("cis-integration")
# 	assert output == 256

# def test_no_zone_id():
# 	load_dotenv('./src/credentials.env')
# 	crn = os.getenv('CRN')
# 	output = os.system("cis-integration " + crn)
# 	assert output == 256

# def test_no_domain():
# 	load_dotenv('./src/credentials.env')
# 	crn = os.getenv('CRN')
# 	zone_id = os.getenv("ZONE_ID")
# 	output = os.system("cis-integration " + crn + " " + zone_id)
# 	assert output == 256

# def test_no_appication_url():
# 	load_dotenv('./src/credentials.env')
# 	crn = os.getenv("CRN")
# 	zone_id = os.getenv("ZONE_ID")
# 	domain = os.getenv("CIS_DOMAIN")
# 	output = os.system("cis-integration " + crn + " " + zone_id + " " + domain)
# 	assert output == 256

# def test_all_info_given():
# 	load_dotenv('./src/credentials.env')
# 	crn = os.getenv("CRN")
# 	zone_id = os.getenv("ZONE_ID")
# 	domain = os.getenv("CIS_DOMAIN")
# 	app_url = os.getenv("APP_URL")
# 	output = os.system("cis-integration " + crn + " " + zone_id + " " + domain + " " + app_url)
# 	assert output == 0