# Build a Django App with TiDB

English | [中文](/README-zh.md)

This a sample project written by PingCAP for Django to connect to TiDB.

This is an example of a game where each player has three attributes: `name`, `coins` and `goods`, and each player has a field `id` that uniquely identifies the player. Players can trade freely if they have enough coins and goods.

## Prerequisites

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- A TiDB cluster. If you don't have a TiDB cluster, you can create one as follows:
  - (Recommended) Follow [Creating a TiDB Serverless Cluster](https://docs.pingcap.com/tidbcloud/dev-guide-build-cluster-in-cloud) to create your own TiDB Cloud cluster.
  - Follow [Deploy a Local Test TiDB Cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a Production TiDB Cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster

## Getting started

### 1. Clone the repository

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 2. Install dependencies (including Django, django-tidb and mysqlclient)

```shell
pip install -r requirements.txt
```

#### Why do we need to install django-tidb and mysqlclient?

- `django-tidb` is a TiDB dialect for Django that addresses compatibility issues between them. For more information, please refer to the [django-tidb repository](https://github.com/pingcap/django-tidb).
- `mysqlclient` is a MySQL driver for Python that is officially supported by Django and django-tidb. It enables communication between Django and the TiDB server. For more information, please refer to the [mysqlclient repository](https://github.com/PyMySQL/mysqlclient).

#### How to choose the right version of django-tidb

The version of `django-tidb` should match the version of `django`, for example, if you are using `django 4.2.x`, you should install `django-tidb 4.2.x` (the minor release number do not need to be the same, use the latest minor release of each). You can find the detailed version mapping in the [django-tidb official documentation](https://github.com/pingcap/django-tidb#installing-django-tidb)

#### Encountering problems when installing mysqlclient

If this is your first time installing mysqlclient, you may encounter some problems as it is not only a pure Python package, but also requires some C extensions. To resolve them, please refer to the [mysqlclient official documentation](https://github.com/PyMySQL/mysqlclient#install)

### 3. Configure connection information

<details open>
<summary><b>(Option 1) TiDB Serverless</b></summary>

1. In the TiDB Cloud, navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, select your TiDB Serverless cluster. Go to the **Overview** page, and click the **Connect** button in the upper right corner.
2. Ensure the configurations in the confirmation window match your operating environment.
    - **Endpoint Type** is set to **Public**
    - **Connect With** is set to **General**
    - Operating System matches your environment
    > If you are running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.
3. Click **Create password** to create a password.
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.
4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

5. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

   ```python
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    Be sure to replace the placeholders `{}` with the values obtained from the connection dialog.

    TiDB Serverless requires a secure connection. Since the `ssl_mode` of mysqlclient defaults to `PREFERRED`, you don't need to manually specify `CA_PATH`. Just leave it empty. But if you have a special reason to specify `CA_PATH` manually, you can refer to the [TLS Connections to TiDB Serverless](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) to get the certificate paths for different operating systems.

6. Save the `.env` file.

</details>

<details>

<summary><b>(Option 2) TiDB Dedicated</b></summary>

1. In the TiDB Cloud, select your TiDB Dedicated cluster. Go to the **Overview** page, and click the **Connect** button in the upper right corner. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the certificate.
    > For more configuration details, refer to [TiDB Dedicated Standard Connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).
2. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

3. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

   ```python
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    Be sure to replace the placeholders `{}` with the values obtained from the **Connect** window, and configure `CA_PATH` with the certificate path downloaded in the previous step.

4. Save the `.env` file.

</details>

<details>
<summary><b>(Option 3) Self-Hosted TiDB</b></summary>

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

    ```python
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Be sure to replace the placeholders `{}` with the values, and remove the `CA_PATH` line. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</details>

### 4. Migrate the database

```shell
python manage.py migrate
```

### 5. Run server

```shell
python manage.py runserver
```

> The default port is 8000. If you want to change the port, you can add the port number after the command, for example: `python manage.py runserver 8080`

### 6. Explore the sample app

Access the application in your browser via <http://127.0.0.1:8000>. If you've modified the port, replace 8000 with your specified port number.

Within the application, you can:

- Create a new player
- Bulk create players
- View all players at
- View a player's details
- Delete a player
- Trade with a player

## Next Steps

- You can continue reading the developer documentation to get more knowledge about TiDB development, such as: [Insert Data](https://docs.pingcap.com/tidb/stable/dev-guide-insert-data), [Update Data](https://docs.pingcap.com/tidb/stable/dev-guide-update-data), [Delete Data](https://docs.pingcap.com/tidb/stable/dev-guide-delete-data), [Single Table Reading](https://docs.pingcap.com/tidb/stable/dev-guide-get-data-from-single-table), [Transactions](https://docs.pingcap.com/tidb/stable/dev-guide-transaction-overview), [SQL Performance Optimization](https://docs.pingcap.com/tidb/stable/dev-guide-optimize-sql-overview), etc.
- If you prefer to learn through courses, we also offer professional [TiDB Developer Courses](https://www.pingcap.com/education/), and provide [TiDB certifications](https://www.pingcap.com/education/certification/) after the exam.
