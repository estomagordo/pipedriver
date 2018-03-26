import pytest
from crudtool import CrudTool


def get_api_key():
    with open('apikey.txt') as f:
        return f.read().strip()


def test_connect():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    assert(True)


def test_create_and_delete():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    pre_count = len(crudtool.get_organizations())
    new_id = crudtool.create_organization('testing, just testing', 0.0, 0.2).id
    create_count = len(crudtool.get_organizations())
    crudtool.delete_organization(new_id)
    delete_count = len(crudtool.get_organizations())

    assert(create_count == pre_count + 1)
    assert(delete_count == pre_count)


def test_update():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    id = crudtool.create_organization('testing, just testing', 0.0, 0.2).id

    new_name = 'new testing'
    new_lat = 14.15
    new_long = 15.14

    crudtool.edit_organization(id, new_name, new_lat, new_long)

    organization = crudtool.get_organization(id)

    crudtool.delete_organization(id)

    assert(organization.name == new_name)
    assert(organization.latitude == new_lat)
    assert(organization.longitude == new_long)


def test_may_return_multiple_nearest():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    id1 = crudtool.create_organization('testing 1', 75.75, -76.0).id
    id2 = crudtool.create_organization('testing 2', 75.75, -76.20).id

    nearest = crudtool.find_nearest((75.75, -76.10))

    crudtool.delete_organization(id1)
    crudtool.delete_organization(id2)

    assert(len(nearest) == 2)
    