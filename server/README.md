# rgzn-ai 后端（FastAPI + MySQL）

## 启动

```bash
cd server
pip install -r requirements.txt
cp .env.example .env   # 已配置好本地 .env，此步仅用于新环境
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动时会自动建库建表并幂等导入初始数据（重复启动不会重复插入）。

## 账号

- `admin` / `123456`（管理员）
- `test` / `123456`（巡检员）

首次部署请在 `.env` 中修改 `JWT_SECRET`，并提示用户修改初始密码。

## 接口

- `POST /api/auth/login` — 登录，返回 token / roles / authBtnList / menuPaths / userInfos
- `GET  /api/auth/me` — 当前用户
- `GET  /api/settings/theme` — 读取主题配置
- `PUT  /api/settings/theme` — 保存主题配置
- `GET  /api/{resource}?pageNum=1&pageSize=10&keyword=` — 全量列表
- `GET  /api/{resource}/page?pageNum=1&pageSize=10&keyword=` — 分页列表
- `GET  /api/{resource}/{id}` / `POST` / `PUT /{id}` / `DELETE /{id}` — CRUD

`resource` 取值为：`menus`、`units`、`roles`、`users`、`relarders`、`detections`、`maintains`、`deldatas`。

除登录外所有接口需在请求头携带 `Authorization: Bearer <token>`（前端 request.ts 已自动注入）。
