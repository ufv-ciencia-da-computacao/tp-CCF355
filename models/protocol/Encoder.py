from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, obj):  ## create different encoders for specific commands
        return obj.to_json()
