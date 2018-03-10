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
exit - exit this program'''

def clear():
    dummy = os.system('cls' if os.name == 'nt' else 'clear')

def clearprint(s):
    clear()
    print(s)

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

    def get_organizations(self):
        return self.pipedriver.get_organizations()

    def print_all(self):
        clearprint('\n'.join(str(self.organizations[id]) for id in sorted(self.organizations.keys())))

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
            crudtool.print_all()
            continue
        elif command == 'create':
            continue
        elif command == 'view':
            continue
        elif command == 'edit':
            continue
        elif command == 'delete':
            continue
        elif command == 'exit':
            break
        else:
            print('Please enter a valid command')