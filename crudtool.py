import os
from organization import Organization
from pipedriver import PipeDriver
from math import radians, cos, sin, atan2, sqrt

earth_radius = 6371
epsilon = 0.000001

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
sNearestReport = '{0} {1} km away.'


def get_api_key():
    with open('apikey.txt') as f:
        return f.read().strip()


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

    deltalat = blat - alat
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

    def get_organization(self, id):
        return self.organizations[id]

    def print_organization(self, id):
        print(self.organizations[id])

    def print_all_organizations(self):
        print('\n'.join(str(self.organizations[id]) for id in sorted(self.organizations.keys())))

    def create_organization(self, name, latitude, longitude):
        organization = self.pipedriver.create_organization(name, latitude, longitude)
        self.organizations[organization.id] = organization
        return organization

    def edit_organization(self, id, name, latitude, longitude):
        self.organizations[id] = self.pipedriver.update_organization(id, name, latitude, longitude)
        return self.get_organization(id)

    def delete_organization(self, id):
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


def help_command():
    clearprint(sInstructions)


def list_command():
    crudtool.print_all_organizations()


def create_command():
    name = ''
    latitude = 1000.0
    longitude = 1000.0

    while not name:
        print(sEnterName)
        name = input().strip()

    while not latitude_legal(latitude):
        print(sEnterLatitude)
        try:
            latitude = float(input())
        except Exception:
            pass

    while not longitude_legal(longitude):
        print(sEnterLongitude)
        try:
            longitude = float(input())
        except Exception:
            pass

    crudtool.create_organization(name, latitude, longitude)
    print(sCreationSuccessful)


def view_command(instruction):
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


def edit_command(instruction, crudtool):
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
                        latitude = float(latString)
                    except Exception:
                        pass

                while not longitude_legal(longitude):
                    print(sEnterEditLongitude)
                    longString = input()
                    if not longString:
                        break
                    try:
                        longitude = float(longString)
                    except Exception:
                        pass

                if not name and not latitude_legal(latitude) and not longitude_legal(longitude):
                    print(sNothingChanged)
                else:
                    organization = crudtool.get_organization(id)

                    name = name if name else organization.name
                    latitude = latitude if latitude_legal(latitude) else organization.latitude
                    longitude = longitude if longitude_legal(longitude) else organization.longitude

                    crudtool.edit_organization(id, name, latitude, longitude)

                    print(sEditSuccessful)
            else:
                print(sNotFound.format(id))
        else:
            print(sInvalid)
    else:
        print(sInvalid)


def delete_command(instruction):
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


def find_command(crudtool):
    latitude = 1000.0
    longitude = 1000.0

    while not latitude_legal(latitude):
        print(sEnterLatitude)
        try:
            latitude = float(input())
        except Exception:
            pass

    while not longitude_legal(longitude):
        print(sEnterLongitude)
        try:
            longitude = float(input())
        except Exception:
            pass

    for id in crudtool.find_nearest((latitude, longitude)):
        organization = crudtool.get_organization(id)
        d = distance((latitude, longitude), (organization.latitude, organization.longitude))
        print(sNearestReport.format(organization, ('%.2f' % d)))


if __name__ == '__main__':
    api_key = get_api_key()
    print(sConnecting)
    crudtool = CrudTool(api_key)
    print(sSuccessful)
    print(len(crudtool.organizations), sOrgsInDb)
    print(sInstructions)

    while True:
        instruction = input().split()
        command = instruction[0]

        if command == 'help':
            help_command()
        elif command == 'list':
            list_command()
        elif command == 'create':
            create_command()
        elif command == 'view':
            view_command(instruction)
        elif command == 'edit':
            edit_command(instruction, crudtool)
        elif command == 'delete':
            delete_command(instruction)
        elif command == 'find':
            find_command(crudtool)
        elif command == 'exit':
            break
        else:
            print('Please enter a valid command')
