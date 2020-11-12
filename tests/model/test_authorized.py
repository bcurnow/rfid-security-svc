from unittest.mock import patch

import rfidsecuritysvc.model.authorized as model
from rfidsecuritysvc.exception import PermissionNotFoundError, AssociationNotFoundError
from rfidsecuritysvc.model.association import Association


@patch('rfidsecuritysvc.model.authorized.association')
def test_authorized(association):
    association.get.return_value = Association('test', 'test_perm')
    assert model.authorized('test', 'test_perm') is True
    association.get.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.association')
def test_authorized_false(association):
    association.get.return_value = None
    assert model.authorized('test', 'test_perm') is False
    association.get.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.association')
def test_authorized_invalid_perm_name(association):
    association.get.side_effect = PermissionNotFoundError
    assert model.authorized('test', 'test_perm') is False
    association.get.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.association')
def test_authorized_invalid_media_id(association):
    association.get.side_effect = AssociationNotFoundError
    assert model.authorized('test', 'test_perm') is False
    association.get.assert_called_once_with('test', 'test_perm')
