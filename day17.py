#       学生管理系统
import pymysql
from aiosqlite import cursor
from fastapi import FastAPI
from pydantic import BaseModel
from pymysql.cursors import DictCursor


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user='root',
        password="1234",
        database='student_db',
        cursorclass=DictCursor
    )

app=FastAPI(
    title="学生管理系统",
    version="0.128.0",
)

class Student(BaseModel):
    name: str
    age: int
    major: str

@app.get("/students/search")
def mohu_select_student(name: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM students WHERE name LIKE %s"
        cursor.execute(sql, (f"%{name}%",))
        students = cursor.fetchall()
        if students:
            return {"data": students}     # 统一返回格式
        return {"error": "学生不存在"}
    finally:
        conn.close()

@app.post("/students/batch")
def batch_add_students(students: list[Student]):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO students (name, age, major) VALUES (%s, %s, %s)"
        values = [(s.name, s.age, s.major) for s in students]
        cursor.executemany(sql, values)
        conn.commit()
        return {"msg": "批量添加成功", "count": len(students)}
    finally:
        conn.close()

@app.get("/students")
def get_all_students():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return {"data": cursor.fetchall()}
    finally:
        conn.close()

@app.get("/students/get_total_avg")
def get_total_avg():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) as total,round(avg(age),2) as avg_ageFROM students")
        return {"data": cursor.fetchone()}
    finally:
        conn.close()



@app.get("/students/{stu_id}")
def get_one_student(stu_id:int):
    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM students WHERE stu_id=%s",(stu_id,))
    student=cursor.fetchone()
    conn.close()
    if student:
        return student
    return {"error":"学生不存在"}

@app.post("/students")
def add_student(stu:Student):
    conn=get_db_connection()
    cursor= conn.cursor()
    sql="INSERT INTO students (name,age,major) VALUES (%s,%s,%s)"
    cursor.execute(sql,(stu.name,stu.age,stu.major))
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    return {"msg":"添加成功","stu_id":new_id}


@app.put("/students/{stu_id}")
def update_student(stu_id:int,stu:Student):
    conn=get_db_connection()
    cursor = conn.cursor()
    sql="UPDATE students SET name=%s,age=%s,major=%s WHERE stu_id=%s"
    cursor.execute(sql,(stu.name,stu.age,stu.major,stu_id))
    conn.commit()
    conn.close()
    return {"msg":"修改成功"}

@app.delete("/students/{stu_id}")
def delete_student(stu_id:int):
    conn=get_db_connection()
    cursor= conn.cursor()
    sql="DELETE FROM students WHERE stu_id=%s"
    cursor.execute(sql,(stu_id,))
    conn.commit()
    conn.close()
    return {"msg":"删除成功"}



