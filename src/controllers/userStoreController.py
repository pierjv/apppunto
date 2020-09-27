from src.models.userModel import userModel
from src.models.userStoreModel import userStoreModel
from src.entities.userEntity import userEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class userStoreController(responseController):

    def get_user_stores(self,index):
        _message = None
        _status = responseController().interruption
        _data= None
        try:
            _userStoreModel = userStoreModel()
            _data = _userStoreModel.get_user_stores_by_id_user(index)
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()