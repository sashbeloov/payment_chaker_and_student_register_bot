import psycopg2



def connection():
    conn = psycopg2.connect(
        dbname="",
        user="postgres",
        password="",
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



