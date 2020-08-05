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
