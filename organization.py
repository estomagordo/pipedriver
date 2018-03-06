class Organization:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.latitude, self.longitude = [float(part) for part in address.split(',')]

    def __str__(self):
        return self.name