class Organization:
    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return 'Name: {0} Position: ({1}, {2}) Id: {3}'.format(self.name, self.latitude, self.longitude, self.id)

    def __repr__(self):
        return str(self)