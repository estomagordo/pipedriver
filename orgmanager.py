from organization import Organization
from pipedriver import PipeDriver
from math import radians, cos, sin, atan2, sqrt

earth_radius = 6371
epsilon = 0.000001


def get_api_key():
    with open('apikey.txt') as f:
        return f.read().strip()


def great_circle_distance(point_a, point_b):
    # From: https://www.movable-type.co.uk/scripts/latlong.html
    alat = radians(point_a[0])
    blat = radians(point_b[0])
    along = radians(point_a[1])
    blong = radians(point_b[1])

    dlat = blat - alat
    dlong = blong - along

    a = (
        sin(dlat / 2) *
        sin(dlat / 2) + cos(alat) *
        cos(blat) * sin(dlong / 2) *
        sin(dlong / 2))

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return earth_radius * c


class OrgManager:

    def __init__(self):
        self.pipedriver = PipeDriver(get_api_key())
        self.organizations = self.pipedriver.get_organizations()

    def contains(self, id):
        return id in self.organizations

    def count(self):
        return len(self.organizations)

    def get_all(self):
        return self.organizations

    def get(self, id):
        return self.organizations[id]

    def print(self, id):
        print(self.organizations[id])

    def print_all(self):
        print('\n'.join(str(self.organizations[id]) for id in sorted(self.organizations.keys())))

    def create(self, name, latitude, longitude):
        organization = self.pipedriver.create_organization(name, latitude, longitude)
        self.organizations[organization.id] = organization
        return organization

    def edit(self, id, name, latitude, longitude):
        self.organizations[id] = self.pipedriver.update_organization(id, name, latitude, longitude)
        return self.get(id)

    def delete(self, id):
        self.pipedriver.delete_organization(id)
        del self.organizations[id]
        return True

    def find_nearest(self, point):
        sorted_orgs = sorted(
            (great_circle_distance(point, (org.latitude, org.longitude)), org)
            for org in self.organizations.values())

        shortest_distance = sorted_orgs[0][0]
        nearest = []

        for distance, organization in sorted_orgs:
            if abs(distance - shortest_distance) < epsilon:  # Handling rounding errors
                nearest.append(organization)
                continue
            break

        return shortest_distance, nearest
