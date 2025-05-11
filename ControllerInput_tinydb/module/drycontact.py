import os
class drycontact:
    def __init__(self,eventaction_table,controllerOutput_table,query):
        self.eventaction_table = eventaction_table
        self.controllerOutput_table = controllerOutput_table
        self.query = query
    #當乾接點打開的時候要執行的事項
    def drycontact_open(self,pin):
        getideventname = self.eventaction_table.search(self.query.id == 30)
        print(getideventname)