import yaml as yml

class dbModel(object):
    def __init__(self):
        with open('src/cn/.env.yml') as f:
            env_vars = yml.full_load(stream=f)
        self.host = env_vars['PG_HOST']
        self.port = env_vars['PG_PORT']
        self.user = env_vars['PG_USER']
        self.password = env_vars['PG_PASS']
        self.database = env_vars['PG_NAME']
        self.token_user = env_vars['Tk_USER']
        self.token_password = env_vars['TK_PASW']
        self.push_uri_post = env_vars['PN_URI_POST']
        self.push_firebase_key = env_vars['PN_FIREBASE_KEY']
        self.culqi_public_key = env_vars['PP_PUBLIC_KEY']
        self.culqi_private_key = env_vars['PP_PRIVATE_KEY']
        self.text_uri_post = env_vars['TM_URI_POST']
        self.text_user = env_vars['TM_USER']
        self.text_password = env_vars['TM_PASSWORD']
        self.url_server = env_vars['URL_SERVER']
