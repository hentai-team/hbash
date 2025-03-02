# hbash - 高级终端模拟器

![HBash Logo](https://github.com/hentai-team/hbash/blob/main/assets/hbash-splash-ch.png?raw=true)

## 概述
hbash 是一个用 Python 编写的功能丰富的终端模拟器，提供现代命令行界面，具有广泛的功能、用户管理和自定义选项。

## 特点

### 核心功能
- 用户认证和管理
- 多语言支持（英语、俄语）
- 丰富多彩且可自定义的界面
- 命令历史记录
- 别名支持
- 类似 Cron 的任务调度

### 文件操作
- 基本文件操作（cp、mv、rm、mkdir、touch）
- 文件内容查看和操作（cat、head、tail）
- 文件搜索和比较（find、grep、diff）
- 归档管理（zip、unzip、tar、gzip）

### 系统工具
- 系统监控（ps、top、df、free）
- 网络实用工具（ping、ifconfig、ssh、scp）
- 进程管理
- 资源监控

### 附加工具
- 带语法高亮的文本编辑器
- 待办事项管理器
- 笔记系统
- 日历
- 天气信息
- 计时器和秒表

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/hterm.git
```

2. 安装所需依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 启动 HBash
```bash
python hbash.py
```

### 默认登录
默认 root 账户的凭据是：
```bash
用户名：root
密码：root
```
实际上，这个功能只是为了好玩而添加的，将会在新版本中移除。


### 基本命令
- `help` - 显示可用命令
- `quit` - 退出 HTerm
- `clear` - 清屏
- `ver` - 显示版本信息

### 用户管理
- `login` - 登录系统
- `logout` - 登出当前用户
- `adduser` - 添加新用户（仅限 root）
- `deluser` - 删除用户（仅限 root）

### 附加文档

不同语言的详细命令文档可在 docs 文件夹中找到：
[English](https://github.com/hentai-team/hbash/blob/main/docs/commands-en.md) | [Russian](https://github.com/hentai-team/hbash/blob/main/docs/commands-ru.md) | [Japanese](https://github.com/hentai-team/hbash/blob/main/docs/commands-jp.md) | [Chinese](https://github.com/hentai-team/hbash/blob/main/docs/commands-ch.md)

## 配置
- 默认配置存储在 `config.json` 中
- 语言设置在 `localization` 目录中
- 用户数据在 `users.json` 中

## 自定义
- 自定义配色方案
- 可配置的提示符
- 常用命令的别名
- 每个用户的个人设置

## 要求
- Python 3.7+
- 所需包已列在 requirements.txt 中

## 贡献
欢迎贡献！请随时提交拉取请求。

## 许可证
本项目基于 MIT 许可证 - 详情请参见 LICENSE 文件。

## 支持
如需支持，请在 GitHub 仓库中提出问题。

