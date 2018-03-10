import os
from organization import Organization
from pipedriver import PipeDriver
from math import radians, cos, sin, atan2, sqrt

api_key = 'a7098337502aacd4a642156eb8131e48eb8b7d31'
earth_radius = 6371

sConnecting = 'Connecting to Pipe Drive'
sSuccessful = 'Successful!'
sOrgsInDb = 'organizations in database.'
sInstructions = '''Command list:
help - repeat this message
list - list all organizations
create - create new organization
view [id] - view organization [id]
edit [id] - edit organization [id]
delete [id] - edit organization [id]
find - find the nearest organization(s) for coordinates
exit - exit this program'''
sInvalid = 'Invalid command, please try again.'
sEnterName = 'Please enter a name.'
sEnterLatitude = 'Please enter a latitude.'
sEnterLongitude = 'Please enter a longitude.'
sCreationSuccessful = 'Creation successful!'
sNotFound = 'Organization with id {0} not found.'
sDeletionSuccessful = 'Deletion successful!'
sEnterEditName = 'Enter new name. Press enter to keep as is.'
sEnterEditLatitude = 'Enter new latitude. Press enter to keep as is.'
sEnterEditLongitude = 'Enter new longitude. Press enter to keep as is.'
sNothingChanged = 'Nothing changed. Update skipped.'
sEditSuccessful = 'Edit successful!'

def clear():
    dummy = os.system('cls' if os.name == 'nt' else 'clear')

def clearprint(s):
    clear()
    print(s)

def latitude_legal(latitude):
    return -90.0 <= latitude <= 90.0

def longitude_legal(longitude):
    return -180.0 <= longitude <= 180.0

def distance(point_a, point_b):
    # From: https://www.movable-type.co.uk/scripts/latlong.html
    alat = radians(point_a[0])
    blat = radians(point_b[0])
    along = radians(point_a[1])
    blong = radians(point_b[1])
    
    deltalat  = blat - alat
    deltalong = blong - along

    a = sin(deltalat / 2) * sin(deltalat / 2) + cos(alat) * cos(blat) * sin(deltalong / 2) * sin(deltalong / 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return earth_radius * c

class CrudTool:
    
    def __init__(self, api_key):
        self.pipedriver = PipeDriver(api_key)        
        self.organizations = self.get_organizations()

    def contains_organization(self, id):
        return id in self.organizations

    def get_organizations(self):
        return self.pipedriver.get_organizations()

    def print_organization(self, id):
        clearprint(self.organizations[id])

    def print_all_organizations(self):
        clearprint('\n'.join(str(self.organizations[id]) for id in sorted(self.organizations.keys())))

    def create_organization(self, name, latitude, longitude):
        organization = self.pipedriver.create_organization(name, latitude, longitude)
        self.organizations[organization.id] = organization

    def edit_organization(self, id, name = None, latitude = None, longitude = None):
        self.organizations[id] = self.pipedriver.update_organization(id, name, latitude, longitude)

    def delete_organization(self, id):
        self.pipedriver.delete_organization(id)

    def find_nearest(self, latitude, longitude):
        # Does distance calculations several times over, for brevity, which isn't horrible seeing how few orgs there likely are.
        sorted_organizations = sorted(self.organizations.values(), key = lambda org: distance((latitude, longitude), (org.latidude, org.longitude)))
        shortest = distance((latitude, longitude), (sorted_organizations[0].latitude, sorted_organizations[0].longitude))
        out = []

        for organization in sorted_organizations:
            if distance((latitude, longitude), (organization.latitude, organization.longitude)) == shortest:
                out.append(organization.id)
            else:
                break

        return out

if __name__ == '__main__':
    print(sConnecting)
    crudtool = CrudTool(api_key)
    print(sSuccessful)
    print(len(crudtool.organizations), sOrgsInDb)
    print(sInstructions)
    
    while True:
        instruction = input().split()
        command = instruction[0]

        if command == 'help':
            clearprint(sInstructions)
            continue
        elif command == 'list':
            crudtool.print_all_organizations()
            continue
        elif command == 'create':
            if len(instruction) > 1:
                print(sInvalid)
            else:
                name = ''
                latitude = 1000.0
                longitude = 1000.0
                
                while not name:
                    print(sEnterName)
                    name = input().strip()
                
                while not latitude_legal(latitude):
                    print(sEnterLatitude)
                    try:
                        latidude = float(input())
                    except:
                        pass

                while not longitude_legal(longitude):
                    print(sEnterLongitude)
                    try:
                        longitude = float(input())
                    except:
                        pass

                crudtool.create_organization(name, latitude, longitude)
                print(sCreationSuccessful)

            continue
        elif command == 'view':
            if len(instruction) == 2:
                if instruction[1].isdigit():
                    id = int(instruction[1])
                    if crudtool.contains_organization(id):
                        crudtool.print_organization(id)
                    else:
                        print(sNotFound.format(id))
                else:
                    print(sInvalid)
            else:
                print(sInvalid)
            continue
        elif command == 'edit':
            if len(instruction) == 2:
                if instruction[1].isdigit():
                    id = int(instruction[1])
                    if crudtool.contains_organization(id):
                        print(sEnterEditName)
                        name = input()                                                
                        
                        latitude = 1000.0
                        longitude = 1000.0

                        while not latitude_legal(latitude):
                            print(sEnterEditLatitude)
                            latString = input()
                            if not latString:
                                break
                            try:
                                latidude = float(latString)
                            except:
                                pass

                        while not longitude_legal(longitude):
                            print(sEnterEditLongitude)
                            longString = input()
                            if not longString:
                                break
                            try:
                                longitude = float(longString)
                            except:
                                pass

                        if not name and not latitude_legal(latitude) and not longitude_legal(longitude):
                            print(sNothingChanged)
                        else:
                            crudtool.edit_organization(id, name or None, latitude if latitude_legal(latitude) else None, longitude if longitude_legal(longitude) else None)
                            print(sEditSuccessful)
                    else:
                        print(sNotFound.format(id))
                else:
                    print(sInvalid)
            else:
                print(sInvalid)
            continue
        elif command == 'delete':
            # Should probably have a confirmation step.
            if len(instruction) == 2:
                if instruction[1].isdigit():
                    id = int(instruction[1])
                    if crudtool.contains_organization(id):
                        crudtool.delete_organization(id)
                        print(sDeletionSuccessful)
                    else:
                        print(sNotFound.format(id))
                else:
                    print(sInvalid)
            else:
                print(sInvalid)
            continue
        elif command == 'find':
            latitude = 1000.0
            longitude = 1000.0

            while not latitude_legal(latitude):
                print(sEnterLatitude)
                try:
                    latidude = float(input())
                except:
                    pass

            while not longitude_legal(longitude):
                print(sEnterLongitude)
                try:
                    longitude = float(input())
                except:
                    pass

            print('\n'.join(crudtool.print_organization(id) for id in crudtool.find_nearest(latitude, longitude)))            
        elif command == 'exit':
            break
        else:
            print('Please enter a valid command')