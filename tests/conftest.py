import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.notes_manager.database import Base
from src.notes_manager.dependencies.database import get_db
from src.notes_manager.main import app
from src.notes_manager.models.user import User, UserRole
from src.notes_manager.services.auth_service import hash_password, create_access_token

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def test_users(db_session):
    users = [
        User(
            email="admin@test.com",
            username="admin",
            first_name="Admin",
            last_name="User",
            hashed_password=hash_password("password123"),
            role=UserRole.admin,
        ),
        User(
            email="editor@test.com",
            username="editor",
            first_name="Editor",
            last_name="User",
            hashed_password=hash_password("password123"),
            role=UserRole.editor,
        ),
        User(
            email="user@test.com",
            username="regular",
            first_name="Regular",
            last_name="User",
            hashed_password=hash_password("password123"),
            role=UserRole.user,
        ),
    ]
    for user in users:
        db_session.add(user)
    db_session.commit()
    for user in users:
        db_session.refresh(user)
    return users


@pytest.fixture()
def admin_token(test_users):
    admin = test_users[0]
    return create_access_token(admin.id, admin.role.value)


@pytest.fixture()
def editor_token(test_users):
    editor = test_users[1]
    return create_access_token(editor.id, editor.role.value)


@pytest.fixture()
def user_token(test_users):
    user = test_users[2]
    return create_access_token(user.id, user.role.value)
