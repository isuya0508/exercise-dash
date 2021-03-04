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

## アプリの実行に関して

* アプリごとにディレクトリを分けている。その中の`app.py`がアプリモジュールである。
* 以下の手順で`app.py`を実行できる。
  ```
  cd [アプリのディレクトリ]
  python app.py
  ```

  その後、http://127.0.0.1:8050/ にアクセスする。