---
description: How to host Clairview on Docker.
readTime: 3 min read
---

<script setup lang="ts">
import { data as packages } from '@/data/packages.data.js';
</script>

# Docker Guide

::: info Non-Docker Guides

We only publish and maintain self-hosting guides using Docker as this removes many environment-specific configuration
problems. If you can't or don't want to use Docker, we also publish an
[npm package](https://www.npmjs.com/package/clairview) without guides.

:::

Clairview is published to [Docker Hub](https://hub.docker.com/r/clairview/clairview) under `clairview/clairview`. If you're
just getting started, check out our [Self-Hosting Quickstart](/self-hosted/quickstart.html).

## Installing Specific Versions

To stick to a more specific version of Clairview you can use one of the following tags:

- Full version, e.g. `{{ packages.clairview.version.full }}`
- Minor releases, e.g. `{{ packages.clairview.version.minor }}`
- Major releases, e.g. `{{ packages.clairview.version.major }}`

It is recommended to explicitly specify a Clairview version in your `docker-compose.yml` file. Include the version number
in your `services.clairview.image` value:

```yaml-vue
services:
  clairview:
    image: clairview/clairview:latest // [!code --]
    image: clairview/clairview:{{ packages.clairview.version.full }} // [!code ++]
```

## Configure Admin User

The `ADMIN_EMAIL` and `ADMIN_PASSWORD` variables, while shown in the quickstart, are optional. If omitted, the published
Docker image will automatically populate the database and create an admin user, and these will only be shown in the
Docker bootstrap logs when starting Clairview for the first time. To configure the email/password for this first user,
include the following environment variables:

```bash
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="d1r3ctu5"
```

Once you've started Clairview for the first time, assuming your database is persisted, you can remove these values from
your compose file.

## Persistence

Containers are ephemeral, and this means that whenever you stop a container, all the data associated with it is going to
be removed [unless you persist them](https://docs.docker.com/storage) when creating your container.

Clairview image by default will use the following locations for data persistence (note that these can be changed through
environment variables):

- `/clairview/database` (only when using SQLite and not configured to a different folder)
- `/clairview/uploads` for uploads
- `/clairview/extensions` for loading extensions
- `/clairview/templates` for overriding and extending email templates

The `services.clairview.volumes` section in your docker-compose.yml is optional. To persist data to your local machine,
include a list of persisted directories:

```yaml
services:
  clairview:
    volumes:
      - ./database:/clairview/database
      - ./uploads:/clairview/uploads
      - ./extensions:/clairview/extensions
      - ./templates:/clairview/templates
```

## Example Docker Compose

While the [Self-Hosting Quickstart](/self-hosted/quickstart.html) aims to show you the minimum-viable
`docker-compose.yml` file, here is a more complete one that spins up a Postgres database, Redis cache, and Clairview
project:

```yaml-vue
version: "3"
services:
  database:
    image: postgis/postgis:13-master
    # Required when running on platform other than amd64, like Apple M1/M2:
    # platform: linux/amd64
    volumes:
      - ./data/database:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: "clairview"
      POSTGRES_PASSWORD: "clairview"
      POSTGRES_DB: "clairview"
    healthcheck:
      test: ["CMD", "pg_isready", "--host=localhost", "--username=clairview"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_interval: 5s
      start_period: 30s

  cache:
    image: redis:6
    healthcheck:
      test: ["CMD-SHELL", "[ $$(redis-cli ping) = 'PONG' ]"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_interval: 5s
      start_period: 30s

  clairview:
    image: clairview/clairview:{{ packages.clairview.version.full }}
    ports:
      - 8055:8055
    volumes:
      - ./uploads:/clairview/uploads
      - ./extensions:/clairview/extensions
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy
    environment:
      SECRET: "replace-with-secure-random-value"

      DB_CLIENT: "pg"
      DB_HOST: "database"
      DB_PORT: "5432"
      DB_DATABASE: "clairview"
      DB_USER: "clairview"
      DB_PASSWORD: "clairview"

      CACHE_ENABLED: "true"
      CACHE_AUTO_PURGE: "true"
      CACHE_STORE: "redis"
      REDIS: "redis://cache:6379"

      ADMIN_EMAIL: "admin@example.com"
      ADMIN_PASSWORD: "d1r3ctu5"

      # Make sure to set this in production
      # (see https://docs.clairview.io/self-hosted/config-options#general)
      # PUBLIC_URL: "https://clairview.example.com"

    # Environment variables can also be defined in a file (for example `.env`):
    # env_file:
    #	  - .env
```

### Updating With Docker Compose

If you are not using the `latest` tag for the Clairview image you need to adjust your `docker-compose.yml` file to
increment the tag version number, e.g.:

```diff-vue
-   image: clairview/clairview:{{ packages.clairview.version.major }}.0.0
+   image: clairview/clairview:{{ packages.clairview.version.full }}
```

Then run the following from your docker-compose root:

```bash
docker compose up
```

The specified image will be pulled and the containers recreated. Migrations will happen automatically so once the
containers have started you will be on the latest version (or the version you specified).

## Supported Databases

The Clairview Docker Image contains all optional dependencies supported in the API. This means the Docker image can be
used with most of the supported databases and storage adapters without having to create a custom image.

Clairview supports the LTS versions of PostgreSQL, MySQL, SQLite, MS SQL Server, MariaDB, CockroachDB, and OracleDB.
Please see https://endoflife.date/ to make sure your database version is still supported.

## Requirements

It can be easy to under-provision resources to run a self-hosted instance of Clairview. For Clairview' container
resources, the required minimum system requirements are 1x 0.25 vCPU / 512 MB, although the recommended minimum is 2x 1
vCPU / 2GB.
