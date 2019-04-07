from cryptic import MicroService

from objects import Base, engine

m: MicroService = MicroService(name="user")

if __name__ == '__main__':
    from models.profile import Profile
    from resources.handle import *

    Base.metadata.create_all(bind=engine)

    m.run()
