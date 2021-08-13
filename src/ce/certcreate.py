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

from src.common.functions import Color as Color
from ibm_cloud_networking_services import SslCertificateApiV1


class CertificateCreator:

    def __init__(self, crn, zone_id, endpoint, domain):
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.hostNames = [domain, "*."+domain]

    def create_certificate(self):
        # setting tls mode to strict
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)
        try:
            resp = cert.change_ssl_setting(value="strict")
            print(
                Color.GREEN+"SUCCESS: Set TLS mode to End-to-end CA Signed (strict)"+Color.END)
        except:
            print(
                Color.RED+"ERROR: Unable to set mode TLS mode to End-to-end CA Signed (strict)"+Color.END)

        # checking for duplicated hostnames
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)
        resp = cert.list_certificates()
        for cert in resp.result['result']:
            if set(self.hostNames) == set(cert['hosts']):
                print(Color.YELLOW+"WARNING: certificate already made with host names: " +
                      " ".join(self.hostNames)+Color.END)
            return
        # end

        # creating certificate
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)

        try:
            resp = cert.order_certificate(
                x_correlation_id="1864", type="dedicated", hosts=self.hostNames)
            print(Color.GREEN+"SUCCESS: Created certificate"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to create certificate. Make sure hostname(s) match custom domain name"+Color.END)
