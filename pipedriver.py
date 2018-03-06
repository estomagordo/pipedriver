import requests
from organization import Organization

class PipeDriver:
    base_url = 'https://companydomain.pipedrive.com/v1/'

    def __init__(self, api_token):
        self.params = { 'api_token': api_token }
        self.organizations = []

    def get_organizations(self):
        response = requests.get(self.base_url + 'organizations', params = self.params)
        data = response.json()['data']
        
        for entry in data:
            self.organizations.append(Organization(int(entry['id']), entry['name'], entry['address']))

        print(' '.join(organization.name for organization in self.organizations))
        for organization in self.organizations: print(organization)

if __name__ == '__main__':
    pipe_driver = PipeDriver('a7098337502aacd4a642156eb8131e48eb8b7d31')
    pipe_driver.get_organizations()