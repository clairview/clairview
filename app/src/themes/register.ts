import type { Theme } from '@clairview/themes';
import { useThemeStore } from '@clairview/themes';

export const registerThemes = (themes: Theme[]) => {
	const themesStore = useThemeStore();
	themes.forEach((theme) => themesStore.registerTheme(theme));
};
