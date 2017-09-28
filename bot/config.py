import json

class ConfigFile(object):

    def __init__(self, dictionary):
        self._dictionary = dictionary

    def __getitem__(self, name):
        return self._dictionary[name]

    def __iter__(self):
        return iter(self._dictionary)

    def keys(self):
        return self._dictionary.keys()

    def items(self):
        return self._dictionary.items()

    def values(self):
        return self._dictionary.values()

    def getValue(self, path, default=None):
        path = path.split('.')

        def findValue(tbl, keys, index=0, default=default):
            key = keys[index]
            try:
                if key not in tbl:
                    return default
                value = tbl[key]
                if index >= len(keys) - 1:
                    return value
                return findValue(value, keys, index=index+1) 
            except:
                return default

        return findValue(self._dictionary, path)

    def hasValue(self, path):
        return self.getValue(path) != None

    @classmethod
    def loadFromJson(cls, json_string):
        return cls(json.load(json_string))

    @classmethod
    def createFromSection(cls, section):
        return cls(section)