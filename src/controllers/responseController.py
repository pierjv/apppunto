class responseController(object):
    def __init__(self):
        self.OK = 1
        self.interruption = -1
        self.failUser = -2
        self.status_user_to_be_confirmed_admin = -2
        self.messageOK = 'Proceso exitoso'
        self.messageUserToBeConfirmed = 'Su Usuario está siendo validado, en breve le enviaremos un SMS.'
        self.messageInterruption = 'Presento una interrupcion: '
        self.messageFailUser = 'El usuario no existe o la clave es incorrecta'
        self.userDontExist = 'El usuario no existe'
        self.dontExistValues = 'No existen valores para la solicitud'
        self.duplicatedMail = "El mail se encuentra registrado"
        self.smsSuccess = "Se envió un SMS a : "
        self.invalidCoupon = "Cupón inválido"
        self.saleSuccess = "Se registró y envió con éxito su solicitud. Importante: aún no se realizó ningún cargo a su tarjeta."
        self.saleSuccessNotPush = "Se registró con éxito su solicitud. Importante: aún no se realizó ningún cargo a su tarjeta."
        self.saleSuccessConfirm = "La transacción fue exitosa"
        self.addCustomer = "Se registraron los datos exitosamente."
        self.addCustomerAndCode = "Se registraron los datos exitosamente y tiene un cupón de descuento." 
        self.messageUserToBeConfirmedAdmin = "Su registro ha sido enviado a los administradores. En las próximas horas, se le informará, sobre su aceptación o rechazo"
        self.status_sale_accept = 1
        self.status_sale_refuse = 2
        self.status_sale_confirm = 3
        self.status_sale_cancel = 4
        self.push_message_user =  "Appunto: Tienes una nueva solicitud pendiente."
        self.push_message_accept_sale = "Appunto: Tu solicitud fue aceptada."
        self.push_message_refuse_sale = "Appunto: Tu solicitud fue rechazada."
        self.pushSuccess = "Se registró y envió con éxito su mensaje."
        self.pushNotSuccess = "Se registró con éxito el cambio."
        self.saleCanceled = "La solicitud fue cancelada"
        self.typeUserFreelancer = "FREELANCER"
        self.typeUserMarca = "MARCA"
        self.idTypeUserFreelancer = 1
        self.idTypeUserMarca =2
        self.status_user_to_be_confirmed = 2
        self.status_user_confirmed =1
        self.status_user_refused = 3
        