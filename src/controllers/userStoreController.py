from src.models.userModel import userModel
from src.models.userStoreModel import userStoreModel
from src.entities.userEntity import userEntity
from src.entities.userStoreEntity import userStoreEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class userStoreController(responseController):

    def get_user_stores_by_id_user(self,index):
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

    def add_user_store(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _entity = userStoreEntity()
            _model = userStoreModel()
            _entity.requestToClass(request)
            _entity = _model.add_user_store(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    
    def delete_user_store(self,index):
        _message = None
        _status = self.interruption
        _id= None
        try:
            _model = userStoreModel()
            _id = _model.delete_user_store(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_id).toJSON()