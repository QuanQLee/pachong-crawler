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
python -m crawler.main --seed <起始 URL> --rate <每秒请求数>
```

- `--seed` 可以指定多个，用于设置爬取的初始链接。
- `--rate` 用于控制请求频率，避免过快访问目标网站。
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

也可以通过 Docker 或 docker-compose 运行：

```bash
docker build -t pachong-crawler .
# 或
docker-compose up
```

## 运行测试

项目包含一些基本测试，可使用 `pytest` 运行：

```bash
PYTHONPATH=. pytest -q
```

