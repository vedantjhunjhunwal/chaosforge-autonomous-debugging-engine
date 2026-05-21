from chaosforge.db.session import Base, engine
from chaosforge.db import models  # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("ChaosForge database initialized")
