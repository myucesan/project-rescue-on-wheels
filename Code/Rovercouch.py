import couchdb

class Repository:


    def __init__(self, server):

        self.server = couchdb.Server(server)
        self.repository = None
        self.repositories = []

    def selectAllRepositories(self):

        for repository in self.server:
            self.repositories.append(repository)

    def deleteRepository(self, name):

        del self.repository

    def deleteDocs(self, id):

        del self.repository[id]

    def createDoc(self, id, doc):

        docToSave = {
            "_id": str(id),
            "state": doc["state"],
            "time": doc["time"]
        }

        self.repository.save(docToSave)

    def createRepository(self, name):

        self.server.create(name)


    def selectRepository(self, name):

        self.repository = self.server[name]