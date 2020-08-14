import requests
import json 
from src.controllers.responseController import responseController
class notificationController(responseController):

    def send_message(self):
        #get_response = requests.get(url="http://127.0.0.1:8080/users")
        post_data = {
            "to": "fN0WAicAdUH5qjVMgD3Api:APA91bEBaRiXlVw0Rh3PhclAQmU0LHfc3zJxPQLIx2mjbtFoQFWqApfpHm6w4x-9_qBehL1jpgVds9a0cm-u6jtDZD4V784F1152yAqrdP_fNr8uMo7POQBRQmM2b-4TLuc287J79WQu",
            "notification": {
                "body":"DUERME BRUS",
                "title":"DUERME WITCH"
            }
        }
        URI_POST = "https://fcm.googleapis.com/fcm/send"
        headers = {"Authorization": "key=AAAAU1tCR1I:APA91bHOETQM-hBFHmxqZQmA3noj4SLDGruH3_fkCaIefTROIYioARyi3cS-yeHoxl6oZYWurUHT2E36HuuqBpY7kDKL1X608I-TlFCWPo3dkd5FSYY7Hj6HeoiP5MEA-TBugYx7v2Dz"}
        # POST some form-encoded data:
        print(post_data)
        print(json.dumps(post_data))

        post_response = requests.post(url=URI_POST, json=post_data,headers=headers)

        #print(get_response.text)
        print(post_response.text)
        return post_response.text