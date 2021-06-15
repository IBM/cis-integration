
AUTHORIZATION="Basic Yng6Yng="
TOKEN=$(echo $(curl -i -k -X POST \
      --header "Content-Type: application/x-www-form-urlencoded" \
      --header "Authorization: $AUTHORIZATION" \
      --data-urlencode "apikey=$CIS_SERVICES_APIKEY" \
      --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
      "https://iam.cloud.ibm.com/identity/token"))
# IAM Access Token
ACCESS_TOKEN=$(echo $TOKEN | sed -e s/.*access_token\":\"//g | sed -e s/\".*//g)
# IAM Refresh token
REFRESH_TOKEN=$(echo $TOKEN | sed -e s/.*refresh_token\":\"//g | sed -e s/\".*//g)   

echo $REFRESH_TOKEN
#export R_TOKEN=$REFRESH_TOKEN
#export