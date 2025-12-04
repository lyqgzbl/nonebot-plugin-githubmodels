<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# nonebot-plugin-githubmodels

_✨ 一个调用 GitHub Models 的 AI 对话插件 ✨_

![License](https://img.shields.io/pypi/l/nonebot-plugin-githubmodels)
![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-githubmodels.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)  
[![NoneBot Registry](https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-githubmodels)](https://registry.nonebot.dev/plugin/nonebot-plugin-githubmodels:nonebot_plugin_githubmodels)
[![Supported Adapters](https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot-plugin-alconna)](https://registry.nonebot.dev/plugin/nonebot-plugin-alconna:nonebot_plugin_alconna)

</div>

## 安装
使用nb-cli [推荐]
```shell
nb plugin install nonebot-plugin-githubmodels
```
使用pip
```shell
pip install nonebot-plugin-githubmodels
```

## 使用
命令需要加 [NoneBot 命令前缀](https://nonebot.dev/docs/appendices/config#command-start-和-command-separator) (默认为`/`)  
使用命令`AI`/`ai`触发插件  
命令选项`-r` 重置上下文记忆  
命令选项`-i` 临时启用图片回复  

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可

### github_token [必填]

- 类型：`str`
- 默认值：`None`
- 说明：用于访问 GitHub Models 的 GitHub token

### max_context_length [选填]

- 类型：`int`
- 默认值：`20`
- 说明：记忆的上下文数量的最大值

### ai_reply_image [选填]


- 类型: `bool`
- 默认: `False`
- 说明: 是否以图片的形式回复

### ai_model_name [选填]

- 类型: `str`
- 默认: `openai/gpt-4.1-mini`
- 说明: 所使用的模型

### ai_temperature [选填]

- 类型: `float`
- 默认: `1.0`
- 说明: 生成的文本的多样性和连贯性

## ai_top_p [选填]

- 类型: `float`
- 默认: `1.0`
- 说明: 生成文本随机性