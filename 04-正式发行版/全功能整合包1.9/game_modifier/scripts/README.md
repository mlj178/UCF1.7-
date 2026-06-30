# scripts/ 废弃历史目录

`scripts/` 不再作为正式运行入口。

- 正式运行不再读取 `scripts/*.js`。
- 本项目使用方案 B：不使用 `common.js`。
- 每个功能的正式 JS 都是 `features/<feature_id>/script.js`。
- 新增功能不要往 `scripts/` 写文件。
- 历史 archive 已删除；需要参考历史实现请查看版本控制记录。
