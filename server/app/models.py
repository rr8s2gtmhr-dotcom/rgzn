from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, func
from .database import Base


class Menu(Base):
    __tablename__ = "sys_menus"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=True)
    path = Column(String(255), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    component = Column(String(255), default="")
    redirect = Column(String(255), default="")
    menuType = Column("menu_type", String(20), default="menu")
    menuSort = Column("menu_sort", Integer, default=0)
    btnPower = Column("btn_power", String(100), default="")
    meta = Column(JSON, default=dict)


class Unit(Base):
    __tablename__ = "sys_units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    deptName = Column("dept_name", String(100), nullable=False)
    deptShortName = Column("dept_short_name", String(50), default="")
    expireTime = Column("expire_time", String(30), default="")


class Role(Base):
    __tablename__ = "sys_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    roleName = Column("role_name", String(100), nullable=False)
    dataScope = Column("data_scope", String(50), default="")
    code = Column(String(50), nullable=False, unique=True, index=True)
    menuPaths = Column("menu_paths", JSON, default=list)
    btnPermissions = Column("btn_permissions", JSON, default=list)


class User(Base):
    __tablename__ = "sys_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column("user_name", String(100), nullable=False, unique=True, index=True)
    passwordHash = Column("password_hash", String(255), nullable=False)
    realName = Column("real_name", String(100), default="")
    phone = Column(String(30), default="")
    status = Column(Boolean, default=True)
    unitId = Column("unit_id", Integer, nullable=True)
    roleIds = Column("role_ids", JSON, default=list)


class UserSetting(Base):
    __tablename__ = "sys_user_settings"
    userId = Column("user_id", Integer, primary_key=True)
    settings = Column(JSON, default=dict)
    updatedAt = Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now())


class Relarder(Base):
    __tablename__ = "biz_relarders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceNo = Column("device_no", String(100), nullable=False, index=True)
    factory = Column(String(100), default="")
    model = Column(String(100), default="")
    address = Column(String(255), default="")
    trackNo = Column("track_no", String(50), default="")
    enableTime = Column("enable_time", String(30), default="")
    damageTime = Column("damage_time", String(30), default="")
    remark = Column(Text, default="")


class Detection(Base):
    __tablename__ = "biz_detections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    relarderNo = Column("relarder_no", String(100), nullable=False, index=True)
    trackNo = Column("track_no", String(50), default="")
    installHeight = Column("install_height", String(50), default="")
    fastPressure = Column("fast_pressure", String(50), default="")
    slowPressure = Column("slow_pressure", String(50), default="")
    returnTime = Column("return_time", String(50), default="")
    gapWidth = Column("gap_width", String(50), default="")
    frontImage = Column("front_image", Text, default="")
    testTime = Column("test_time", String(30), default="")
    detector = Column(String(100), default="")


class Maintain(Base):
    __tablename__ = "biz_maintains"
    id = Column(Integer, primary_key=True, autoincrement=True)
    relarderNo = Column("relarder_no", String(100), nullable=False, index=True)
    maintainTime = Column("maintain_time", String(30), default="")
    maintainProject = Column("maintain_project", String(255), default="")
    maintainUser = Column("maintain_user", String(100), default="")


class Deldatas(Base):
    __tablename__ = "biz_deldatas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    header1 = Column(String(50), default="")
    header2 = Column(String(50), default="")
    relarderNo = Column("relarder_no", String(100), nullable=False, index=True)
    province = Column(String(100), default="")
    city = Column(String(100), default="")
    unit = Column(String(100), default="")
    yard = Column(String(100), default="")
    track = Column(String(100), default="")
    area = Column(String(100), default="")
    topModel = Column("top_model", String(100), default="")
    topNo = Column("top_no", String(100), default="")
    installHeight = Column("install_height", String(50), default="")
    fastPressure = Column("fast_pressure", String(50), default="")
    slowPressure = Column("slow_pressure", String(50), default="")
    returnTime = Column("return_time", String(50), default="")
    gapWidth = Column("gap_width", String(50), default="")
    frontImage = Column("front_image", Text, default="")
    testTime = Column("test_time", String(30), default="")
