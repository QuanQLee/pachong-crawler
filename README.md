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

镜像默认会执行 `python -m crawler.main`。要在容器中运行持续爬取并通过 Web 界面提交 URL，可使用 `docker-compose`：

```bash
docker-compose up
```

如果容器无法访问外网，可在 `docker-compose.yml` 中使用 `network_mode: host` （本仓库已如此配置）以共享宿主机的网络。

启动后访问 <http://localhost:8000> 填写要爬取的地址，并通过 `ws://localhost:8765` 实时接收发现的链接。

## 高级异步爬虫

项目额外提供了一个 `AsyncCrawler` 类，能够使用 `aiohttp` 异步抓取静态页面，并在需要
时自动切换到 Playwright 进行 JS 渲染。所有抓取结果会保存到 SQLite 数据库中，队列也
会持久化，因而支持断点续抓。

示例：

```bash
python -m crawler.async_crawler
```

## Live WebSocket

借助 `LiveWebSocket` 模块，可以在爬虫运行时实时推送发现的链接。

```bash
python -m crawler.run_with_ws
```

启动后连接 `ws://localhost:8765` 即可接收链接消息。

## 运行测试

项目包含一些基本测试，可使用 `pytest` 运行：

```bash
PYTHONPATH=. pytest -q
```

