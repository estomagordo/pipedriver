import os
from orgmanager import OrgManager
from sys import exit

sInstructions = '''Command list:

help - repeat this message
list - list all organizations
create - create new organization
view [id] - view organization [id]
edit [id] - edit organization [id]
delete [id] - delete organization [id]
find - find the nearest organization(s) for coordinates
exit - exit this program
'''
sConnecting = 'Connecting to Pipe Drive\n'
sSuccessful = 'Successful!\n'
sOrgsInDb = 'organizations in database.\n'
sInvalid = 'Invalid command, please try again.'
sEnterName = 'Please enter a name.'
sEnterLatitude = 'Please enter a valid latitude.'
sEnterLongitude = 'Please enter a valid longitude.'
sCreationSuccessful = 'Creation successful!'
sNotFound = 'Organization with id {0} not found.'
sDeletionSuccessful = 'Deletion successful!'
sEnterEditName = 'Enter new name. Press enter to keep as is.'
sEnterEditLatitude = 'Enter new latitude. Press enter to keep as is.'
sEnterEditLongitude = 'Enter new longitude. Press enter to keep as is.'
sNothingChanged = 'Nothing changed. Update skipped.'
sEditSuccessful = 'Edit successful!'
sNearestReport = '{0} {1} km away.'
sConnectionFailed = 'Connection to Pipe Drive failed. Please try again later.'
sDeleteConfirm = 'Are you sure you want to delete {0} (y/n)?'
sDeletionSkipped = 'Deletion skipped.'


class CrudTool:
    def __init__(self):
        print(sConnecting)
        try:
            self.orgmanager = OrgManager()
        except Exception:
            print(sConnectionFailed)
            exit(1)

        print(sSuccessful)
        print(self.orgmanager.count(), sOrgsInDb)

    def run(self):
        print(sInstructions)

        while True:
            instruction = input().split()
            command = instruction[0]

            if command == 'help':
                self.help_command()
            elif command == 'list':
                self.list_command()
            elif command == 'create':
                self.create_command()
            elif command == 'view':
                self.view_command(instruction)
            elif command == 'edit':
                self.edit_command(instruction)
            elif command == 'delete':
                self.delete_command(instruction)
            elif command == 'find':
                self.find_command()
            elif command == 'exit':
                break
            else:
                print('Please enter a valid command')

    def clear(self):
        dummy = os.system('cls' if os.name == 'nt' else 'clear')

    def clearprint(self, s):
        self.clear()
        print(s)

    def lat_legal(self, latitude):
        return -90.0 <= latitude <= 90.0

    def long_legal(self, longitude):
        return -180.0 <= longitude <= 180.0

    def help_command(self):
        self.clearprint(sInstructions)

    def list_command(self):
        organizations = self.orgmanager.get_all()
        print('\n'.join(map(str, organizations)))

    def create_command(self):
        name = ''  # Some arbitrary invalid value
        latitude = 1000.0  # Some arbitrary invalid value
        longitude = 1000.0  # Some arbitrary invalid value

        while not name:
            print(sEnterName)
            name = input().strip()

        while not self.lat_legal(latitude):
            print(sEnterLatitude)
            try:
                latitude = float(input())
            except Exception:
                pass

        while not self.long_legal(longitude):
            print(sEnterLongitude)
            try:
                longitude = float(input())
            except Exception:
                pass

        try:
            self.orgmanager.create(name, latitude, longitude)
            print(sCreationSuccessful)
        except Exception:
            print(sConnectionFailed)
            exit(1)

    def view_command(self, instruction):
        if len(instruction) != 2 or not instruction[1].isdigit():
            print(sInvalid)
            return

        id = int(instruction[1])

        if self.orgmanager.contains(id):
            print(self.orgmanager.get(id))
        else:
            print(sNotFound.format(id))

    def edit_command(self, instruction):
        if len(instruction) != 2 or not instruction[1].isdigit():
            print(sInvalid)
            return

        id = int(instruction[1])

        if not self.orgmanager.contains(id):
            print(sNotFound.format(id))
            return

        print(sEnterEditName)

        name = input()
        latitude = 1000.0  # Some arbitrary invalid value
        longitude = 1000.0  # Some arbitrary invalid value

        while not self.lat_legal(latitude):
            print(sEnterEditLatitude)
            latString = input()
            if not latString:
                break
            try:
                latitude = float(latString)
            except Exception:
                pass

        while not self.long_legal(longitude):
            print(sEnterEditLongitude)
            longString = input()
            if not longString:
                break
            try:
                longitude = float(longString)
            except Exception:
                pass

        changed = name or self.lat_legal(latitude) or self.long_legal(longitude)

        if not changed:
            print(sNothingChanged)
            return

        organization = self.orgmanager.get(id)

        name = name if name else organization.name
        latitude = latitude if self.lat_legal(latitude) else organization.latitude
        longitude = longitude if self.long_legal(longitude) else organization.longitude

        try:
            self.orgmanager.edit(id, name, latitude, longitude)
            print(sEditSuccessful)
        except Exception:
            print(sConnectionFailed)
            exit(1)

    def delete_command(self, instruction):
        if len(instruction) != 2 or not instruction[1].isdigit():
            print(sInvalid)
            return

        id = int(instruction[1])

        if not self.orgmanager.contains(id):
            print(sNotFound.format(id))
            return

        confirmation = ''

        while confirmation not in ['Y', 'y', 'N', 'n']:
            print(sDeleteConfirm.format(self.orgmanager.get(id).name))
            confirmation = input().strip()

        if confirmation in ['N', 'n']:
            print(sDeletionSkipped)
            return

        try:
            self.orgmanager.delete(id)
            print(sDeletionSuccessful)
        except Exception:
            print(sConnectionFailed)
            exit(1)

    def find_command(self):
        latitude = 1000.0  # Some arbitrary invalid value
        longitude = 1000.0  # Some arbitrary invalid value

        while not self.lat_legal(latitude):
            print(sEnterLatitude)
            try:
                latitude = float(input())
            except Exception:
                pass

        while not self.long_legal(longitude):
            print(sEnterLongitude)
            try:
                longitude = float(input())
            except Exception:
                pass

        point = (latitude, longitude)
        shortest_distance, nearest_organizations = self.orgmanager.find_nearest(point)

        for organization in nearest_organizations:
            print(sNearestReport.format(organization, ('%.2f' % shortest_distance)))


if __name__ == '__main__':
    crudtool = CrudTool()
    crudtool.run()
