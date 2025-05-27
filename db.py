import psycopg2



def connection():
    conn = psycopg2.connect(
        dbname="student",
        user="postgres",
        password="23",
        port="5432",
        host="localhost"
    )
    return conn

def create_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_info (
                tg_id BIGINT UNIQUE,   
                fio VARCHAR(100),
                phone VARCHAR(20),
                course VARCHAR(100),
                payment_amount NUMERIC DEFAULT 1200000,
                balance NUMERIC DEFAULT 1200000,
                payment_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        return cursor, conn
    except Exception as e:
        return f"Xato: {e}"


def save_info(tg_id, fio, phone, course):
    cursor, conn = create_table()

    cursor.execute('''
        INSERT INTO student_info (tg_id, fio, phone, course)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (tg_id) DO NOTHING
    ''', [tg_id, fio, phone, course])

    conn.commit()
    cursor.close()
    conn.close()


def get_all_students():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM student_info")

        students = cursor.fetchall()
        cursor.close()
        conn.close()

        return students

    except Exception as e:
        return f"Error: {e}"



def delete_student(tg_id=None, phone=None, fio=None):
    try:
        conn = connection()
        cursor = conn.cursor()

        if tg_id:
            if not str(tg_id).isdigit():
                return "Xatolik: tg_id raqam bo‘lishi kerak."
            cursor.execute("DELETE FROM student_info WHERE tg_id = %s", (int(tg_id),))
        elif phone:
            cursor.execute("DELETE FROM student_info WHERE phone = %s", (phone,))
        elif fio:
            cursor.execute("DELETE FROM student_info WHERE fio = %s", (fio,))
        else:
            return "Xatolik: tg_id yoki phone yoki fio qiymati berilishi kerak."

        conn.commit()
        cursor.close()
        conn.close()
        return "Foydalanuvchi muvaffaqiyatli o‘chirildi."

    except Exception as e:
        return f"Xatolik: {e}"



def create_super_admins_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS super_admins (
                tg_id BIGINT UNIQUE
            )
        ''')
        conn.commit()
        return cursor, conn
    except Exception as e:
        return None, f"Xato: {e}"  # doimo 2ta qiymat qaytariladi



def add_super_admin(tg_id):
    cursor, conn = create_super_admins_table()

    if cursor is None:
        return conn  # bu yerda `conn`da xatolik matni bo'ladi

    try:
        cursor.execute("INSERT INTO super_admins (tg_id) VALUES (%s) ON CONFLICT DO NOTHING", (tg_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return f"Xato: {e}"


def get_super_admin():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM super_admins")
        admins = cursor.fetchall()

        cursor.close()
        conn.close()

        return admins

    except Exception as e:
        return f"Error: {e}"



# def find_user(tg_id=None, phone=None, fio=None):
#     try:
#         # if not (tg_id or phone or fio):
#         #     return []  # hech qanday parametr berilmagan
#         conn = connection()
#         cursor = conn.cursor()
#         print(tg_id,tg_id,fio)
#
#         if tg_id:
#             cursor.execute("SELECT * FROM student_info WHERE tg_id ILIKE %s", (f"%{tg_id}%",))
#         elif phone:
#             cursor.execute("SELECT * FROM student_info WHERE phone ILIKE %s", (f"%{phone}%",))
#         elif fio:
#             cursor.execute("SELECT * FROM student_info WHERE fio ILIKE %s", (f"%{fio}%",))
#
#         result = cursor.fetchall()
#         cursor.close()
#         conn.close()
#
#         return result
#
#     except Exception as e:
#         print(f"Xato: {e}")
#         return []


def find_user(tg_id=None, phone=None, fio=None):
    try:
        conn = connection()
        cursor = conn.cursor()

        if tg_id:
            cursor.execute("SELECT * FROM student_info WHERE CAST(tg_id AS TEXT) ILIKE %s", (f"%{tg_id}%",))
        elif phone:
            cursor.execute("SELECT * FROM student_info WHERE phone ILIKE %s", (f"%{phone}%",))
        elif fio:
            cursor.execute("SELECT * FROM student_info WHERE fio ILIKE %s", (f"%{fio}%",))

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    except Exception as e:
        print(f"Xato: {e}")
        return []
