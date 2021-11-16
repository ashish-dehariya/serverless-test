from qualtrics_api_base import 
import json


class MailingLists():
    def __init__(self, api_token, data_center, retries=0):
        super(MailingLists, self).__init__(api_token, data_center, retries)

 

    def update_contact(self, mailing_list_id, contact_id, embedded_data=''):
        if not mailing_list_id:
            raise ValueError("mailing_list_id cannot be empty")
        if not contact_id:
            raise ValueError("contact_id cannot be empty")
        url = '{}{}/contacts/{}'.format(self._get_service_url(), mailing_list_id, contact_id)
        data = {}
        if embedded_data:
            data.update({"embeddedData": embedded_data})

        response = self.put(url, data=json.dumps(data), headers=self.get_headers())
        if response.ok:
            pass
        else: response={"Error":"failed"}
        return response.json()



    def _get_service_url(self):
        return self.get_base_url() + "mailinglists/"


