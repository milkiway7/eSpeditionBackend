from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
class ShipperRegistrationService:
        def __init__(self,repository):
                self.repository = repository
        
        async def finalize_registration(self,registration_to_update: RegistrationsDbTableModel):
                #transaction

                #return JWT ? czy to wystarczy do bycia zalogowanym ?
                
            pass

        # For shipper this is final step- so i neet to update status to COMPLETED and save account type to SHIPPER
        # Then create transatcion for shipper
        # BEGIN TRANSACTION
        # mark registration COMPLETED
        # create company
        # create user
        # link user → company
        # COMMIT
        # Retrun JWT TOKEN bcs he will be already logged in