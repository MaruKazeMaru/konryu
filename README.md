# konryu
![test_result](https://github.com/MaruKazeMaru/konryu/actions/workflows/python-package.yml/badge.svg)<br>
minimum Jinja2 CLI tools

## 概要
Pythonパッケージです。<br>
Jinja2を使って複数ファイルを一度にレンダリングするCLIアプリを提供します。<br>
用途として静的webサイトの構築を想定しています。


## インストール
```sh
git clone https://github.com/MaruKazeMaru/konryu
cd konryu
pip install .
```


## 使用例
```
d
├── plan.txt
└── in
    ├── base.html
    └── render.html
```

in/base.html
```
{%- block body -%}
{%- endblock -%}
```

in/render.html
```
{% extends "base.html" %}
{%- block body -%}
render
{%- endblock -%}
```

plan.txt
```
SRC_DIR=in
DST_DIR=out

RENDER *.html
IGNORE base.html
```

ディレクトリdにて次のコマンドを実行します。
```sh
konryu plan.txt
```
すると次のようなディレクトリoutが出力されます。
```
d
├── plan.txt
├── in
│   ├── base.html
│   └── render.html
└── out
    └── render.html
```
out/render.html
```
render
```

