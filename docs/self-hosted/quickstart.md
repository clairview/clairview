---
description:
  If you're looking for the fastest way to get up-and-running with Clairview locally, this guide will get you there in minutes.
---

<script setup lang="ts">
import { data as packages } from '@/data/packages.data.js';
</script>

# Self-Hosting Quickstart

<iframe style="width:100%; aspect-ratio:16/9; margin-top: 2em;" src="https://www.youtube.com/embed/J7tFWxAGkh4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Install Docker

You should have Docker installed and running on your machine. You can
[download it here](https://docs.docker.com/get-docker/).

::: info What Is Docker?

Docker is a developer tool that allows software-creators to distribute their work along with all dependencies and
required environment settings. This means that applications can run reliably and consistently, making it the perfect way
to use Clairview both locally and in-production.

As soon as there are new releases of Clairview, we publish them on
[Docker Hub](https://hub.docker.com/r/clairview/clairview).

:::

## Create a Docker Compose File

Create a new empty folder on your Desktop called `clairview`. Within this new folder, create the three empty folders
`database`, `uploads`, and `extensions`.

Open a text editor such as Visual Studio Code, nano, Vim, TextEdit, or Notepad.

Copy and paste the following and save the file as `docker-compose.yml`:

```yaml-vue
version: "3"
services:
  clairview:
    image: clairview/clairview:{{ packages.clairview.version.full }}
    ports:
      - 8055:8055
    volumes:
      - ./database:/clairview/database
      - ./uploads:/clairview/uploads
      - ./extensions:/clairview/extensions
    environment:
      SECRET: "replace-with-secure-random-value"
      ADMIN_EMAIL: "developers@digi-trans.org"
      ADMIN_PASSWORD: "d1r3ctu5"
      DB_CLIENT: "sqlite3"
      DB_FILENAME: "/clairview/database/data.db"
      WEBSOCKETS_ENABLED: "true"
```

Save the file. Let's step through it:

- This file defines a single Docker container that will use the specified version of the `clairview/clairview` image.
- The `ports` list maps internal port `8055` is made available to our machine using the same port number, meaning we can
  access it from our computer's browser.
- The`volumes` section maps internal `database`, `uploads` and `extensions` data to our local file system alongside the
  `docker-compose.yml` - meaning data is stored and persisted outside of Docker containers.
- The `environment` section contains any [configuration variables](/self-hosted/config-options.html) we wish to set.
  - `SECRET` is required and should be a secure random value, it's used to sign tokens.
  - `ADMIN_EMAIL` and `ADMIN_PASSWORD` is the initial admin user credentials on first launch.
  - `DB_CLIENT` and `DB_FILENAME` are defining the connection to your database.
  - `WEBSOCKETS_ENABLED` is not required, but enables [Clairview Realtime](/guides/real-time/getting-started/index.html).

The volumes section is not required, but without this, our database and file uploads will be destroyed when the Docker
container stops running. The default database is SQLite - a self-contained server-less database that stores data to a
file.

## Run Clairview

::: tabs

== macOS/Linux

Open the Terminal and run the following commands one line at a time:

```
cd Desktop/clairview
docker compose up
```

== Windows

Open the Command Line and run the following commands one line at a time:

```
cd Desktop\clairview
docker compose up
```

:::

Clairview should now be available at http://localhost:8055 or http://127.0.0.1:8055.
