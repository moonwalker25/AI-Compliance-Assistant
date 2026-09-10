from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint


class Base(DeclarativeBase):
    pass

#TODO: REMOVE AFTER MIGRATING RETRIEVAL ENGINE
class Compliance(Base):
    __tablename__ = "compliance"

    id = Column(Integer, primary_key=True, index=True)

    country = Column(String)

    industry = Column(String)

    regulation = Column(String)

    description = Column(String)

class Industry(Base):
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)

    industry_name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    _table_args_=(
        UniqueConstraint(
            "country",
            "industry_name",
            name="unique_country_industry"
        ),
    )


class Act(Base):
    __tablename__ = "acts"

    id = Column(Integer, primary_key=True, index=True)
    
    act_name = Column(String, nullable=False)

    country = Column(String, nullable=False)


    particulars = relationship(
        "ComplianceParticular",
        back_populates="act"
    )

class ComplianceParticular(Base):
    __tablename__ = "compliance_particulars"

    id = Column(Integer, primary_key=True, index=True)

    act_id = Column(Integer, ForeignKey("acts.id"))

    particular = Column(String, nullable=False)

    description = Column(String)

    csv_id = Column(
        Integer,
        unique=True,
        nullable=False
    )
    compliance_key = Column(
        String,
        nullable=False
    )

    act = relationship(
        "Act",
        back_populates="particulars"
    )

class IndustryActMapping(Base):
    __tablename__ = "industry_act_mapping"

    id = Column(Integer, primary_key=True, index=True)

    industry_name = Column(String, nullable=False)

    country = Column(String, nullable=False)

    act_name = Column(String, nullable=False)

class MappingSuggestion(Base):
    __tablename__ = "mapping_suggestions"

    id = Column(Integer, primary_key=True, index=True)

    country = Column(String, nullable=False)

    industry = Column(String, nullable=False)

    suggested_act = Column(String, nullable=False)

    ai_reason = Column(String)

    confidence = Column(Integer)

    status = Column(
        String,
        default="PENDING"
    )