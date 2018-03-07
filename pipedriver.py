import requests
from organization import Organization

class PipeDriver:
    base_url = 'https://companydomain.pipedrive.com/v1/'

    def coords_to_address(self, latitude, longitude):
        return str(latitude) + ',' + str(longitude)

    def address_to_coords(self, address):
        return [float(coord) for coord in address.split(',')]

    def __init__(self, api_token):
        self.params = { 'api_token': api_token }
        self.organizations = {}
        self.next_id = 0

    def get_organizations(self):
        response = requests.get(self.base_url + 'organizations', params = self.params)

        response.raise_for_status()

        data = response.json()['data']
        
        for entry in data:
            id = int(entry['id'])
            self.next_id = max(self.next_id, id + 1)
            name = entry['name']
            latitude, longitude = self.address_to_coords(entry['address'])

            self.organizations[id] = Organization(id, name, latitude, longitude)

        return len(self.organizations)

    def create_organization(self, name, latitude, longitude):
        # Should be improved to handle multiple users
        address = self.coords_to_address(latitude, longitude)
        organization = Organization(self.next_id, name, latitude, longitude)

        data = { 'name': name, 'address': address }

        response = requests.post(self.base_url + 'organizations', data = data, params = self.params)

        response.raise_for_status()

        self.organizations[self.next_id] = organization
        self.next_id += 1

        return self.next_id - 1

    def delete_organization(self, id):
        if not id in self.organizations:
            raise IndexError

        response = requests.delete(self.base_url + 'organizations/' + str(id), params = self.params)
        response.raise_for_status()

        del self.organizations[id]

        return True

    def update_organization(self, id, name = None, latitude = None, longitude = None):
        if not id in self.organizations:
            raise IndexError

        organization = self.organizations[id]
        newname = name or organization.name
        newlatitude = latitude or organization.latitude
        newlongitude = longitude or organization.longitude
        address = self.coords_to_address(newlatitude, newlongitude)

        data = { 'name': newname, 'address': address }
        
        response = requests.put(self.base_url + 'organizations/' + str(id), data = data, params = self.params)

        response.raise_for_status()

        self.organizations[id].latitude = newlatitude
        self.organizations[id].longitude = newlongitude
        self.organizations[id].name = newname

        return True