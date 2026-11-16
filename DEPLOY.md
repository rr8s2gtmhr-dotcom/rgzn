# 免费 PaaS 部署指南（Cloudflare Pages + Railway）

本指南把项目部署到公网，**零成本**（在免费额度内）。架构：

- **前端** → Cloudflare Pages（免费，全球 CDN，无流量限制）
- **后端 + MySQL** → Railway（注册送免费额度，足够本项目演示使用）

> ⚠️ 现实说明：PlanetScale 已取消免费层；Railway 目前注册送一次性免费额度（用完需付费，但本项目用量极小）。免费层服务长时间不访问会休眠，首次访问有几十秒延迟；国内访问速度不稳定。适合演示/学习，不适合正式生产。

---

## 一、前置准备

1. 一个 **GitHub** 账号（代码要推上去，Railway 和 Cloudflare 都从 GitHub 拉取）。
2. 一个 **Railway** 账号（railway.app，用 GitHub 登录即可）。
3. 一个 **Cloudflare** 账号（dash.cloudflare.com）。

---

## 二、把代码推到 GitHub

在项目根目录执行（把 `你的仓库地址` 换成你自己的）：

```bash
git init
git remote add origin https://github.com/你的用户名/你的仓库名.git
git add .
git commit -m "init deploy"
git push -u origin main
```

`.gitignore` 已忽略 `server/.env`（数据库密码）、`node_modules`、`dist`，不会上传敏感信息和大文件。

---

## 三、部署后端 + MySQL 到 Railway

### 1. 创建项目和 MySQL
1. 登录 Railway → **New Project** → **Empty Project**。
2. 项目里点 **New** → **Database** → **Add MySQL**。等待创建完成。
3. 点开刚建的 MySQL → **Variables** 标签，会看到 `MYSQLHOST`、`MYSQLPORT`、`MYSQLUSER`、`MYSQLPASSWORD`、`MYSQLDATABASE` 等变量——后端代码已自动兼容这些变量名，无需手动改。

### 2. 部署后端服务
1. 项目里点 **New** → **GitHub Repo** → 选择你刚推的仓库。
2. 点开新加的服务 → **Settings**：
   - **Root Directory**：填 `server`（后端代码在这个子目录）
   - **Start Command**：填 `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. 切到 **Variables** 标签，添加：
   - `JWT_SECRET` = 一串随机字符串（如 `my-super-secret-2026-xxx`，别用默认值）
   - `CORS_ORIGINS` = `*` （等前端部署好后可改成前端域名，更安全）
   - `PORT` = `8000`（Railway 一般自动注入，没有就手动加）
4. 数据库变量（`MYSQL*`）Railway 会自动注入到后端服务，**如果没自动出现**，手动在后端服务的 Variables 里点 **Add Reference** 引用 MySQL 服务的对应变量。

### 3. 验证后端
- 服务部署完成后，点服务顶部生成的域名（如 `xxx.up.railway.app`），访问：
  ```
  https://xxx.up.railway.app/api/health
  ```
  返回 `{"code":0,"message":"ok",...}` 即成功。
- 首次启动会自动建表并导入初始数据（admin/test 账号）。在 **Deployments → 日志** 里可看到 seed 信息。
- **把这个后端域名记下来**，下一步要用。

> 如果启动失败看日志：常见原因是数据库变量没引用上（`MYSQL*` 为空）或 Root Directory 没填 `server`。

---

## 四、部署前端到 Cloudflare Pages

1. 登录 Cloudflare → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**。
2. 选择 GitHub 仓库 → **Begin setup**。
3. 构建配置：
   - **Framework preset**：Vue（或 Vite）
   - **Build command**：`npm run build`
   - **Build output directory**：`dist`
   - **Root directory**：留空（前端在仓库根目录）
4. **Environment variables**（点击 "Add variable"）：
   - `VITE_API_URL` = `https://你的后端域名.up.railway.app/api`
     （例：`https://rgzn-ai.up.railway.app/api`，注意末尾带 `/api`，不要带引号）
5. 点 **Save and Deploy**。等待构建完成（几分钟）。
6. 部署好后得到前端地址：`https://你的项目名.pages.dev`。

> 本项目使用 hash 路由（`/#/login`），所以 Cloudflare Pages 不需要配置 SPA 重写规则，直接可访问任何页面。

---

## 五、验证

打开 `https://你的项目名.pages.dev`：
1. 看到登录页（「南宁铁路局」+ 标语）→ 前端正常。
2. 用 `admin / 123456` 登录 → 后端 + 数据库正常。
3. 进入「用户管理」，切换部门筛选、新增/删除用户 → CRUD 接口正常。
4. 浏览器控制台（F12）无报错 → CORS 配置正常。

如果有 CORS 报错：回到 Railway 后端服务的 Variables，把 `CORS_ORIGINS` 改成你的前端域名：
```
https://你的项目名.pages.dev
```

---

## 六、常见问题

| 问题 | 原因 | 解决 |
|---|---|---|
| 后端 `/api/health` 访问 502 | 服务休眠或启动失败 | 看 Railway 日志；首次访问等 30-60 秒冷启动 |
| 登录时报网络错误 | 前端 `VITE_API_URL` 没配对 | 检查 Cloudflare Pages 环境变量，改对后重新部署 |
| 数据为空/没初始账号 | seed 未执行 | 看后端日志；检查数据库连接变量 |
| 长时间不用后打不开 | 免费层休眠 | 等几十秒冷启动；Railway 免费额度用完会暂停服务 |
| 国内访问慢 | 免费 PaaS 节点在境外 | 正常现象，演示可接受；正式使用建议国内云服务器 |

---

## 七、成本与后续

- 当前方案在免费额度内 **¥0 成本**。
- Railway 免费额度用完后服务会暂停，需要绑定信用卡继续使用（本项目用量极小，通常够用很久）。
- 如果要长期稳定使用且国内访问快，建议后续迁移到国内云服务器（腾讯云/阿里云轻量，约 ¥50-100/年首年），用 Docker 一键部署（架构相同，只需把 MySQL 和后端放到服务器上）。

---

## 附：本次为部署做过的代码改造

1. `server/app/database.py`：`init_db()` 去掉 `CREATE DATABASE`，只建表（兼容 Railway 自动创建的数据库）。
2. `server/app/config.py`：数据库环境变量同时兼容本地 `DB_*` 和 Railway 注入的 `MYSQL*` 变量名（AliasChoices）。
3. `.env.development`：接口地址改为 `/api` + Vite 本地代理（本地/内网穿透用）。
4. `vite.config.ts`：增加 `/api` 代理到本机 `8001`。
5. `.env.production`：接口地址保持 `/api`（部署时由 Cloudflare Pages 环境变量 `VITE_API_URL` 覆盖为 Railway 后端完整地址）；新增 `VITE_PUBLIC_PATH = /` 覆盖基础 `.env` 的 `/vue-next-admin-preview/` 前缀，确保构建产物资源路径为 `/assets/...`，适配 Cloudflare Pages 根目录部署。
