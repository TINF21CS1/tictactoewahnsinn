import pytest
import user.user as user

def test_user_creation():
    x = user.User("JohnDoe")
    assert x.get_name() == "JohnDoe"
    assert x.get_wins() == 0
    assert x.get_draws() == 0
    assert x.get_losses() == 0


def test_loss():
    x = user.User("JohnDoe")
    x.

def test_win():
    pass

def test_draw():
    pass

def test_user_creation_from_file():
    pass

def test_save_data():
    pass

def test_change_name():
    pass

def delete_profile():
    pass

def change_name():
    pass

def test_make_move():
    pass

