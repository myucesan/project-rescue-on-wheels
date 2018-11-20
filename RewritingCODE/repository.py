import couchdb

class Repository:


    def __init__(self, server):

        self.server = couchdb.Server(server)
        self.repository = None
        self.repositories = []

    def select_all_repositories(self):

        for repository in self.server:
            self.repositories.append(repository)

    def delete_repository(self, name):

        del self.repository

    def delete_docs(self, id):

        del self.repository[id]

    def create_doc(self, id, doc):

        save = {
            "_id": str(id),
            "state": doc["state"],
            "time": doc["time"]
        }

        self.repository.save(save)

    def open_doc(self, id):

        return self.repository[str(id)]

    def create_repository(self, name):

        self.server.create(name)


    def select_repository(self, name):

        self.repository = self.server[name]