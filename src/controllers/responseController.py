class responseController(object):
    def __init__(self):
        self.OK = 1
        self.interruption = -1
        self.failUser = -2
        self.messageOK = 'Proceso exitoso'
        self.messageInterruption = 'Presento una interrupcion: '
        self.messageFailUser = 'El usuario no existe o la clave es incorrecta'
        self.userDontExist = 'El usuario no existe o'
