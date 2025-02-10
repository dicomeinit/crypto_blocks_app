from api.routers.v1 import providers
from api.routers.v1 import blocks
from api.routers.v1 import user

routers = [providers.router, blocks.router, user.router]
