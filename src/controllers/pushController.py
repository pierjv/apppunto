import requests
import json
import http.client

class pushController():

    def send_message(self):
        print('hola 2')
        #get_response = requests.get(url='http://127.0.0.1:8080/users')
        post_data = {
                    'to':'fN0WAicAdUH5qjVMgD3Api:APA91bEBaRiXlVw0Rh3PhclAQmU0LHfc3zJxPQLIx2mjbtFoQFWqApfpHm6w4x-9_qBehL1jpgVds9a0cm-u6jtDZD4V784F1152yAqrdP_fNr8uMo7POQBRQmM2b-4TLuc287J79WQu',
                    'notification':{
                        'body':'DUERME BRUS',
                        'title':'DUERME WITCH'
                        }
                    }
        URI_POST = 'https://fcm.googleapis.com/fcm/send'
        headers = {'Authorization': 'key=AAAAU1tCR1I:APA91bHOETQM-hBFHmxqZQmA3noj4SLDGruH3_fkCaIefTROIYioARyi3cS-yeHoxl6oZYWurUHT2E36HuuqBpY7kDKL1X608I-TlFCWPo3dkd5FSYY7Hj6HeoiP5MEA-TBugYx7v2Dz'}
        # POST some form-encoded data:
        print(post_data)
        print(json.dumps(post_data))
        #post_data = json.dumps(post_data)

        post_response = requests.post(url=URI_POST, json=post_data,headers=headers)

        #print(get_response.text)
        print(post_response.text)
        return post_response.text

    def send_message_3(self):
        print('hola 2')
        #get_response = requests.get(url='http://127.0.0.1:8080/users')
        post_data = {'mail':'jean@hotmail.com','password':'12345678'}
        # POST some form-encoded data:
        print(post_data)
        print(json.dumps(post_data))
        #post_data = json.dumps(post_data)
        post_response = requests.post(url='http://127.0.0.1:8080/login', json=post_data)

        #print(get_response.text)
        print(post_response.text)
        return 'OK'

    def send_message_2(self):
        # defining the api-endpoint  
        API_ENDPOINT = "http://pastebin.com/api/api_post.php"
        
        # your API key here 
        API_KEY = "XXXXXXXXXXXXXXXXX"
        
        # your source code here 
        source_code = ''' 
        print("Hello, world!") 
        a = 1 
        b = 2 
        print(a + b) 
        '''
        
        # data to be sent to api 
        data = {'api_dev_key':API_KEY, 
                'api_option':'paste', 
                'api_paste_code':source_code, 
                'api_paste_format':'python'} 
        
        # sending post request and saving response as response object 
        r = requests.post(url = API_ENDPOINT, data = data) 
        
        # extracting response text  
        pastebin_url = r.text 
        print("The pastebin URL is:%s"%pastebin_url) 
    
