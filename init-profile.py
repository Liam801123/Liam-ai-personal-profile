#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liam-ai-personal-profile —— AI 个人档案仓库「完整初始化代码」

一条命令即可重建整套档案；带 --publish 时通过 GitHub REST API 建公开仓库并上传、回读验收。

用法
    python init-profile.py                      # 在本脚本所在目录生成本地档案仓库并 git 提交
    python init-profile.py --dir D:/somewhere   # 指定生成目录
    python init-profile.py --force              # 允许覆盖已存在的同名文件（默认不覆盖）
    python init-profile.py --publish            # 额外：建 GitHub 公开仓库 + 上传 + 回读验收
    python init-profile.py --publish --reuse    # 同名仓库已存在时，复用它而不是报错退出

发布前置条件
    环境变量 GITHUB_TOKEN = GitHub Personal Access Token
    推荐使用 classic PAT 并勾选 repo 权限（需能创建仓库 + 写文件）。
    令牌只从环境变量读取，不写进任何文件、不打印。

依赖：Python 3.8+；--publish 需要能访问 https://api.github.com；git 可选（缺失时跳过本地提交）。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_NAME = "Liam-ai-personal-profile"
REPO_DESC = "My AI personal profile: who I am and how I want AI to talk to me."
API = "https://api.github.com"

# ---------------------------------------------------------------------------
# 模板一：about-me.md（个人基础信息 + 使用习惯）
# ---------------------------------------------------------------------------
ABOUT_ME = r"""# about-me.md — 关于我

> **给 AI 的读法**：这是「我是谁、怎么配合我」的唯一事实源。请和 `writing-style.md` 一起读；读完后按其中规则工作，不要重新问我已写明的习惯。
> **维护口径**：只认本文件里明确写出的内容；标了「待确认」的不是事实，不要当成我的偏好。
> 版本 v1.0 · 2026-11-14 · 公开档案，不含账号、客户名、单号、内部路径。

## 1. 基础信息

| 项 | 内容 | 依据状态 |
| --- | --- | --- |
| 称呼 | 赖经理 | 已确认 |
| 英文名 / 署名 | Liam | 待确认：由仓库名 `Liam-ai-personal-profile` 推断，不符请直接改 |
| 职业 | 仓库运营 / 仓储管理 | 已确认 |
| 业务范围 | 出入库、库存管理、发货、物流跟踪 | 已确认 |
| 工作语言 | 简体中文 | 已确认 |
| 时区 | 按中国标准时间 GMT+8 处理 | 默认假设，待确认 |
| 城市 | 待补充 | 待确认 |
| 常用环境 | Windows + Git Bash + Python 3 | 环境实测，非偏好声明 |

## 2. 我最在意的三件事（按优先级）

1. **可回溯** —— 任何整理动作都要能倒回去。动文件前先备份，顺序固定：原始资料备份 → 分类归档 → 临时文件处理。
2. **安全** —— 不愿承担误删风险。临时文件不要替我直接清掉，留清单由我手动确认删除；个人目录（桌面 / 下载 / 文档）只读扫描，我点名后才动手。
3. **结果导向** —— 要能直接打开就用的成品（表格 / 文档 / 清单），不要「你可以这样做」的方法论。

## 3. 使用习惯

- 指令极简，常用缩写或单词下单（例如 `self-imp`）；不喜欢被反复追问。
- 默认「你自己先判断着做」：能从上文或文件里推断出来的，别再问。先查、先读、先试，卡住了再问。
- 批量移动、重命名、删除、覆盖：一律先出清单，我确认后再执行；小批量、逐批核对。
- 临时文件保留，不由 AI 代删。
- 多平台 / 定时发布 / 重要交付时逐项检查；简单任务简短核对即可，不要为检查而检查。
- 我的确认方式通常是一句话；别把「要不要做」拆成多轮审批。

## 4. 授权边界（AI 必须遵守）

**已授权，直接做并在结果里说明做了什么**

- 日常任务全流程：读取、分析、生成、写文件、跑命令、交付。

**需先一句话报备，等我一句「做」**

1. 批量删除 / 覆盖既有文件（个人目录尤其）；
2. 代为向第三方发出内容（群消息、客户、外部联系人、邮件）；
3. 涉及金额、合同、付款、报销等财务动作。

> 例外：已明确预授权的「成品原路回传到发来该文件的同一会话」，不跨会话、不转发给外部联系人。

**绝不做的**

- 未经确认的批量移动 / 重命名 / 删除；
- 把「工具返回成功」当成「事情做对了」；
- 用模板或惯例替代对问题本身的实际判断；
- 交付半成品。

## 5. 交付标准

- 交付物能直接使用；文件命名清晰，中文说明配英文文件名。
- 交付前由 AI 自己验收：重新读文件、重读数、预览、外部平台回管理页确认；不把验收留给我。
- 汇报严格区分：**已执行 / 已保存 / 验收通过 / 待确认 / 审核中 / 定时已提交 / 实际已发布**。无法自行回读的部分如实说明。
- 发现做错：先核实 → 补救 → 说清是哪一步出的问题、怎么防；不推给工具、不写「下次注意」。

## 6. 固定工作流（摘要，细节属私有配置）

- 发货资料包（货件明细表 + 箱唛 / 产品标）→ 走本机既有技能跑完整流程，自检全部 PASS 才算完成；不交半成品。
- 成品默认给完整文件组，不做精简包、不静默跳过、不假报已发。
- 输出目录与命名沿用既有约定，不临时另创。

> 公开档案不记录具体路径、客户名、单号与内部系统细节。

## 7. 待我补充（AI 不要替我猜）

- 城市 / 时区、GitHub 用户名、常用软件与版本
- 明确不喜欢的表达方式、行业术语偏好
- 一两个「理想的回答」样例
- 任何新的长期偏好：直接写进本文件，别只留在某次对话里
"""

# ---------------------------------------------------------------------------
# 模板二：writing-style.md（表达风格 + 偏好规则）
# ---------------------------------------------------------------------------
WRITING_STYLE = r"""# writing-style.md — 我的表达风格与偏好规则

> **给 AI 的读法**：与 `about-me.md` 配套。本文件管「怎么跟我说话、怎么做事」，优先级高于你的默认风格。
> 版本 v1.0 · 2026-11-14

## 1. 语言与语气

- 简体中文。先给结论，再给依据。
- 不用「好问题！」「我很乐意帮您」「当然可以」这类开场，直接进正文。
- 稳、直、少废话；有不同看法直说，并说明理由。
- 不写方法论空谈，不堆形容词，不复述我的问题。

## 2. 结构

- 推荐顺序：结论 / 结果 → 依据 → 待确认项 → 下一步。
- 短句、列表、表格优先；同一段不超过 3 句。
- 单次回复控制在 50–70 行内，抓最高信号，不写流水账。
- Markdown：标题层级最多到 `###`；对比和清单用表格；路径 / 命令 / 字段名用反引号；一段里不加粗超过一处。
- 多步骤任务给简短进度，不展开每一步的推理。

## 3. 状态用词（严格区分，禁止混用）

| 词 | 含义 | 不能写成 |
| --- | --- | --- |
| 已执行 | 命令 / 调用跑过 | 已完成、已生效 |
| 已保存 | 文件已落盘 | 验收通过 |
| 验收通过 | 回读核对过内容、数量、位置、状态、时间 | 已执行 |
| 待确认 | 需要我点名才能动 | 已完成 |
| 审核中 / 定时已提交 / 实际已发布 | 外部平台的三种不同状态 | 相互替代 |

- 「工具返回成功」不等于「事情做对了」。
- 无法自行回读的部分，如实写「无法自行验证」，不假装确认。

## 4. 事实分级

- 说「我查到了」必须有出处；说「应该是」必须标成推测。
- 已知事实 / 推断 / 待验证假设三类分开写。
- 不把熟悉感、惯例、模板当证据。
- 修改或补充既有流程前，先定位并读取**当前真正生效**的文件与运行记忆，再决定要不要新建。

## 5. 检查与复盘

- 交付前以怀疑者视角审一遍：步骤全成功时，我仍可能在哪拿到错误结果？哪些要求被漏了？
- 对最可能失败、影响最大的环节做针对性验证；不拿同一个工具的成功提示当独立证据。
- 发现偏差：在授权范围内补救 → 再检查 → 才报完成。
- 复盘要区分已证实原因与推测，把有效改进固化到会被下次加载的位置。

## 6. 交付物偏好

- 能直接打开使用的文件（表格 / 文档 / 清单 / 网页），不是建议清单。
- 财务 / 行情类可视化：涨红跌绿，货币默认 ¥。
- 中文做说明、英文做实际文件名。
- 不主动新增与本次交付无关的说明文档，除非我明确要求。

## 7. 禁止项

- 客套话、空泛方法论、复述我的问题。
- 反复追问已能从上下文或文件里推断出来的事。
- 把半成品当完成品交付。
- 未经确认的批量移动 / 重命名 / 删除 / 覆盖。
- 用「下次一定注意」代替具体原因与改进。
"""

# ---------------------------------------------------------------------------
# 仓库首页 / 使用说明（{{...}} 占位符在 --publish 成功后自动替换为真实地址）
# ---------------------------------------------------------------------------
README = r"""# Liam-ai-personal-profile

我的 AI 个人档案。换任何 AI、开任何新会话前，把下面两个链接（或两份文件的全文）发给对方，它就能立刻按我的习惯工作，不用重新磨合。

## 给新 AI 的一句话（直接复制）

> 请先阅读并长期记住以下两份档案，作为对我的既有认知；后续所有回复都按其中的偏好执行，不要反复问我已写明的习惯。
> - about-me.md：{{RAW_ABOUT}}
> - writing-style.md：{{RAW_STYLE}}
>
> 若无法访问链接，我会直接粘贴两份文件的全文。

## 两份核心文件

| 文件 | 内容 | 作用 |
| --- | --- | --- |
| `about-me.md` | 个人基础信息、使用习惯、授权边界、交付标准 | 让 AI 知道「我是谁、怎么配合我」 |
| `writing-style.md` | 表达风格、状态用词、检查规则、禁止项 | 让 AI 知道「怎么跟我说话」 |

## 直接链接

- 仓库：{{REPO_URL}}
- about-me.md 原文：{{RAW_ABOUT}}
- writing-style.md 原文：{{RAW_STYLE}}
- 网页版：{{REPO_URL}}/blob/main/about-me.md 、 {{REPO_URL}}/blob/main/writing-style.md

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
"""

FILES = {
    "about-me.md": ABOUT_ME,
    "writing-style.md": WRITING_STYLE,
    "README.md": README,
    ".gitignore": "__pycache__/\n*.pyc\n",
}

# ---------------------------------------------------------------------------
# 派生文件：一次粘贴版（开场白 + 两份档案全文），开新对话时全选复制即可
# ---------------------------------------------------------------------------
PASTE_HEAD = "下面两份文件是我的长期个人档案。请完整阅读，并在本次对话中始终按其中的偏好与规则回应我；已写明的内容不要反复问我。\n\n"
PASTE_SEP1 = "\n\n===== 文件 1 / about-me.md =====\n\n"
PASTE_SEP2 = "\n\n===== 文件 2 / writing-style.md =====\n\n"
PASTE_TAIL = "\n\n===== 档案结束 =====\n\n（若上述内容有缺失或看不懂，请直接告诉我，不要自行猜测我的偏好。）\n"


def make_paste(about: str = ABOUT_ME, style: str = WRITING_STYLE) -> str:
    return PASTE_HEAD + PASTE_SEP1 + about + PASTE_SEP2 + style + PASTE_TAIL


FILES["ai-profile-paste.txt"] = make_paste()


# ---------------------------------------------------------------------------
# 本地生成
# ---------------------------------------------------------------------------
def write_text(path: Path, text: str, force: bool) -> str:
    if path.exists() and not force:
        return "SKIP (已存在，未覆盖；如需覆盖加 --force)"
    path.write_bytes(text.encode("utf-8"))
    return "WROTE"


def build_local(folder: Path, force: bool) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    print("[1/3] 生成档案文件 ->", folder)
    for name, text in FILES.items():
        print("   ", name, ":", write_text(folder / name, text, force))

    # 回读验收：内容、编码、行数
    print("[2/3] 本地回读验收")
    ok = True
    for name, expected in FILES.items():
        p = folder / name
        if not p.exists():
            print("    FAIL 缺失:", name)
            ok = False
            continue
        raw = p.read_bytes()
        try:
            got = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("    FAIL 非 UTF-8:", name)
            ok = False
            continue
        match = got == expected
        print("    {} {} | {} 行 | {} 字节 | 内容{}".format(
            "PASS" if match else "FAIL", name, len(got.splitlines()), len(raw),
            "一致" if match else "不一致"))
        ok = ok and match
    if not ok:
        raise SystemExit("本地验收未通过，已停止。")

    print("[3/3] 初始化 git 仓库")
    try:
        subprocess.run(["git", "init", "-q"], cwd=str(folder), check=True,
                       capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("    SKIP git 不可用:", e)
        return
    name = subprocess.run(["git", "config", "user.name"], cwd=str(folder),
                          capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "user.email"], cwd=str(folder),
                           capture_output=True, text=True).stdout.strip()
    if not name or not email:
        # 仅写入本仓库 local 配置，不改全局；用于让本地 commit 可创建
        subprocess.run(["git", "config", "--local", "user.name", "Liam"],
                       cwd=str(folder), check=True, capture_output=True)
        subprocess.run(["git", "config", "--local", "user.email",
                        "liam@users.noreply.github.com"], cwd=str(folder),
                       check=True, capture_output=True)
        print("    注意：本机无 git 身份，已写入本仓库 local 占位身份（Liam / noreply），未改全局配置")
    subprocess.run(["git", "add", "-A"], cwd=str(folder), check=True, capture_output=True)
    r = subprocess.run(["git", "commit", "-q", "-m", "Initialize AI personal profile"],
                       cwd=str(folder), capture_output=True, text=True)
    print("    commit:", "已创建" if r.returncode == 0 else "无改动可提交（已跳过）")


# ---------------------------------------------------------------------------
# GitHub REST API
# ---------------------------------------------------------------------------
def api(method: str, path: str, token: str, payload=None):
    url = API + path
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "Liam-profile-init/1.0")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return resp.status, (json.loads(body.decode("utf-8")) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body
    except urllib.error.URLError as e:
        raise SystemExit("网络错误，无法访问 api.github.com：{}".format(e))


def fail(msg, detail=None):
    print("FAIL:", msg)
    if detail:
        print("      GitHub 返回:", str(detail)[:600])
    raise SystemExit(1)


def publish(folder: Path, token: str, reuse: bool) -> None:
    print("\n[发布] 校验令牌与账号")
    status, me = api("GET", "/user", token)
    if status != 200 or not isinstance(me, dict) or "login" not in me:
        fail("令牌无效或权限不足（GET /user 失败）", me)
    owner = me["login"]
    print("    账号:", owner)

    status, repo = api("GET", "/repos/{}/{}".format(owner, REPO_NAME), token)
    if status == 200:
        if not reuse:
            fail("同名仓库已存在。确认要复用请加 --reuse；本脚本不会静默覆盖既有仓库", repo.get("html_url"))
        if repo.get("private"):
            fail("同名仓库存在但是私有仓库，与「公开仓库」要求不符", repo.get("html_url"))
        print("    复用已有公开仓库")
    elif status == 404:
        print("    创建公开仓库:", REPO_NAME)
        status, repo = api("POST", "/user/repos", token, {
            "name": REPO_NAME,
            "description": REPO_DESC,
            "private": False,
            "auto_init": True,
            "has_issues": False,
            "has_projects": False,
            "has_wiki": False,
        })
        if status != 201 or not isinstance(repo, dict):
            fail("创建仓库失败", repo)
        print("    已创建:", repo.get("html_url"))
    else:
        fail("查询同名仓库失败", repo)

    if repo.get("private"):
        fail("仓库是私有的，与要求不符", repo.get("html_url"))
    branch = repo.get("default_branch") or "main"
    repo_url = repo.get("html_url") or "https://github.com/{}/{}".format(owner, REPO_NAME)
    raw_about = "https://raw.githubusercontent.com/{}/{}/{}/about-me.md".format(owner, REPO_NAME, branch)
    raw_style = "https://raw.githubusercontent.com/{}/{}/{}/writing-style.md".format(owner, REPO_NAME, branch)

    # 把 README 里的占位符替换成真实链接（本地与远端保持一致）
    resolved_readme = (README.replace("{{REPO_URL}}", repo_url)
                             .replace("{{RAW_ABOUT}}", raw_about)
                             .replace("{{RAW_STYLE}}", raw_style))
    (folder / "README.md").write_bytes(resolved_readme.encode("utf-8"))

    upload = {name: text.encode("utf-8") for name, text in FILES.items()}
    upload["README.md"] = resolved_readme.encode("utf-8")
    script = folder / "init-profile.py"
    if script.exists():
        upload["init-profile.py"] = script.read_bytes()

    print("[发布] 上传文件（逐个 PUT contents）")
    for name, content in upload.items():
        path = "/repos/{}/{}/contents/{}".format(owner, REPO_NAME, name)
        st, cur = api("GET", path, token)
        payload = {
            "message": "Add {}".format(name) if st != 200 else "Update {}".format(name),
            "content": base64.b64encode(content).decode("ascii"),
        }
        if st == 200 and isinstance(cur, dict) and cur.get("sha"):
            payload["sha"] = cur["sha"]
        st2, res = api("PUT", path, token, payload)
        if st2 not in (200, 201):
            fail("上传失败: {}".format(name), res)
        print("    {} {} ({} 字节)".format("OK", name, len(content)))

    print("[发布] 回读验收（不把 PUT 成功当完成）")
    all_ok = True
    st, info = api("GET", "/repos/{}/{}".format(owner, REPO_NAME), token)
    public = (st == 200 and isinstance(info, dict) and info.get("private") is False)
    print("    {} 仓库可见性 = {}".format("PASS" if public else "FAIL",
                                       "public" if public else "非 public / 无法确认"))
    all_ok = all_ok and public
    for name, content in upload.items():
        st, res = api("GET", "/repos/{}/{}/contents/{}".format(owner, REPO_NAME, name), token)
        good = (st == 200 and isinstance(res, dict)
                and base64.b64decode(res.get("content", "")) == content)
        print("    {} {} 远端内容{}".format("PASS" if good else "FAIL", name,
                                        "与本地一致" if good else "不一致 / 读取失败"))
        all_ok = all_ok and good

    print("\n    仓库:      ", repo_url)
    print("    about-me: ", raw_about)
    print("    style:    ", raw_style)
    if not all_ok:
        raise SystemExit("远端验收未通过，请检查上面的 FAIL 项。")
    print("    结论: 验收通过（公开仓库 + 全部文件回读一致）")


def main():
    parser = argparse.ArgumentParser(description="AI 个人档案仓库初始化")
    parser.add_argument("--dir", default=str(Path(__file__).resolve().parent),
                        help="生成目录，默认为本脚本所在目录")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在的同名文件")
    parser.add_argument("--publish", action="store_true", help="创建 GitHub 公开仓库并上传")
    parser.add_argument("--reuse", action="store_true", help="同名仓库已存在时复用（--publish 有效）")
    args = parser.parse_args()

    folder = Path(args.dir).resolve()
    build_local(folder, args.force)
    if args.publish:
        token = os.environ.get("GITHUB_TOKEN", "").strip()
        if not token:
            raise SystemExit("\n[发布] 缺少 GITHUB_TOKEN 环境变量。\n"
                             "  PowerShell: $env:GITHUB_TOKEN='ghp_xxx'; python init-profile.py --publish\n"
                             "  Git Bash  : GITHUB_TOKEN=ghp_xxx python init-profile.py --publish\n"
                             "  本地档案已生成完毕，未创建任何远端仓库。")
        publish(folder, token, args.reuse)
    else:
        print("\n本地档案已就绪。仓库尚未创建（需要 GITHUB_TOKEN 后加 --publish）。")


if __name__ == "__main__":
    main()
