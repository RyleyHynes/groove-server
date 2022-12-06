# __init__.py files make python dictionaries into python packages
from .auth import login_user
from .auth import register_user
from .stage import StageView
from .artist import ArtistView
from .show import ShowView
from .my_lineup import MyLineupView
from .profile import ProfileView
from .deactivate import DeactivateView
from .demote import DemoteView