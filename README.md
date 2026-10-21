# 小红书图文 11 版式 Skill

**作者 / Maintainer：** [老三 @Heylaosan](https://x.com/Heylaosan)

**灵感来源 / Inspiration：** [@ianneo_ai](https://x.com/ianneo_ai) 提供的 11 种图文模板思路 · [原始帖子](https://x.com/ianneo_ai/status/2112730753075417104)。感谢原作者的分享。

> 独立提炼与实现的 Agent Skill，非原作者的源设计文件，也不代表原作者参与或认可本仓库。原始素材的权利归相应权利人所有。


把文章/设计案例/教程/AI/Apple 资讯改写为 3:4 小红书轮播图的 **Agent Skill**。**默认每一页单独输出 1080×1440 PNG，绝不合成为一张大图。**

> **仓库同步状态：** 文档、Skill 规则、运行脚本和 JSON 示例已上传。11 张参考 PNG 和独立导出的演示 PNG 尚未上传到 GitHub（可从此会话提供的 v1.1 完整压缩包获取）。下列目录是完整安装包的结构说明。

## 内容清单

- `SKILL.md`：Skill 入口，负责自动选择版式、组织内容、检验质量。
- `references/layout-spec.md`：11 套布局与字数约束。
- `references/editorial-playbook.md`：改写策略与合理选页。
- `references/data-contract.md`：自动出图的 JSON 格式。
- `scripts/render.py`：Pillow 渲染程序，每个页面独立导出 1080×1440 PNG。
- `examples/demo.json`：11 种版式的演示内容（全部是示意数据）。
- `assets/templates/`：由原始参考拼图精确裁切出的 11 张独立版式参考图（各 360×480）。
- `references/template-index.md`：T01–T11 与 11 张参考图片的对应关系。
- `examples/rendered/`：11 张独立 PNG 示例；`examples/apple-output/`：AirDrop 主题 6 张独立 PNG 示例。

## 安装

将完整目录 `xiaohongshu-layout-kit` 放到你的支持 Agent Skills 的智能体可识别的 Skills 文件夹。常见例子：项目根目录下 `.agents/skills/xiaohongshu-layout-kit/`，或 Claude Code / Codex 所配置的 Skills 路径。依所用客户端配置为准。

## 怎么调用

对智能体说：“用 xiaohongshu-layout-kit 把下面这篇文章变成 6 页小红书图文，保持白底极简风，不编造数据，输出 1080×1440 的 PNG。”

## 出图（需 Python）

```bash
python -m pip install Pillow
python scripts/render.py examples/demo.json --out examples/rendered
```

命令完成后，会获得**11 张单独的图片** `01-T01.png` … `11-T11.png`，另有 `pages-manifest.json` 和 `content.json`。

若想测试 6 页 Apple 主题 demo：

```bash
python scripts/render.py examples/apple-airdrop-demo.json --out examples/apple-output
```

按文件编号单张上传到小红书。生成的 PNG 每张均为 1080×1440 px，可单独使用。无图可先输出灰色占位版（真实发布前应替换对应素材）。

只有需要**额外制作审核预览拼图**时，才手动加 `--contact-sheet`。该预览不能替代单张 PNG。

## 重要说明

本 Skill 是根据截图重新归纳的**版式规范与工程化渲染**，并非原帖中 Claude 生成的原始文件或 Figma 源图。当前渲染器输出 PNG（非可编辑 Figma 图层）。