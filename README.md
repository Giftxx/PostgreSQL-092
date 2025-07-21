# 📦 PostgreSQL & SQLAlchemy - 6510110092

ระบบจัดการฐานข้อมูลด้วย PostgreSQL และเชื่อมต่อผ่าน SQLAlchemy บนภาษา Python

## 🚀 เทคโนโลยีที่ใช้

* **PostgreSQL** – ระบบฐานข้อมูลฟรีและเสถียร รองรับข้อมูลหลากหลาย
* **PGAdmin** – เครื่องมือ GUI สำหรับจัดการ PostgreSQL
* **SQLAlchemy** – ไลบรารีเชื่อมฐานข้อมูลผ่าน Python รองรับ ORM

## ✅ จุดเด่นของ PostgreSQL

* รองรับมาตรฐาน SQL และความปลอดภัยแบบ ACID
* จัดการข้อมูลได้ทั้งแบบมีโครงสร้าง (ตาราง) และไม่มีโครงสร้าง (JSON)
* รองรับการทำงานพร้อมกันหลายผู้ใช้
* ขยายความสามารถด้วย Extensions (เช่น PostGIS, TimescaleDB)
* เชื่อมต่อกับภาษาโปรแกรมยอดนิยม เช่น Python, R

## ⚠️ ข้อควรระวัง

* การตั้งค่าเริ่มต้นค่อนข้างซับซ้อน
* ทำงานบน Windows อาจไม่เสถียรเท่า Linux
* การปรับจูนประสิทธิภาพต้องใช้ความรู้เฉพาะ

## 🛠️ ตัวอย่างคำสั่ง SQL พื้นฐาน

```sql
-- เพิ่มข้อมูล
INSERT INTO Activities (id, name, description, created_date, updated_date)
VALUES (7, 'Watch Tutorial', 'Learn PostgreSQL', now(), now());

-- แก้ไขข้อมูล
UPDATE Activities
SET name = 'Practice PostgreSQL', updated_date = now()
WHERE id = 6;

-- ลบข้อมูล
DELETE FROM Activities WHERE id = 7;
```

## SQLAlchemy คืออะไร?

SQLAlchemy คือไลบรารีที่ช่วยให้เขียน Python ติดต่อฐานข้อมูลได้ง่ายขึ้น โดยมี 2 รูปแบบการใช้งาน:

* **Core**: เขียน SQL ด้วย Python Syntax
* **ORM**: เขียนเชิงวัตถุ (OOP) ใช้ Class แทน Table

ตัวอย่าง ORM:

```python
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

## 📸 Checkpoints

* แสดงการติดตั้งและรัน PostgreSQL / PGAdmin
* แสดงการเพิ่ม แก้ไข ลบข้อมูล
* ใช้ SQLAlchemy จัดการข้อมูล

---

หากคุณต้องการให้เพิ่มรูปภาพ, badge (เช่น version, license), หรือคำอธิบายเพิ่มเติมเกี่ยวกับการติดตั้ง/รันโค้ด – แจ้งได้เลยครับ!
