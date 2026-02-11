import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine, Base
from app.models import User, Role, BusinessElement, AccessRoleRule
from app.auth import get_password_hash
from app.config import settings
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Создание ролей...")
    roles = ["admin", "manager", "user", "guest"]
    role_objects = {}
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"{role_name.capitalize()} role")
            db.add(role)
            print(f"Создана роль: {role_name}")
        role_objects[role_name] = role
    db.commit()

    print("\nСоздание бизнес-элементов...")
    elements = ["users", "products", "orders", "stores", "access_rules"]
    element_objects = {}
    for elem_name in elements:
        elem = db.query(BusinessElement).filter(BusinessElement.name == elem_name).first()
        if not elem:
            elem = BusinessElement(name=elem_name, description=f"{elem_name.capitalize()} management")
            db.add(elem)
            print(f"Создан элемент: {elem_name}")
        element_objects[elem_name] = elem
    db.commit()

    print("\nНастройка правил доступа...")
    admin = role_objects["admin"]
    manager = role_objects["manager"]
    user = role_objects["user"]
    guest = role_objects["guest"]

    # Admin - полный доступ
    for elem in element_objects.values():
        db.add(AccessRoleRule(
            role_id=admin.id,
            business_element_id=elem.id,
            read_permission=True, read_all_permission=True,
            create_permission=True, update_permission=True, update_all_permission=True,
            delete_permission=True, delete_all_permission=True
        ))
        print(f"Admin: полный доступ к {elem.name}")
    db.commit()

    # Manager - управление товарами и заказами
    for elem_name in ["products", "orders", "stores"]:
        elem = element_objects[elem_name]
        db.add(AccessRoleRule(
            role_id=manager.id,
            business_element_id=elem.id,
            read_permission=True, read_all_permission=True,
            create_permission=True, update_permission=True, update_all_permission=True,
            delete_permission=False, delete_all_permission=False
        ))
        print(f"Manager: доступ к {elem_name}")
    db.commit()

    # User - базовый доступ
    db.add(AccessRoleRule(
        role_id=user.id,
        business_element_id=element_objects["products"].id,
        read_permission=True, read_all_permission=True,
        create_permission=True, update_permission=True, update_all_permission=False,
        delete_permission=True, delete_all_permission=False
    ))
    db.add(AccessRoleRule(
        role_id=user.id,
        business_element_id=element_objects["orders"].id,
        read_permission=True, read_all_permission=False,
        create_permission=True, update_permission=False, update_all_permission=False,
        delete_permission=False, delete_all_permission=False
    ))
    print(f"User: доступ к продуктам и заказам")
    db.commit()

    # Guest - только чтение товаров
    db.add(AccessRoleRule(
        role_id=guest.id,
        business_element_id=element_objects["products"].id,
        read_permission=True, read_all_permission=True,
        create_permission=False, update_permission=False, update_all_permission=False,
        delete_permission=False, delete_all_permission=False
    ))
    print(f"Guest: чтение продуктов")
    db.commit()

    print("\nСоздание администратора...")
    if not db.query(User).filter(User.email == "admin@example.com").first():
        db.add(User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role_id=admin.id,
            is_active=True
        ))
        print("Админ создан")
    db.commit()

    db.close()
    print("\nБаза данных успешно инициализирована!")
    print("Админ: admin@example.com / admin123")

if __name__ == "__main__":
    init_db()