from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# 1. Definisi Base
# Membuat basis deklaratif untuk mendefinisikan model
Base = declarative_base()

# 2. Tabel Asosiasi (Mata Kuliah ke Mahasiswa melalui Nilai)
# Tabel Nilai/Pendaftaran (Enrollment) adalah tabel asosiasi
# yang membawa data tambahan (nilai/grade).
class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    # Kunci Primer Gabungan
    student_id = Column(ForeignKey('students.id'), primary_key=True)
    course_id = Column(ForeignKey('courses.id'), primary_key=True)
    
    # Data Tambahan
    grade = Column(String(2)) # Contoh: 'A', 'B+', 'C-'
    enrollment_date = Column(DateTime, default=datetime.now)

    # Relationship untuk navigasi (backref: 'enrollments')
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')>"

# 3. Entitas Mahasiswa (Student)
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    nim = Column(String(10), unique=True, nullable=False) # Nomor Induk Mahasiswa
    name = Column(String(100), nullable=False)
    
    # Relationship Many-to-Many melalui tabel asosiasi 'enrollments'
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.id}, nim='{self.nim}', name='{self.name}')>"

# 4. Entitas Mata Kuliah (Course)
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False) # Kode Mata Kuliah
    title = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False) # SKS

    # Relationship Many-to-Many melalui tabel asosiasi 'enrollments'
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.id}, code='{self.code}', title='{self.title}')>"

# ----------------------------------------------------------------------
# 5. Konfigurasi Database dan Contoh Penggunaan
# ----------------------------------------------------------------------

# Inisialisasi Engine (menggunakan SQLite in-memory untuk contoh)
# Untuk database 'hsqldb' atau lainnya, ganti string koneksi ini.
engine = create_engine('sqlite:///:memory:')

# Membuat semua tabel dalam database
Base.metadata.create_all(engine)

# Membuat Session
Session = sessionmaker(bind=engine)
session = Session()

# Contoh Data
student1 = Student(nim='1901001', name='Budi Santoso')
course1 = Course(code='CS101', title='Pemrograman Dasar', credits=3)
course2 = Course(code='MA205', title='Kalkulus I', credits=4)

# Menambahkan entitas utama
session.add_all([student1, course1, course2])
session.commit()

# Contoh Pendaftaran dan Pemberian Nilai (Enrollment)
# Mahasiswa Budi mendaftar ke CS101 dan mendapat nilai A
enroll1 = Enrollment(student=student1, course=course1, grade='A')
# Mahasiswa Budi mendaftar ke MA205 dan mendapat nilai B+
enroll2 = Enrollment(student=student1, course=course2, grade='B+')

session.add_all([enroll1, enroll2])
session.commit()

# 6. Contoh Query (Pengambilan Data)
print("--- Data Mahasiswa ---")
print(session.query(Student).all())

print("\n--- Nilai Budi Santoso ---")
budi = session.query(Student).filter_by(name='Budi Santoso').first()

for e in budi.enrollments:
    print(f"Mata Kuliah: {e.course.title} ({e.course.code}), Nilai: {e.grade}")

session.close()
