import pytest
from crudtool import CrudTool


def get_api_key():
    with open('apikey.txt') as f:
        return f.read().strip()


def connect_test():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    assert(True)


def create_and_delete_test():
    api_key = get_api_key()
    crudtool = CrudTool(api_key)

    pre_count = len(crudtool.get_organizations())
    new_id = crudtool.create_organization('testing, just testing', 0.0, 0.2).id
    create_count = len(crudtool.get_organizations())
    crudtool.delete_organization(new_id)
    delete_count = len(crudtool.get_organizations())

    assert(create_count == pre_count + 1)
    assert(delete_count == pre_count)
