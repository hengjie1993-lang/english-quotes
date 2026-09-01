# 英句囊 · 交接手册（HANDOFF）

> 给「接手即改」用的。改动铁律、核心机制、踩坑清单、验证命令都在这里。
> 姊妹项目「小诗囊」（中文古诗）见 `D:/WorkBuddy-Results/poetry-reader/HANDOFF.md`，架构同源，可对照阅读。

---

## 0. TL;DR 改动对照表

| 你要改的东西 | 必须同步动什么 | 不做的后果 |
|---|---|---|
| 改 `index.html` 的任何功能/样式 | 升 `index.html` 与 `sw.js` 里的 `APP_VERSION` | 手机端看不到任何改动（SW 缓存陷阱，详见 §4） |
| 改/增 `quotes.json` 数据 | 升 `APP_VERSION`（让客户端强制重拉 `quotes.json?v=N`） | 用户手机仍读旧数据 |
| 加/改主题标签 | 同步更新 `index.html` 里 `tagLabel()` 的中文映射表 | 新标签显示为英文原文 |

---

## 1. 项目概览

- **定位**：给「阿无」自己用的经典英文名句工具，手机优先，微信浮窗/浏览器书签点开即用，**亲子学英语**场景。不是 App、不做后端、不部署服务器。
- **形态**：纯静态站点 + GitHub Pages。零服务器、零数据库、零构建步骤。
- **技术栈**：单文件 `index.html`（Vue 3 global build + 自写 CSS，CDN 走 jsdelivr）+ `quotes.json` + PWA（`manifest.webmanifest` + `sw.js`）。
- **与小诗囊的核心差异**：
  - 没有「拼音」→ 改为 **中文翻译**（中英对照，可一键隐藏）。
  - 加 **主题标签筛选**（智慧/勇气/友谊…），小诗囊没有。
  - 版权范围受约束：只收录**作者去世超百年的公版名家**（见 §5）。

---

## 2. 文件地图

| 文件 | 作用 | 改动频率 |
|---|---|---|
| `index.html` | Vue3 单文件主应用（UI + 逻辑 + 样式） | 高 |
| `quotes.json` | 名句数据（219 条 / ~52KB），字段见 §5 | 中（加句子时） |
| `build_quotes.py` | 策划数据的脚本，运行生成 `quotes.json` | 低（加句子时改它再跑） |
| `sw.js` | Service Worker，**v5 起改为「透明穿透」，不再缓存任何资源** | 低（仅版本号随动） |
| `manifest.webmanifest` | PWA 加到主屏 | 低 |
| `LICENSE` | MIT | 不 |
| `HANDOFF.md` | 本文件 | 中（每次大改同步） |

---

## 3. 核心机制

### 3.1 渲染管线
```
quotes.json ──fetch──▶ this.all ──filter(query+tag)──▶ view ──idx──▶ current
```
- `view`：根据搜索词 `query` 和当前标签 `activeTag` 过滤后的列表。
- `idx`：在 `view` 中的下标；`current = view[idx]`。
- 上一句/下一句在 `view` 内循环；🎲 随机跳到 `view` 内随机下标。

### 3.2 随机起手（真随机）
`mounted()` 拉完数据后自动 `shuffle()`，不再固定第 1 条。
随机源 `randInt(n)`：优先 `crypto.getRandomValues`（密码学安全），回退 `Math.random()`。

### 3.3 搜索与标签
- `view` 计算属性：`text + zh + author + work` 拼接后忽略大小写 `includes(query)`；再按 `activeTag` 过滤。
- `query` / `activeTag` 变化 → `watch` 把 `idx` 重置为 0（避免越界到旧列表）。
- 标签中文名由 `tagLabel()` 映射（英文 tag → 中文，加新 tag 必须同步这里）。

### 3.4 隐藏翻译
`showZh` 布尔，`v-if="showZh"` 控制中文块渲染（用 `v-if` 销毁节点，不留白——**不要改用 `visibility:hidden`**，见 §6）。

### 3.5 Service Worker / 缓存策略（v5 重大调整）
> 历史教训：v1→v4 的 SW 用 cache-first / network-first 缓存 `index.html`，多次导致**手机端困在旧版**（如 v4 加了作者中文名，桌面正常、手机作者名消失）。v5 起改为**透明穿透**：

- **注册**：微信内不注册（UA 判定），否则 `load` 后注册 `sw.js`。
- **`sw.js` v5 行为**：
  - `fetch` 事件 **完全穿透**（`event.respondWith(fetch(event.request))`），**不缓存任何资源**，内容永远走网络、永远最新。
  - `install` 即 `skipWaiting()`；`activate` 清空全部旧缓存 → `clients.claim()` → **强制 `navigator` 刷新每一个已打开页面**。
  - 正是靠「激活即强刷所有页面」，手机端滞留的旧 HTML 会被一次性甩掉（无需用户手动清缓存）。
- `index.html` 仍保留 `Cache-Control: no-cache` meta，减少浏览器/微信的 HTTP 层缓存干扰。
- 微信内不注册 SW（腾讯对 SW 支持差），但微信里 `index.html` 本身靠 no-cache meta + `quotes.json?v=N` 强制重拉，也不会困旧版。
- 代价：牺牲离线可用（无缓存），但换来了「永远最新、不再有缓存陷阱」，对亲子随手用的小工具更稳妥。

---

## 4. 发布铁律（最重要）

> **每改 `index.html` / `quotes.json` / `sw.js`，必须同步升版本号：**

- `index.html` 顶部：`const APP_VERSION = 'N';`
- `sw.js` 顶部：`const CACHE = 'english-vN';` 和 `const APP_VERSION = 'N';`
- `quotes.json` 走 `quotes.json?v=N` 版本戳，客户端自动重拉。

**为什么**：SW 一旦缓存了旧 `index.html`/`quotes.json`，手机端不会自动更新，肉眼看不到改动。这是小诗囊历史上翻车最多次的地方。

**push 后等约 30 秒** GitHub Pages 才重建完，立刻 `curl` 会拿到旧版。

---

## 5. 数据结构（quotes.json）

```json
{
  "id": 1,
  "text": "The fool doth think he is wise, but the wise man knows himself to be a fool.",
  "zh": "愚者自以为智，智者自知其愚。",
  "author": "William Shakespeare",
  "work": "As You Like It",
  "tags": ["wisdom"]
}
```

- `id`：顺序编号（由 `build_quotes.py` 自动赋，不必手填）。
- `text`：英文原句。
- `zh`：中文翻译。
- `author`：作者英文名。
- `authorZh`：作者中文名（显示用，由 `build_quotes.py` 的 `AUTHOR_ZH` 映射自动生成，加新作者须在此字典补中文名）。
- `work`：出处（无出处留空字符串）。
- `tags`：主题标签数组，取值见 `tagLabel` 映射（wisdom/courage/friendship/love/perseverance/time/learning/happiness/character/success/life/freedom/nature/truth/hope）。

### 版权约束（硬规矩）
**只收作者去世超百年的公版名家**（莎士比亚、培根、苏格拉底、孔子、老子、孙中山同时代之外… 实际已收录 33 位，均满足）。翻译用自译或公版译本。
- ❌ 不要加现代/健在作者（乔布斯、爱因斯坦晚年作品、当代名人等）——版权不干净。
- 加句子请改 `build_quotes.py` 的 `DATA` 列表后重跑，不要在 `quotes.json` 上手改（重跑会被覆盖）。

### 重建命令
```bash
cd D:/WorkBuddy-Results/english-quotes
python3 build_quotes.py      # 重新生成 quotes.json
```

---

## 6. 踩坑 / 注意事项

| 坑 | 说明 |
|---|---|
| 微信内不注册 SW | 同小诗囊教训，防旧版缓存陷阱。 |
| 隐藏翻译用 `v-if` | 销毁节点而非 `visibility:hidden`，否则留白（小诗囊 v9 的坑）。 |
| 加 tag 要同步 `tagLabel` | 否则新标签显示英文。 |
| 搜索词大小写 | 已 `toLowerCase()` 归一，无需担心。 |
| 升级后仍看到旧版 | 浏览器/PWA/微信可能缓存旧 `index.html`。v3 起 `index.html` 走 network-first 并加 no-cache meta；如仍看到旧版，手动下拉刷新或清除浏览器缓存。 |

---

## 7. 修改 Cookbook

- **加一句名言**：编辑 `build_quotes.py` 的 `DATA`（加 `[text, zh, author, work, tags]` 一行）→ 跑 `python3 build_quotes.py` → 升 `APP_VERSION` → push。
- **改配色/字体**：改 `index.html` 顶部 `:root` CSS 变量。
- **加主题标签**：`DATA` 里加 tag → `index.html` 的 `tagLabel()` 加中文映射 → 升版本。
- **去 PWA / SW**：删掉 index.html 底部 SW 注册那段即可（不需 SW 时）。

---

## 8. 发布与验证

```bash
git add -A && git commit -m "..." && git push origin main
# 等约 30 秒让 GitHub Pages 重建，然后：
curl -s "https://<账号>.github.io/english-quotes/index.html" | grep -oE "APP_VERSION = '[0-9]+'"
curl -s "https://<账号>.github.io/english-quotes/sw.js" | grep -oE "const CACHE = '[^']+'|APP_VERSION = '[0-9]+'"
curl -s "https://<账号>.github.io/english-quotes/quotes.json?v=1" | python -c "import json,sys; print('条数:', len(json.load(sys.stdin)))"
```

预期：`APP_VERSION = 'N'`、`CACHE = 'english-vN'`、条数 219（或更新后数字）。

---

## 9. 当前状态

- 版本 **v5**（`APP_VERSION = '5'`，`sw.js` 已无 `CACHE` 变量，改为透明穿透）。
- 数据 **219 条**，33 位公版名家。
- 功能：随机起手、搜索（英/中/作者含中文名）、主题标签筛选、隐藏翻译。
- v2 移除 TTS 朗读；v3 优化缓存策略；v4 新增**作者中文名**（`authorZh` 字段）+ 重做视觉；**v5 把 SW 改成透明穿透并激活即强刷所有页面，根治「手机端作者名不显示 / 升级后仍显示旧版」的缓存陷阱**。
- 仓库公开 + MIT 许可 + 仅你有写权限。
