class responseController(object):
    def __init__(self):
        self.OK = 1
        self.interruption = -1
        self.failUser = -2
        self.messageOK = 'Proceso exitoso'
        self.messageInterruption = 'Presento una interrupcion: '
        self.messageFailUser = 'El usuario no existe o la clave es incorrecta'
        self.userDontExist = 'El usuario no existe'
        self.dontExistValues = 'No existen valores para la solicitud'
        self.duplicatedMail = "El mail se encuentra registrado"
        self.smsSuccess = "Se envió un SMS a : "
        self.invalidCoupon = "Cupón inválido"
        self.saleSuccess = "Venta exitosa."
        self.addCustomer = "Se registraron los datos exitosamente."
        self.addCustomerAndCode = "Se registraron los datos exitosamente y tiene un cupón de descuento." 
