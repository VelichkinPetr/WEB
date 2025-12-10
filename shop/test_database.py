# test_data.py
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
import os

# Добавляем путь к моделям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем все модели
from models.user import User, UserStatus
from models.profile import Profile
from models.category import Category
from models.product import Product
from models.reviews import Review
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.base import Base

# Создаем engine и сессию
engine = create_engine('sqlite:///test_database.db', echo=True)
Base.metadata.create_all(engine)

def create_test_data():
    """Создание тестовых данных для проверки связей"""
    session = Session(engine)
    
    try:
        # 1. Создаем пользователей
        print("Создаем пользователей...")
        admin_user = User(
            email="admin@example.com",
            status=UserStatus.admin,
            is_admin=True
        )
        
        moderator_user = User(
            email="moderator@example.com",
            status=UserStatus.moderator,
            is_admin=False
        )
        
        customer_user = User(
            email="customer@example.com",
            status=UserStatus.moderator,
            is_admin=False
        )
        
        session.add_all([admin_user, moderator_user, customer_user])
        session.flush()
        
        # 2. Создаем профили
        print("Создаем профили...")
        admin_profile = Profile(
            name="Александр",
            surname="Иванов",
            phone="+79001234567",
            birthday=date(1990, 5, 15),
            photo="admin.jpg",
            user_id=admin_user.id
        )
        
        customer_profile = Profile(
            name="Мария",
            surname="Петрова",
            phone="+79007654321",
            birthday=date(1995, 8, 22),
            photo="customer.jpg",
            user_id=customer_user.id
        )
        
        session.add_all([admin_profile, customer_profile])
        session.flush()
        
        # 3. Создаем категории (иерархическая структура)
        print("Создаем категории...")
        
        # Родительские категории
        electronics = Category(
            name="Электроника",
            slug="electronics",
            description="Электронные устройства",
            sort=1
        )
        
        clothing = Category(
            name="Одежда",
            slug="clothing",
            description="Одежда и аксессуары",
            sort=2
        )
        
        session.add_all([electronics, clothing])
        session.flush()
        
        # Дочерние категории
        smartphones = Category(
            name="Смартфоны",
            slug="smartphones",
            description="Мобильные телефоны",
            sort=1,
            parent_id=electronics.id
        )
        
        laptops = Category(
            name="Ноутбуки",
            slug="laptops",
            description="Портативные компьютеры",
            sort=2,
            parent_id=electronics.id
        )
        
        mens_clothing = Category(
            name="Мужская одежда",
            slug="mens-clothing",
            description="Одежда для мужчин",
            sort=1,
            parent_id=clothing.id
        )
        
        womens_clothing = Category(
            name="Женская одежда",
            slug="womens-clothing",
            description="Одежда для женщин",
            sort=2,
            parent_id=clothing.id
        )
        
        session.add_all([smartphones, laptops, mens_clothing, womens_clothing])
        session.flush()
        
        # 4. Создаем продукты
        print("Создаем продукты...")
        
        product1 = Product(
            name="iPhone 15 Pro",
            article="IPH15PRO256",
            preview_text="Новый iPhone 15 Pro",
            detail_text="Флагманский смартфон Apple с камерой 48 МП",
            price=120000
        )
        
        product2 = Product(
            name="Samsung Galaxy S24",
            article="SGS24ULTRA",
            preview_text="Samsung Galaxy S24 Ultra",
            detail_text="Мощный смартфон с S-Pen",
            price=95000
        )
        
        product3 = Product(
            name="MacBook Air M2",
            article="MBAIRM2",
            preview_text="Ноутбук Apple MacBook Air",
            detail_text="Легкий и мощный ноутбук на чипе M2",
            price=115000
        )
        
        product4 = Product(
            name="Джинсы Levi's",
            article="LEVI501",
            preview_text="Классические джинсы",
            detail_text="Прямые джинсы из денима",
            price=4500
        )
        
        product5 = Product(
            name="Футболка Nike",
            article="NKDRYFIT",
            preview_text="Спортивная футболка",
            detail_text="Футболка из дышащей ткани",
            price=2500
        )
        
        session.add_all([product1, product2, product3, product4, product5])
        session.flush()
        
        # 5. Связываем продукты с категориями (многие-ко-многим)
        print("Связываем продукты с категориями...")
        product1.category.extend([electronics, smartphones])
        product2.category.extend([electronics, smartphones])
        product3.category.extend([electronics, laptops])
        product4.category.extend([clothing, mens_clothing])
        product5.category.extend([clothing, womens_clothing])
        
        # 6. Создаем корзины
        print("Создаем корзины...")
        customer_cart = Cart(
            profile_id=customer_profile.id
        )
        
        session.add(customer_cart)
        session.flush()
        
        # 7. Добавляем товары в корзину (через CartItem)
        print("Добавляем товары в корзину...")
        cart_item1 = CartItem(
            count=1,
            product_id=product1.id,
            cart_id=customer_cart.id
        )
        
        cart_item2 = CartItem(
            count=2,
            product_id=product4.id,
            cart_id=customer_cart.id
        )
        
        cart_item3 = CartItem(
            count=1,
            product_id=product5.id,
            cart_id=customer_cart.id
        )
        
        session.add_all([cart_item1, cart_item2, cart_item3])
        
        # 8. Создаем отзывы
        print("Создаем отзывы...")
        review1 = Review(
            rate=5,
            comment="Отличный телефон!",
            product_id=product1.id,
            profile_id=customer_profile.id
        )
        
        review2 = Review(
            rate=4,
            comment="Хорошие джинсы, но маломерят",
            product_id=product4.id,
            profile_id=customer_profile.id
        )
        
        review3 = Review(
            rate=5,
            comment="Лучший ноутбук!",
            product_id=product3.id,
            profile_id=admin_profile.id
        )
        
        session.add_all([review1, review2, review3])
        
        # 9. Создаем заказы
        print("Создаем заказы...")
        order1 = Order(
            status=OrderStatus.processed,
            total_price=120000 + 4500*2 + 2500,  # product1 + 2*product4 + product5
            profile_id=customer_profile.id
        )
        
        session.add(order1)
        session.flush()
        
        # 10. Добавляем товары в заказ (через OrderItem)
        print("Добавляем товары в заказ...")
        order_item1 = OrderItem(
            quantity=1,
            price=120000,
            cost=120000,
            product_id=product1.id,
            order_id=order1.id
        )
        
        order_item2 = OrderItem(
            quantity=2,
            price=4500,
            cost=9000,
            product_id=product4.id,
            order_id=order1.id
        )
        
        order_item3 = OrderItem(
            quantity=1,
            price=2500,
            cost=2500,
            product_id=product5.id,
            order_id=order1.id
        )
        
        session.add_all([order_item1, order_item2, order_item3])
        
        # Сохраняем все изменения
        session.commit()
        
        print("\n" + "="*50)
        print("ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
        print("="*50)
        
        # 11. Проверяем связи
        print("\nПРОВЕРКА СВЯЗЕЙ:")
        print("="*50)
        
        # Проверка User ↔ Profile
        print("1. User ↔ Profile:")
        user = session.query(User).filter_by(email="customer@example.com").first()
        print(f"   Пользователь: {user.email}")
        print(f"   Профиль: {user.profile.name} {user.profile.surname}")
        
        # Проверка Profile ↔ Cart
        print("\n2. Profile ↔ Cart:")
        profile = session.query(Profile).filter_by(name="Мария").first()
        print(f"   Профиль: {profile.name}")
        print(f"   Корзина ID: {profile.cart.id}")
        print(f"   Товаров в корзине: {len(profile.cart.cart_item)}")
        
        # Проверка Cart ↔ CartItem ↔ Product
        print("\n3. Cart ↔ CartItem ↔ Product:")
        cart = session.query(Cart).first()
        print(f"   Корзина ID: {cart.id}")
        for item in cart.cart_item:
            print(f"   - Товар: {item.product.name}, Количество: {item.count}")
        
        # Проверка Category иерархии
        print("\n4. Category иерархия:")
        electronics_cat = session.query(Category).filter_by(name="Электроника").first()
        print(f"   Родительская категория: {electronics_cat.name}")
        print(f"   Дочерние категории: {[child.name for child in electronics_cat.category_child]}")
        
        # Проверка Product ↔ Category (многие-ко-многим)
        print("\n5. Product ↔ Category:")
        product = session.query(Product).filter_by(name="iPhone 15 Pro").first()
        print(f"   Товар: {product.name}")
        print(f"   Категории: {[cat.name for cat in product.category]}")
        
        # Проверка Review
        print("\n6. Review:")
        reviews = session.query(Review).all()
        for rev in reviews:
            print(f"   Отзыв: {rev.product.name} ← {rev.profile.name}: {rev.rate} звезд")
        
        # Проверка Order ↔ OrderItem
        print("\n7. Order ↔ OrderItem:")
        order = session.query(Order).first()
        print(f"   Заказ #{order.id}, Статус: {order.status.value}, Сумма: {order.total_price}")
        for item in order.order_item:
            print(f"   - {item.product.name}: {item.quantity} × {item.price} = {item.cost}")
        
        # Проверка Profile ↔ Order
        print("\n8. Profile ↔ Order:")
        print(f"   Профиль '{profile.name}' имеет {len(profile.order)} заказ(ов)")
        
        # Проверка Product ↔ Reviews
        print("\n9. Product ↔ Reviews:")
        for prod in session.query(Product).all():
            print(f"   {prod.name}: {len(prod.reviews)} отзыв(ов)")
        
        # Проверка Product через CartItem
        print("\n10. Product ↔ CartItem:")
        product_with_cart_items = session.query(Product).filter_by(name="iPhone 15 Pro").first()
        print(f"   Товар '{product_with_cart_items.name}' в {len(product_with_cart_items.cart_item)} корзинах")
        
        # Проверка Product через OrderItem
        print("\n11. Product ↔ OrderItem:")
        product_with_order_items = session.query(Product).filter_by(name="Джинсы Levi's").first()
        print(f"   Товар '{product_with_order_items.name}' в {len(product_with_order_items.order_item)} заказах")
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
        raise
    finally:
        session.close()

def run_tests():
    """Запуск проверок связей"""
    print("Запуск тестов связей...")
    
    session = Session(engine)
    
    try:
        # Проверка всех связей
        test_cases = [
            ("Пользователи", session.query(User).count()),
            ("Профили", session.query(Profile).count()),
            ("Категории", session.query(Category).count()),
            ("Продукты", session.query(Product).count()),
            ("Корзины", session.query(Cart).count()),
            ("Товары в корзинах", session.query(CartItem).count()),
            ("Заказы", session.query(Order).count()),
            ("Товары в заказах", session.query(OrderItem).count()),
            ("Отзывы", session.query(Review).count()),
        ]
        
        print("\n" + "="*50)
        print("СТАТИСТИКА БАЗЫ ДАННЫХ:")
        print("="*50)
        for name, count in test_cases:
            print(f"{name}: {count}")
        
        # Дополнительные проверки
        print("\n" + "="*50)
        print("ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ:")
        print("="*50)
        
        # Проверяем, что у каждого профиля есть корзина
        profiles = session.query(Profile).all()
        for profile in profiles:
            if not hasattr(profile, 'cart') or not profile.cart:
                print(f"⚠️ Профиль {profile.name} не имеет корзины!")
            else:
                print(f"✓ Профиль {profile.name} имеет корзину #{profile.cart.id}")
        
        # Проверяем связи категорий
        categories_with_parents = session.query(Category).filter(Category.parent_id.isnot(None)).all()
        print(f"\nКатегорий с родителями: {len(categories_with_parents)}")
        
        # Проверяем, что у продуктов есть категории
        products_without_categories = []
        for product in session.query(Product).all():
            if len(product.category) == 0:
                products_without_categories.append(product.name)
        
        if products_without_categories:
            print(f"⚠️ Продукты без категорий: {products_without_categories}")
        else:
            print("✓ Все продукты имеют категории")
            
    finally:
        session.close()

if __name__ == "__main__":
    # Очистка базы данных (опционально)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    # Создание тестовых данных
    create_test_data()
    
    # Запуск проверок
    run_tests()
    
    print("\n" + "="*50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("База данных: test_database.db")
    print("="*50)