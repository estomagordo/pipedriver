from organization import Organization
from pipedriver import PipeDriver
from math import radians, cos, sin, atan2, sqrt

api_key = 'a7098337502aacd4a642156eb8131e48eb8b7d31'
earth_radius = 6371

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

if __name__ == '__main__':
    pipe_driver = PipeDriver(api_key)
    pipe_driver.get_organizations()
    print(distance((53.43, -6.80), (53.414299, -6.830470)))