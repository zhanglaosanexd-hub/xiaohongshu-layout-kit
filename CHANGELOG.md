# Changelog

## 1.1.0 — 单张图片交付

- 将原 11 版式总览参考图裁切为 T01–T11 的 **11 张独立 360×480 PNG**，放入 `assets/templates/`。
- 主渲染器默认只导出 **逐页 1080×1440 PNG**，没有合并长图、没有默认拼图。
- 新增 `pages-manifest.json`，标识图片顺序与文件名。
- 若确需一张审稿拼图，需主动指定 `--contact-sheet`，不影响独立出图。
- 新增 `references/template-index.md` 以及可运行的 6 页 Apple AirDrop 示例。
- 旧版合并参考图 `assets/reference-contact-sheet.png` 和示例 `examples/rendered/contact-sheet.png` 已从安装包移除。