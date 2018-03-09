class Organization:
    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)