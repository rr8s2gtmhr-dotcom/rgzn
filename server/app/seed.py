from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from .config import settings
from .security import hash_password

ALL_MENU_PATHS = [
    "/home", "/data", "/relarder", "/detection", "/maintain", "/deldata",
    "/system", "/dept", "/role", "/user", "/menu", "/personal",
]
DATA_MENU_PATHS = ["/data", "/relarder", "/detection", "/maintain", "/deldata"]
ALL_BTN_PERMISSIONS = ["btn.add", "btn.edit", "btn.del", "btn.link", "btn.export"]
COMMON_BTN_PERMISSIONS = ["btn.add", "btn.link"]


def menu_meta(title: str, icon: str, roles: list, extra: dict | None = None) -> dict:
    meta = {
        "title": title, "icon": icon, "isHide": False, "isKeepAlive": True,
        "isAffix": False, "isLink": "", "isIframe": False, "roles": roles,
    }
    if extra:
        meta.update(extra)
    return meta


MENUS = [
    dict(id=1, pid=None, path="/home", name="home", component="/@/views/home/index.vue", menuType="menu", menuSort=0, meta=menu_meta("message.router.home", "iconfont icon-shouye", ["admin", "common"], {"isAffix": True})),
    dict(id=2, pid=None, path="/data", name="data", component="/@/layout/routerView/parent.vue", redirect="/relarder", menuType="menu", menuSort=1, meta=menu_meta("message.router.data", "ele-Tools", ["admin", "common"])),
    dict(id=3, pid=2, path="/relarder", name="dataRelarder", component="/@/views/railway/relarderIndex.vue", menuType="menu", menuSort=0, meta=menu_meta("message.router.dataRelarder", "ele-Document", ["admin", "common"])),
    dict(id=4, pid=2, path="/detection", name="dataDetection", component="/@/views/railway/detectionIndex.vue", menuType="menu", menuSort=1, meta=menu_meta("message.router.dataDetection", "ele-Search", ["admin", "common"])),
    dict(id=5, pid=2, path="/maintain", name="dataMaintain", component="/@/views/railway/maintainIndex.vue", menuType="menu", menuSort=2, meta=menu_meta("message.router.dataMaintain", "ele-Timer", ["admin", "common"])),
    dict(id=6, pid=2, path="/deldata", name="dataDeldata", component="/@/views/railway/deldatasIndex.vue", menuType="menu", menuSort=3, meta=menu_meta("message.router.dataDeldata", "ele-Refresh", ["admin", "common"])),
    dict(id=7, pid=None, path="/system", name="system", component="/@/layout/routerView/parent.vue", redirect="/dept", menuType="menu", menuSort=2, meta=menu_meta("message.router.system", "iconfont icon-xitongshezhi", ["admin"])),
    dict(id=8, pid=7, path="/dept", name="systemDept", component="/@/views/system/dept/index.vue", menuType="menu", menuSort=0, meta=menu_meta("message.router.systemDept", "ele-OfficeBuilding", ["admin"])),
    dict(id=9, pid=7, path="/role", name="systemRole", component="/@/views/system/role/index.vue", menuType="menu", menuSort=1, meta=menu_meta("message.router.systemRole", "ele-ColdDrink", ["admin"])),
    dict(id=10, pid=7, path="/user", name="systemUser", component="/@/views/system/user/index.vue", menuType="menu", menuSort=2, meta=menu_meta("message.router.systemUser", "iconfont icon-icon-", ["admin"])),
    dict(id=11, pid=7, path="/menu", name="systemMenu", component="/@/views/system/menu/index.vue", menuType="menu", menuSort=3, meta=menu_meta("message.router.systemMenu", "iconfont icon-caidan", ["admin"])),
    dict(id=12, pid=None, path="/personal", name="personal", component="/@/views/personal/index.vue", menuType="menu", menuSort=99, meta=menu_meta("message.router.personal", "iconfont icon-gerenzhongxin", ["admin", "common"], {"isHide": True})),
]

UNITS = [
    dict(id=1, deptName="运输部", deptShortName="运输", expireTime="2027-12-31"),
    dict(id=2, deptName="工务段", deptShortName="工务", expireTime="2027-10-31"),
]

ROLES = [
    dict(id=1, roleName="管理员", dataScope="全部", code="admin", menuPaths=ALL_MENU_PATHS, btnPermissions=ALL_BTN_PERMISSIONS),
    dict(id=2, roleName="巡检员", dataScope="本单位", code="common", menuPaths=[ALL_MENU_PATHS[0]] + DATA_MENU_PATHS, btnPermissions=COMMON_BTN_PERMISSIONS),
]

USERS = [
    dict(id=1, userName="admin", realName="系统管理员", phone="13800000001", status=True, unitId=1, roleIds=[1], password="123456"),
    dict(id=2, userName="test", realName="巡检员", phone="13800000002", status=True, unitId=2, roleIds=[2], password="123456"),
]

RELARDERS = [
    dict(id=1, deviceNo="JD-001", factory="铁科院", model="TJK-3", address="一场/3股道", trackNo="3", enableTime="2025-01-10", damageTime="", remark="正常"),
    dict(id=2, deviceNo="JD-002", factory="中铁装备", model="TJK-2", address="二场/7股道", trackNo="7", enableTime="2025-03-22", damageTime="", remark=""),
]

DETECTIONS = [
    dict(id=1, relarderNo="JD-001", trackNo="3", installHeight="110", fastPressure="3.12", slowPressure="2.48", returnTime="0.8", gapWidth="12", frontImage="", testTime="2026-11-16 09:30:00", detector="张师傅"),
]

MAINTAINS = [
    dict(id=1, relarderNo="JD-002", maintainTime="2026-11-10", maintainProject="更换弹簧", maintainUser="李工"),
]

DELDATAS = [
    dict(id=1, header1="0a", header2="0a", relarderNo="1132456789", province="12", city="13", unit="aa", yard="a1", track="113", area="dd", topModel="aasdf", topNo="dwfq1234", installHeight="124", fastPressure="3.14", slowPressure="2.56", returnTime="122", gapWidth="33", frontImage="", testTime="2026-11-16 15:03:00"),
]

SEED_MAP = [
    (models.Menu, MENUS),
    (models.Unit, UNITS),
    (models.Role, ROLES),
    (models.Relarder, RELARDERS),
    (models.Detection, DETECTIONS),
    (models.Maintain, MAINTAINS),
    (models.Deldatas, DELDATAS),
]


async def seed_database(db: AsyncSession) -> dict:
    summary: dict[str, int] = {}
    for model, rows in SEED_MAP:
        count = 0
        for row in rows:
            exists = await db.execute(select(model).where(model.id == row["id"]))
            if not exists.scalar_one_or_none():
                db.add(model(**row))
                count += 1
        summary[model.__tablename__] = count

    for row in USERS:
        exists = await db.execute(select(models.User).where(models.User.userName == row["userName"]))
        if not exists.scalar_one_or_none():
            db.add(models.User(
                id=row["id"], userName=row["userName"], passwordHash=hash_password(row["password"]),
                realName=row["realName"], phone=row["phone"], status=row["status"],
                unitId=row["unitId"], roleIds=row["roleIds"],
            ))
            summary.setdefault("sys_users", 0)
            summary["sys_users"] += 1

    await db.commit()
    return summary
