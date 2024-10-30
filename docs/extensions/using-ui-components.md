---
description: Learn how to use the Clairview UI components in your app extensions.
contributors: Esther Agbaje
---

# Using Clairview UI Components

Clairview provides a set of reusable UI components that can be used when building extensions. These components are used
by Clairview itself, and are designed to provide a consistent user experience across different parts of the Clairview Data
Studio.

## Components Playground

Explore the available components in our [Clairview Components Playground](https://components.clairview.io/). Here, you can
see all available components and experiment with variations before implementing them in your extensions.

![Exploring the Button Component and its variations on the Clairview UI Components Playground](https://marketing.clairview.app/assets/46d72f1a-5d9f-49f8-a09a-b2ffc5200812.gif)

## Extension Usage

Clairview UI components are globally registered, making them accessible throughout your extension project without the
need for explicit imports. Here’s an example:

```vue
<VButton>
	My Button
</VButton>
```

## Customizing Styles

Each component exports CSS custom properties (variables) that can be targeted for style overrides.

For example, to adjust the text color of a button on hover:

```vue
<template>
	<!-- give the button a class -->
	<VButton class="my-button">
		My Button
	</VButton>
</template>

<style>
/* customize the style */
.my-button {
	--v-button-color-hover: black;
}
</style>
```

::: tip Explore Component CSS Variables

Refer to the full list of component based CSS variables
[in our codebase](https://github.com/clairview/clairview/tree/main/app/src/components).

:::

## Creating a Custom UI Component

The Clairview UI components are designed with flexibility and customization in mind. However, you may need to create your
own components using shared styling. Clairview exposes several CSS variables for both light and dark themes.

Examples of CSS variables include `--border-normal`, `--foreground-normal` `-purple`, `--module-background`, and
`--overlay-color`.

::: tip Explore Light and Dark Theme CSS Variables

Refer to our [codebase](https://github.com/clairview/clairview/tree/main/app/src/styles/themes) for a full list of CSS
variables.

:::
