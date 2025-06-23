# pachong-crawler

pachong-crawler 是一个示例爬虫项目，包含命令行工具和简易的 Web 界面，可用于演示如何抓取网页并发现其中的链接。

## 环境准备

1. 安装 Python 3.11 及以上版本。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 命令行使用

执行以下命令即可启动爬虫：

```bash
python -m crawler.main --seed <起始 URL> --rate <每秒请求数> --output-dir out
```

- `--seed` 可以指定多个，用于设置爬取的初始链接。
- `--rate` 用于控制请求频率，避免过快访问目标网站。
- `--output-dir` 用于指定抓取结果保存目录，默认为 `data`。
- 也可以通过 `--config` 指定 YAML/JSON 配置文件来提供这些参数。

示例配置文件 `config.yaml`：

```yaml
seeds:
  - "https://example.com"
rate: 1.0
```

运行：

```bash
python -m crawler.main --config config.yaml
```

## Web 界面

项目提供了一个基于 Flask 的简单前端，可在浏览器中输入网址并查看发现的链接：

```bash
python frontend/app.py
```

启动后访问 <http://localhost:8000> 即可使用。

## Docker 方式

也可以通过 Docker 或 docker-compose 运行。

首先构建镜像：

```bash
docker build -t pachong-crawler .
```

镜像默认会执行 `python -m crawler.main`，脚本仅打印参数后即退出。如果想在容器中运行 Web 前端，可使用：

```bash
docker run -p 8000:8000 pachong-crawler python frontend/app.py
```

若要保存抓取结果到宿主机目录，可挂载卷并指定 `--output-dir`：

```bash
docker run -v $(pwd)/out:/data pachong-crawler \
  python -m crawler.main --seed https://example.com --output-dir /data
```

若使用 `docker-compose`，可启动 `frontend` 服务：

```bash
docker-compose up frontend
```

## 运行测试

项目包含一些基本测试，可使用 `pytest` 运行：

```bash
PYTHONPATH=. pytest -q
```

