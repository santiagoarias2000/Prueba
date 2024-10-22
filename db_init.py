import sqlite3

# Ruta para las bases de datos (debe ser consistente en todos los scripts)
PRODUCTS_DB = 'products.db'
ORDERS_DB = 'orders.db'

def init_db():
    # Inicializa la base de datos de productos
    with sqlite3.connect(PRODUCTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL
            )
        """)
        print("Tabla 'products' creada o ya existe.")
        conn.commit()

    # Inicializa la base de datos de pedidos
    with sqlite3.connect(ORDERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        print("Tabla 'orders' creada o ya existe.")
        conn.commit()

if __name__ == "__main__":
    init_db()
