# `@clairview/release-notes-generator`

A release notes generator for [`changesets`](https://github.com/changesets/changesets) used by Clairview

## Installation

```shell
npm install @clairview/release-notes-generator
```

## Usage

Update the `.changeset/config.json` file to point to this package:

```json
	"changelog": "@clairview/release-notes-generator",
```

The release notes will be generated and printed when running the `changesets` command to update the versions:

```shell
GITHUB_TOKEN=<token> pnpm changeset version
```

For local use, you'll need a
[GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
with `read:user` and `repo:status` permissions.

To force the main version:

```shell
CLAIRVIEW_VERSION=10.0.0 GITHUB_TOKEN=<token> pnpm changeset version

# To force a prerelease version you need to be in prerelease mode
pnpm changeset pre enter beta
CLAIRVIEW_VERSION=10.0.0-beta.0 GITHUB_TOKEN=<token> pnpm changeset version
```

### GitHub CI

When running `pnpm changeset version` in the GitHub CI context, this package will automatically set the following
outputs:

- `CLAIRVIEW_VERSION`
- `CLAIRVIEW_PRERELEASE`
- `CLAIRVIEW_PRERELEASE_ID` (available if `CLAIRVIEW_PRERELEASE` is `true`)
- `CLAIRVIEW_RELEASE_NOTES`

## Special Changesets Features

### Notices in Changesets

In addition to the normal content, changeset may include a notice to draw special attention to a change. These notices
will be rendered in the release notes under the section "⚠️ Potential Breaking Changes".

Use the following format to add such a notice:

<!-- prettier-ignore -->
```md
---
'example-package': patch
---

::: notice
Notices can contain any markdown syntax

- An important notice
:::

Normal changeset summary
```
