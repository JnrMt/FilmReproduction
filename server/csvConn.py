import numpy as np
import oneNN as on

class csvConn :
    
    def __init__(self):
        self.ids_path = './registration/informations/names.npy'
        self.descs_path = './registration/informations/descs.npy'
    
    def deleteUser(self,username):
        total_descs = []
        total_ids = []
        try:
            total_ids = np.load(self.ids_path).tolist()
            total_descs = np.load(self.descs_path).tolist()
        except:
            pass
        for i in range(0,len(total_ids)):
            if(total_ids[i]==username):
                del(total_ids[i])
                del(total_descs[i])
                break
        user_names = np.asarray(total_ids)
        user_descs = np.asarray(total_descs)
        np.save(self.ids_path, user_names)
        np.save(self.descs_path, user_descs)
    
    def searchUser(self,average_feat,username):
        total_descs = []
        total_ids = []
        try:
            total_ids = np.load(self.ids_path)
            total_descs = np.load(self.descs_path)
        except:
            pass
        classifier = on.OneNNClassifier(total_ids, total_descs)
        closest = classifier.predict(average_feat,username)
        if closest == None: #closest == None se non c'è un utente registrato con le mie features oppure se non ci sono descrittori
            return "none"
        else:
            return closest
            
    def regUser(self,name,features):
        user_names = []
        user_descs = []
        try:
            user_names = np.load(self.ids_path).tolist()
            user_descs = np.load(self.descs_path).tolist()
        except:
            pass
        user_names.append(name)
        user_descs.append(features)
        user_names = np.asarray(user_names)
        user_descs = np.asarray(user_descs)
        np.save(self.ids_path, user_names)
        np.save(self.descs_path, user_descs)
        #mongo = Connection_DB()
        #mongo.insertUser(name)
