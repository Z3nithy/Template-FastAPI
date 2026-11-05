import os


os.environ["SECRET_KEY"] = "test-secret-key-with-at-least-32-characters"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["ALGORITHM"] = "HS256"
os.environ["DEBUG"] = "false"
