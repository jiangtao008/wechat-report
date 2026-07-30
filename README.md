# 微信群周报

把微信群聊天记录整理为本地 HTML 报告，黑色科技风，浏览器直接打开即可查看。

## 项目结构

```text
.
├── report/                          # 群聊 HTML 报告，按群名分目录存放
│
├── index.html           # 报告总览页 —— 浏览器打开后展示所有群组及报告列表
├── index.json           # 报告索引文件（供 index.html 加载使用）
├── generate-index.sh    # 扫描 report/ 下所有 HTML 文件，自动生成 index.json
│
├── wechat-group-report/     # Codex skill（项目主体内容）
├── wechat-group-report-cc/  # claude code skill（项目主体内容）
│
├── .gitignore
└── README.md
```

### 各文件 / 目录说明

| 路径 | 作用 |
|------|------|
| `report/` | 生成的 HTML 报告按群名分目录存放，每个目录对应一个微信群 |
| `index.html` | 项目首页，以折叠树形式展示所有群组及报告，可直接在浏览器打开 |
| `index.json` | 报告索引数据，由 `index.html` 的 JavaScript 动态加载并渲染 |
| `generate-index.sh` | 一键扫描 `report/` 目录，自动更新 `index.json` |
| `wechat-group-report/` | 分析聊天文本生成 HTML 报告的 skill 定义 |
| `wechat-group-report-cc/` | 聚焦社群动态的黑色科技风报告 skill 定义 |

### 更新索引

生成或删除了报告后，运行以下命令刷新 `index.json`：

```bash
bash generate-index.sh
```

## 数据来源

聊天数据通过 [wechat-insight](https://github.com/caigee-cmd/wechat-insight) 从 Mac 微信 4.x 本地数据库提取，导出为 JSONL 格式后，再由本项目的 skill 整理为 HTML 报告。

```text
微信本地数据库 → [wechat-insight 提取] → JSONL → [生成报告] → HTML 报告
```

## 使用方式

在 Codex 中调用对应 skill，并提供聊天文本或本地导出文件：

```text
使用 $wechat-group-report 分析这份聊天记录，生成群聊周报：/path/to/messages.csv
```
