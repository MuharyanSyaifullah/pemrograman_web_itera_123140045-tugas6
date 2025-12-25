from sqlalchemy import Column, Integer, Text
from sqlalchemy.schema import UniqueConstraint

from .meta import Base


class Matakuliah(Base):
    __tablename__ = "matakuliah"
    __table_args__ = (UniqueConstraint("kode_mk", name="uq_matakuliah_kode_mk"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_mk = Column(Text, nullable=False, unique=True)
    nama_mk = Column(Text, nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "kode_mk": self.kode_mk,
            "nama_mk": self.nama_mk,
            "sks": self.sks,
            "semester": self.semester,
        }
