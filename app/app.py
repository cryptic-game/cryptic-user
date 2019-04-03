from objects_db import base, engine
from resources.handle import m

if __name__ == '__main__':
    base.metadata.create_all(bind=engine)
    m.run()
