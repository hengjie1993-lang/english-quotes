# Maxim · 英文经典金句

手机优先的英文经典名句小工具，随时打开给娃读一句、顺带学英语。纯静态、零后端、零服务器。

> 名字 **Maxim** 取自英语里「箴言 / 格言 / 准则」的标准原生词——单字即品牌，语义精准对应「金句」，也契合英文内容的调性（而非生硬套用中式命名）。

- 公网地址（GitHub Pages）：`https://hengjie1993-lang.github.io/english-quotes/`
- 上手前建议阅读 `HANDOFF.md`（项目交接手册：改动铁律、核心算法、踩坑清单）

## 功能
- 随机起手（浏览器 `crypto.getRandomValues` 真随机，每次打开不固定）
- 搜索：英文原文 / 中文翻译 / 作者（含中文名），任意匹配
- 主题标签筛选：智慧 / 勇气 / 友谊 / 爱情 / 坚韧 / 时间 / 学习 / 幸福 / 品格 / 成功 / 人生 / 自由 / 自然 / 真理 / 希望（共 15 个）
- 中英对照：中文翻译可一键隐藏
- 作者双层呈现：中文名（加粗）+ 英文名（斜体）+ 作品《》
- 手机优先排版 + 支持「添加到主屏幕」（PWA）

## 数据来源与许可
- 名句均为**作者去世超百年的公版名家**（莎士比亚、培根、苏格拉底、孔子、老子、歌德、尼采、马克·吐温、王尔德、雨果、托尔斯泰、陀思妥耶夫斯基等 33 位），内容属公版领域。
  - 严守公版边界：只收录去世超百年作者；曾误加一条 Steve Jobs（2011 年去世）已剔除。
- 中文翻译由本项目提供，随代码以 **MIT** 许可发布。
- 数据由 `build_quotes.py` 自策展生成（非第三方数据集），如需扩展见下。
- 本项目代码同样以 **MIT** 发布，详见 [LICENSE](LICENSE)。

## 本地预览
```bash
cd 项目目录
python -m http.server 8137
# 浏览器打开 http://localhost:8137  （不要用 file:// 直接双击）
```

## 扩充 / 重新生成数据
```bash
# 1. 编辑 build_quotes.py 的 DATA，加一行 [text, zh, author, work, tags]
# 2. 若新增作者，在 AUTHOR_ZH 字典补其中文名
# 3. 生成
python build_quotes.py      # -> quotes.json
# 4. 升 APP_VERSION（index.html 内常量）后提交
git add quotes.json index.html && git commit -m "data: 更新名句集" && git push
```

## 部署（GitHub Pages）
代码已 push 到 `main` 分支并开启 Pages，改动后 `git push` 即自动更新。
