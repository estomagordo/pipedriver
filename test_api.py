import pytest
from orgmanager import OrgManager


@pytest.fixture
def orgmanager():
    return OrgManager()


def test_connect(orgmanager):
    orgmanager = OrgManager()

    assert(True)


def test_create_and_delete(orgmanager):
    pre_count = len(orgmanager.get_all())
    new_id = orgmanager.create('testing, just testing', 0.0, 0.2).id
    create_count = len(orgmanager.get_all())
    orgmanager.delete(new_id)
    delete_count = len(orgmanager.get_all())

    assert(create_count == pre_count + 1)
    assert(delete_count == pre_count)


def test_update(orgmanager):
    id = orgmanager.create('testing, just testing', 0.0, 0.2).id

    new_name = 'new testing'
    new_lat = 14.15
    new_long = 15.14

    orgmanager.edit(id, new_name, new_lat, new_long)

    organization = orgmanager.get(id)

    orgmanager.delete(id)

    assert(organization.name == new_name)
    assert(organization.latitude == new_lat)
    assert(organization.longitude == new_long)


def test_may_return_multiple_nearest(orgmanager):
    id1 = orgmanager.create('testing 1', 75.75, -76.0).id
    id2 = orgmanager.create('testing 2', 75.75, -76.20).id

    nearest = orgmanager.find_nearest((75.75, -76.10))

    orgmanager.delete(id1)
    orgmanager.delete(id2)

    assert(len(nearest) == 2)
    