from organization import Organization
from pipedriver import PipeDriver
from math import radians, cos, sin, atan2, sqrt

earth_radius = 6371
epsilon = 0.000001


def get_api_key():
    with open('apikey.txt') as f:
        return f.read().strip()


def distance(point_a, point_b):
    # From: https://www.movable-type.co.uk/scripts/latlong.html
    alat = radians(point_a[0])
    blat = radians(point_b[0])
    along = radians(point_a[1])
    blong = radians(point_b[1])

    deltalat = blat - alat
    deltalong = blong - along

    a = sin(deltalat / 2) * sin(deltalat / 2) + cos(alat) * cos(blat) * sin(deltalong / 2) * sin(deltalong / 2)
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
        # Does distance calculations several times over, for brevity, which isn't horrible seeing how few orgs there likely are.
        sorted_organizations = sorted(self.organizations.values(), key=lambda org: distance(point, (org.latitude, org.longitude)))
        shortest = distance(point, (sorted_organizations[0].latitude, sorted_organizations[0].longitude))
        out = []

        for organization in sorted_organizations:
            orgpoint = (organization.latitude, organization.longitude)
            orgdist = distance(point, orgpoint)
            if abs(orgdist - shortest) < epsilon:  # Handling rounding errors
                out.append(organization.id)
            else:
                break

        return out