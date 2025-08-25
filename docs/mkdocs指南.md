# MkDocs指南

## 安装MkDocs

参考 readthedocs 的 [MkDocs指南](https://docs.readthedocs.io/en/stable/intro/getting-started-with-mkdocs.html) 、[MkDocs文档](https://www.mkdocs.org/user-guide/)

安装需求的库：

```sh
# 安装 mkdocs 库
pip install mkdocs
```

创建项目，在项目目录 `D:\Project` 下执行以下操作：

```sh
mkdocs new .
```

目录结构：

```sh
D:\Project
│  .readthedocs.yaml      # ReadtheDocs主配置文件。需要自己手动创建。
│  mkdocs.yml             # mkdocs 主配置文件。由 mkdocs 生成。
│
└─docs                    # 文档主目录
        index.md          # 文档主页显示内容
        requirements.txt  # ReadtheDocs 需要的依赖文件，必须。
```

readthedocs配置文件 `.readthedocs.yaml` 内容：

```yaml
# Read the Docs configuration file for MkDocs projects
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-lts-latest
  tools:
    python: latest

mkdocs:
  configuration: mkdocs.yml

# Optionally declare the Python requirements required to build your docs
python:
  install:
  - requirements: docs/requirements.txt
```

运行以下命令，然后在浏览器中打开 <http://127.0.0.1:8000> 实时预览。

```sh
# 建议加上 --watch-theme 参数，实时监控主题修改变化
mkdocs serve --watch-theme
```

Build the documentation site，生成静态文件至目录 `site` 。

```sh
mkdocs build
```

## 安装 Material for MkDocs 主题

[Material for MkDocs 主题文档](https://squidfunk.github.io/mkdocs-material/getting-started/)

安装 material 主题，非常漂亮，而且支持暗黑模式。

```sh
pip install mkdocs-material
```

修改 mkdocs.yml 配置文件：

```yaml
site_name: My site
site_url: https://mydomain.org/mysite
theme:
  name: material
```

## 安装 mkdocstrings

自动生成文档，参考：<https://mkdocstrings.github.io/python/usage/>

```shell
pip install mkdocstrings[python]
```
