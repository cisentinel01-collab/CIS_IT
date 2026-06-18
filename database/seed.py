from models.user import User
from models.supplier import Supplier
from models.item import Item
from models.location import Location
from database.db_manager import DBManager
import bcrypt

def seed_data():
    db = DBManager()

    # 1. Users
    user_model = User()
    users = [
        {"username": "admin", "password": "admin", "full_name": "المدير العام", "role": "admin"},
        {"username": "keeper", "password": "keeper", "full_name": "أمين المخزن", "role": "warehouse_keeper"},
        {"username": "supervisor", "password": "supervisor", "full_name": "المشرف", "role": "supervisor"}
    ]
    for u in users:
        if not db.execute_query("SELECT id FROM users WHERE username = ?", (u['username'],)):
            user_model.create_user(u)

    # 2. Locations
    loc_model = Location()
    locations = ["مخزن رئيسي", "رف A1", "رف A2", "منطقة الشحن", "ثلاجة التخزين"]
    for l in locations:
        if not db.execute_query("SELECT id FROM locations WHERE name = ?", (l,)):
            loc_model.create({"name": l, "description": "موقع تخزين افتراضي"})

    # 3. Suppliers
    supplier_model = Supplier()
    suppliers = [
        {"name": "شركة الملاحة العربية", "phone": "0123456789", "email": "info@arabmarine.com", "address": "الإسكندرية، مصر"},
        {"name": "مورد الخليج للخدمات", "phone": "9876543210", "email": "sales@gulfserv.com", "address": "دبي، الإمارات"},
        {"name": "الشركة العالمية لقطع الغيار", "phone": "5551234", "email": "parts@global.com", "address": "القاهرة، مصر"},
        {"name": "خدمات الدعم اللوجستي", "phone": "4443322", "email": "support@logistic.com", "address": "جدة، السعودية"}
    ]
    for s in suppliers:
        if not db.execute_query("SELECT id FROM suppliers WHERE name = ?", (s['name'],)):
            supplier_model.create(s)

    # 4. Items
    item_model = Item()
    loc_id = db.execute_query("SELECT id FROM locations LIMIT 1")[0]['id']
    items = [
        {"code": "ENG-001", "name": "محرك ديزل بحري 500 حصان", "category": "محركات", "unit": "قطعة", "location_id": loc_id, "min_stock": 2, "current_stock": 5},
        {"code": "OIL-050", "name": "زيت محرك هيدروليك 20 لتر", "category": "زيوت", "unit": "جالون", "location_id": loc_id, "min_stock": 10, "current_stock": 50},
        {"code": "BRG-202", "name": "رولمان بلي مقاس 202", "category": "قطع غيار", "unit": "قطعة", "location_id": loc_id, "min_stock": 20, "current_stock": 100},
        {"code": "FLT-99", "name": "فلتر وقود أصلي", "category": "فلاتر", "unit": "قطعة", "location_id": loc_id, "min_stock": 15, "current_stock": 30},
        {"code": "CAB-10", "name": "كابلات كهرباء بحرية 10 ملم", "category": "كهرباء", "unit": "متر", "location_id": loc_id, "min_stock": 100, "current_stock": 500}
    ]
    for i in items:
        if not db.execute_query("SELECT id FROM items WHERE code = ?", (i['code'],)):
            item_model.create(i)

    print("Data seeding completed successfully.")

if __name__ == "__main__":
    seed_data()
