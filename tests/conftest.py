import pytest
from app import create_app
from app.extensions import db
from app.model import Order, Status
from datetime import datetime


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_orders():
    orders = [
        Order(
            name="Order1",
            description="Description1",
            creation_date=datetime(2024, 6, 21, 10, 10, 10),
            status=Status.NEW.value,
        ),
        Order(
            name="Order2",
            description="Description2",
            creation_date=datetime(2024, 6, 22, 15, 15, 15),
            status=Status.IN_PROGRESS.value,
        ),
        Order(
            name="Order3",
            description="Description3",
            creation_date=datetime(2024, 6, 23, 18, 18, 18),
            status=Status.COMPLETED.value,
        ),
    ]

    db.session.bulk_save_objects(orders)
    db.session.commit()

    return orders
