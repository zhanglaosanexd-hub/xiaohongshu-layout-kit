# JSON 输入结构

```json
{
  "pages": [
    {"template":"T01","title":"AirDrop 为什么好用？","subtitle":"好体验让技术消失","image":"assets/hero.png"},
    {"template":"T08","title":"好的设计\n减少思考成本"},
    {"template":"T11","title":"你最常用的功能是什么？"}
  ]
}
```

`template` 为 T01–T11 之一；`title` 为主标题，`subtitle` 可选，`image` 为相对于运行目录的素材路径（可选）。

渲染器逐页输出 `01-T01.png` 等独立文件，附带 `pages-manifest.json`。