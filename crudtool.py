import os
from orgmanager import OrgManager

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


def clear():
    dummy = os.system('cls' if os.name == 'nt' else 'clear')


def clearprint(s):
    clear()
    print(s)


def latitude_legal(latitude):
    return -90.0 <= latitude <= 90.0


def longitude_legal(longitude):
    return -180.0 <= longitude <= 180.0


def help_command():
    clearprint(sInstructions)


def list_command(orgmanager):
    orgmanager.print_all()


def create_command(orgmanager):
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

    orgmanager.create(name, latitude, longitude)
    print(sCreationSuccessful)


def view_command(orgmanager, instruction):
    if len(instruction) == 2:
        if instruction[1].isdigit():
            id = int(instruction[1])
            if orgmanager.contains(id):
                orgmanager.print(id)
            else:
                print(sNotFound.format(id))
        else:
            print(sInvalid)
    else:
        print(sInvalid)


def edit_command(orgmanager, instruction):
    if len(instruction) == 2:
        if instruction[1].isdigit():
            id = int(instruction[1])
            if orgmanager.contains(id):
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
                    organization = orgmanager.get(id)

                    name = name if name else organization.name
                    latitude = latitude if latitude_legal(latitude) else organization.latitude
                    longitude = longitude if longitude_legal(longitude) else organization.longitude

                    orgmanager.edit(id, name, latitude, longitude)

                    print(sEditSuccessful)
            else:
                print(sNotFound.format(id))
        else:
            print(sInvalid)
    else:
        print(sInvalid)


def delete_command(orgmanager, instruction):
    # Should probably have a confirmation step.
    if len(instruction) == 2:
        if instruction[1].isdigit():
            id = int(instruction[1])
            if orgmanager.contains(id):
                orgmanager.delete(id)
                print(sDeletionSuccessful)
            else:
                print(sNotFound.format(id))
        else:
            print(sInvalid)
    else:
        print(sInvalid)


def find_command(orgmanager):
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

    for id in orgmanager.find_nearest((latitude, longitude)):
        organization = orgmanager.get(id)
        d = distance((latitude, longitude), (organization.latitude, organization.longitude))
        print(sNearestReport.format(organization, ('%.2f' % d)))


if __name__ == '__main__':
    print(sConnecting)
    orgmanager = OrgManager()
    print(sSuccessful)
    print(orgmanager.count(), sOrgsInDb)
    print(sInstructions)

    while True:
        instruction = input().split()
        command = instruction[0]

        if command == 'help':
            help_command()
        elif command == 'list':
            list_command(orgmanager)
        elif command == 'create':
            create_command(orgmanager)
        elif command == 'view':
            view_command(orgmanager, instruction)
        elif command == 'edit':
            edit_command(orgmanager, instruction)
        elif command == 'delete':
            delete_command(orgmanager, instruction)
        elif command == 'find':
            find_command(orgmanager)
        elif command == 'exit':
            break
        else:
            print('Please enter a valid command')
