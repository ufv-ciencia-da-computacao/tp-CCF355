from json import JSONEncoder


class CompleteUserEncoder(JSONEncoder):
    def default(self, obj):
        return obj.complete_to_json()


class CreateUserEncoder(JSONEncoder):
    def default(self, obj):
        return obj.create_to_json()
