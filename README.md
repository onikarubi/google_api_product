<p align="center">
  <a href="https://github.com/onikarubi" rel="noopener">
 <img width=200px height=200px style="border-radius: 50%; object-fit: cover;" src="https://source.unsplash.com/2EJCSULRwC8
" alt="Project logo"></a>
</p>

<h3 align="center">My Portfolio</h3>

<p align="center"> sample project
    <br>
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)

## 🧐 About <a name = "about"></a>

パーム油は副菜

## 🏁 Getting Started <a name = "getting_started"></a>
このコンテンツはDockerによるコンテナ内の環境でプログラムが動きます。
プログラムを実行するには[Docker](https://www.docker.com/)が必要なので事前にインストールしてください。

### プロジェクトファイルのダウンロード
下のコマンドを実行し、プロジェクト用のファイルをダウンロードしてください。

```
git clone https://github.com/onikarubi/google_api_product.git
```

### Dockerイメージファイルをビルドし後、コンテナを立ち上げる
プロジェクト配下に移動後、Dockerイメージをビルドしてください。

```
docker-compose up --build -d
```

### pytestの実行
コンテナ起動後にコンテナ内に入り、pytestを実行してPythonのプログラムが正常に動いているか確認してください。

```
docker-compose exec python bash
```

```
python -m pytest test/test_google_cloud_api.py
```

ひとまず以上。
