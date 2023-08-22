# 使用 Django 和 TiDB 构建应用程序

[English](/README.md) | 中文

这是 PingCAP 为 Django 编写的使用 TIDB 构建应用程序的示例项目。

这是一个关于游戏的例子，每个玩家有三个属性：姓名 `name`, 金币数 `coins` 和货物数 `goods`。且每个玩家都拥有一个字段 `id`，作为玩家的唯一标识。玩家在金币数和货物数充足的情况下，可以自由地交易。

## 前置要求

- 推荐 [Python 3.10 及以上版本](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
  - （推荐方式）参考[创建 TiDB Serverless 集群](https://docs.pingcap.com/tidbcloud/dev-guide-build-cluster-in-cloud)，创建你自己的 TiDB Cloud 集群。
  - 参考[部署本地测试 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-tidb#部署本地测试集群)或[部署正式 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/production-deployment-using-tiup)，创建本地集群。

## 开始实践

### 1. 克隆示例代码仓库到本地

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 2. 安装依赖 (包括 Django, django-tidb 和 mysqlclient)

```shell
pip install -r requirements.txt
```

#### 为什么我们还需要安装 django-tidb 和 mysqlclient？

- django-tidb 是由 PingCAP 开发的用于解决 Django 和 TiDB 之间的兼容性问题。更多信息请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)
- mysqlclient 是 Django 和 django-tidb 官方支持的 Python MySQL 驱动，它帮助 Django 和 TiDB 实现具体通信，并且提供了较高的性能。更多信息请参考 [mysqlclient 仓库](https://github.com/PyMySQL/mysqlclient)

#### 如何选择正确的 django-tidb 版本

- django-tidb 的版本应该和 django 的版本匹配，例如，如果你使用的是 `django 4.2.x`，你应该安装 `django-tidb 4.2.x`（最小版本号不需要完全一致，推荐使用各自的最新小版本）。更多信息请参考 [django-tidb 官方文档](https://github.com/pingcap/django-tidb#installing-django-tidb)

#### 安装 mysqlclient 时遇到问题

- 如果这是你第一次安装 mysqlclient，你可能会遇到一些问题，因为它不仅仅是一个纯 Python 包，还需要一些 C 扩展。为了解决这些问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)

### 3. 配置连接信息

<details open>
<summary><b>(选项 1) TiDB Serverless</b></summary>

1. 在 TiDB Cloud 控制台中，打开 [Clusters](https://tidbcloud.com/console/clusters) 页面，选择你的 TiDB Serverless 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。
2. 确认窗口中的配置和你的运行环境一致。
    - **Endpoint Type** 为 **Public**
    - **Connect With** 为 **General**
    - Operating System 为你的运行环境
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。
3. 点击 **Generate password** 生成密码。
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。
4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 复制并粘贴对应连接字符串至 `.env` 中。示例结果如下：

   ```python
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

    TiDB Serverless 要求使用 secure connection，由于 mysqlclient 的 `ssl_mode` 默认为 `PREFERRED`，所以不需要你手动指定 `CA_PATH`，设置为空即可。但如果你有特殊原因需要手动指定 `CA_PATH`，可以参考 [TiDB Cloud 文档](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-default-path)获取不同操作系统下证书的路径。

6. 保存文件。
</details>

<details>

<summary><b>(选项 2) TiDB Dedicated</b></summary>

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Dedicated 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。点击 **Allow Access from Anywhere** 并点击 **Download TiDB cluster CA** 下载证书。
    > 更多配置细节，可参考 [TiDB Dedicated 标准连接教程](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

2. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

3. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

   ```python
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值，并配置前面步骤中下载好的证书路径。

4. 保存文件。

</details>

<details>
<summary><b>(选项 3) 自建 TiDB</b></summary>

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。示例结果如下：

    ```python
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并删除 `CA_PATH` 这行。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存文件。

</details>

### 4. 迁移数据库

```shell
python manage.py migrate
```

### 5. 运行服务器

```shell
python manage.py runserver
```

> 默认端口为 8000。如果你想修改端口，可以在命令后添加端口号，例如：`python manage.py runserver 8080`

### 6. 探索示例应用

在浏览器中访问 <http://127.0.0.1:8000>。如果你修改了端口号，将 8000 替换为你的端口号。

在应用中，你可以：

- 创建新玩家
- 批量创建玩家
- 查看所有玩家
- 查看玩家详情
- 删除玩家
- 与玩家交易

## 下一步

- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的开发者知识。例如：[插入数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-insert-data)，[更新数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-update-data)，[删除数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-delete-data)，[单表读取](https://docs.pingcap.com/zh/tidb/stable/dev-guide-get-data-from-single-table)，[事务](https://docs.pingcap.com/zh/tidb/stable/dev-guide-transaction-overview)，[SQL 性能优化](https://docs.pingcap.com/zh/tidb/stable/dev-guide-optimize-sql-overview)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
