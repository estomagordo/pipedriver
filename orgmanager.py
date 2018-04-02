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
        self.update()

    def update(self):
        try:
            self.organizations = self.pipedriver.get_organizations()
        except Exception:
            raise

    def contains(self, id):
        return id in self.organizations

    def count(self):
        return len(self.organizations)

    def get_all(self):
        return [self.organizations[key] for key in sorted(self.organizations)]

    def get(self, id):
        return self.organizations[id]

    def create(self, name, latitude, longitude):
        try:
            organization = self.pipedriver.create_organization(name, latitude, longitude)
            self.organizations[organization.id] = organization
            return organization
        except Exception:
            raise

    def edit(self, id, name, latitude, longitude):
        try:
            organization = self.pipedriver.update_organization(id, name, latitude, longitude)
            self.organizations[id] = organization
            return organization
        except Exception:
            raise

    def delete(self, id):
        try:
            self.pipedriver.delete_organization(id)
            del self.organizations[id]
            return True
        except Exception:
            raise

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
