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

    def get_organization(self, id):
        response = requests.get(self.base_url + 'organizations/' + str(id), params = self.params)
        response.raise_for_status()
        data = response.json()['data']
        
        name = data['name']
        latitude, longitude = self.address_to_coords(data['address'])

        return Organization(id, name, latitude, longitude)

    def get_organizations(self):
        response = requests.get(self.base_url + 'organizations', params = self.params)

        response.raise_for_status()

        organizations = {}

        data = response.json()['data']
        
        for entry in data:
            id = int(entry['id'])
            name = entry['name']
            latitude, longitude = self.address_to_coords(entry['address'])

            organizations[id] = Organization(id, name, latitude, longitude)

        return organizations

    def create_organization(self, name, latitude, longitude):
        address = self.coords_to_address(latitude, longitude)
        data = { 'name': name, 'address': address }
        response = requests.post(self.base_url + 'organizations', data = data, params = self.params)

        response.raise_for_status()
        id = response.json()['data']['id']

        organization = Organization(id, name, latitude, longitude)

        return organization

    def delete_organization(self, id):
        response = requests.delete(self.base_url + 'organizations/' + str(id), params = self.params)
        response.raise_for_status()

        return True

    def update_organization(self, id, name, latitude, longitude):
        organization = self.get_organization(id)
        address = self.coords_to_address(latitude, longitude)
        data = { 'name': name, 'address': address }
        
        response = requests.put(self.base_url + 'organizations/' + str(id), data = data, params = self.params)

        response.raise_for_status()

        organization.name = name
        organization.latitude = latitude
        organization.longitude = longitude        

        return organization