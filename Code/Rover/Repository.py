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

    def createDoc(self, id, step, direction, time):

        doc = {
            "_id": id,
            "step": step,
            "direction": direction,
            "time": time
        }

        self.repository.save(doc)

    def createRepository(self, name):

        self.server.create(name)


    def selectRepository(self, name):

        self.repository = self.server[name]

    def writeIntoRepository(self, doc):

        self.repository.save(doc)


repo = Repository("http://localhost:5984")
repo.selectRepository("rover")
#repo.deleteDocs("0d5d9d5f021220e7635304febc00169e")
repo.createDoc("1", 1, "forward", 20)