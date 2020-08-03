#Importar librerias
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

#Clase para conectar a BD 
class Database:
  def __init__(self,client=None,cursor=None):
    self._client = client
    self._cursor = cursor
  def connect(self,host,port,user,password,database,schema='public',ssl_mode=None,ssl_server_ca=None,ssl_client_cert=None,ssl_client_key=None):
    try:
      options = f'-c search_path={schema} -c statement_timeout=540000'
      self._client = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        sslmode=ssl_mode,
        sslrootcert=ssl_server_ca,
        sslcert=ssl_client_cert,
        sslkey=ssl_client_key,
        options=options,
        application_name='app-puntos'
      )
    except Exception as e:
      print('error:',repr(e))
      raise e
  def connect_pool(self,host,port,user,password,database,schema='public'):
    try:
      options = f'-c search_path={schema}'
      pool = SimpleConnectionPool(
        minconn=1,
        maxconn=1,
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        options=options
      )
      self._client = pool.getconn()
    except Exception as e:
      print('error:',repr(e))
      raise e
  def disconnect(self):
    if self._client: self._client.close()
    if self._cursor: self._cursor.close()
  def get_client(self):
    return self._client
  def get_cursor(self):
    return self._cursor
  def load_config(self):
    self._client.autocommit = False
  def set_cursor(self):
    self._cursor = self._client.cursor(cursor_factory=RealDictCursor)