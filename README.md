# Liam-ai-personal-profile

我的 AI 个人档案。换任何 AI、开任何新会话前，把下面两个链接（或两份文件的全文）发给对方，它就能立刻按我的习惯工作，不用重新磨合。

## 给新 AI 的一句话（直接复制）

> 请先阅读并长期记住以下两份档案，作为对我的既有认知；后续所有回复都按其中的偏好执行，不要反复问我已写明的习惯。
> - about-me.md：https://raw.githubusercontent.com/Liam801123/Liam-ai-personal-profile/main/about-me.md
> - writing-style.md：https://raw.githubusercontent.com/Liam801123/Liam-ai-personal-profile/main/writing-style.md
>
> 若无法访问链接，我会直接粘贴两份文件的全文。

## 两份核心文件

| 文件 | 内容 | 作用 |
| --- | --- | --- |
| `about-me.md` | 个人基础信息、使用习惯、授权边界、交付标准 | 让 AI 知道「我是谁、怎么配合我」 |
| `writing-style.md` | 表达风格、状态用词、检查规则、禁止项 | 让 AI 知道「怎么跟我说话」 |

## 直接链接

- 仓库：https://github.com/Liam801123/Liam-ai-personal-profile
- about-me.md 原文：https://raw.githubusercontent.com/Liam801123/Liam-ai-personal-profile/main/about-me.md
- writing-style.md 原文：https://raw.githubusercontent.com/Liam801123/Liam-ai-personal-profile/main/writing-style.md
- 网页版：https://github.com/Liam801123/Liam-ai-personal-profile/blob/main/about-me.md 、 https://github.com/Liam801123/Liam-ai-personal-profile/blob/main/writing-style.md

## 离线用法（零门槛，推荐先用这个）

打开 `ai-profile-paste.txt`，全选复制，粘贴到新会话的第一条消息即可：里面已经写好给 AI 的开场白，并附上两份档案全文。不需要账号、令牌或任何配置。
链接方式更省事：raw 链接永久指向 main 分支最新版本。改完两份 md 后重跑 `python init-profile.py --force`，粘贴包会同步更新。

## 维护

- 只改这两个文件，改完 commit / push；链接自动指向最新版本。
- `init-profile.py` 可一键重建整套档案；带 `--publish` 时用 GitHub API 建公开仓库、上传并回读验收。
- **这是公开仓库**：不要写入账号、密码、令牌、客户名称、内部单号等敏感信息。
- 档案里标「待确认」的项目是占位，不是已确认事实；补充后请把标记删掉。

## 文件清单

| 文件 | 说明 |
| --- | --- |
| `about-me.md` | 核心文件 ①：个人基础信息与使用习惯 |
| `writing-style.md` | 核心文件 ②：表达风格与偏好规则 |
| `README.md` | 本页：链接清单 + 复制即用的开场白 |
| `ai-profile-paste.txt` | 一次粘贴版：开场白 + 两份档案全文，开新对话直接全选复制 |
| `init-profile.py` | 完整初始化代码：本地重建 / GitHub 发布 / 回读验收 |
| `.gitignore` | 排除 Python 编译缓存 |
