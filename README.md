# Exercise-Dash

* [Dash](https://dash.plotly.com/)でダッシュボードを作成する練習プロジェクト

## 環境

* OS: Ubuntu20.04
* Python: Python3.9.0

## セットアップ

* `requirements.txt`に書かれたパッケージをインストールする

  ```
  pip install -r requirements.txt
  ```

## 開発

* `pre-commit`を利用して、commit時に`flake8`と`mypy`のチェックが走るようにする。

  ```
  pip install pre-commit==2.9.3
  pre-commit install
  ```

  チェックの内容は、`.pre-commit-config.yaml`に記述されている。
