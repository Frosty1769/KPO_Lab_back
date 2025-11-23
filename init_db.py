"""
Скрипт инициализации базы данных
Создаёт таблицы и добавляет дефолтного администратора
"""

from app import app, db
from model.model import User

def init_db():
    with app.app_context():
        # Создание таблиц
        db.create_all()
        print("✓ Таблицы созданы")
        
        # Проверка существования админа
        admin = db.session.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            # Создание администратора по умолчанию
            admin = User(username='admin', password='admin', role='admin')
            db.session.add(admin)
            db.session.commit()
            print("✓ Создан администратор по умолчанию (логин: admin, пароль: admin)")
        else:
            print("✓ Администратор уже существует")
        
        print("\n=== База данных готова к работе ===")

if __name__ == '__main__':
    init_db()
