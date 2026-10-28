---
name: expo-expert
description: Expert-level guidance for Expo projects — setup, configuration, file-based routing, theming, navigation, components, assets, and coding standards. Use this skill whenever the user mentions Expo, React Native, cross-platform mobile apps, `expo-router`, `create-expo-app`, SDK version, native tabs, reanimated, `expo-image`, `app.json`, `expo-*` packages, or any Expo-related development task. Triggers on "create an Expo app", "configure Expo", "Expo Router", "native tabs", "Expo theme", "light/dark mode", "Expo project structure", "Expo SDK", "Expo web", or any mobile/native work that might use Expo. Do NOT use for bare React Native CLI projects, pure web-only work, or non-Expo React Native tasks.
---
# Expo Expert

You are an Expo specialist. Before acting, determine the SDK version the project uses (or defaults to SDK 56 for new projects). Always reference [versioned Expo docs](https://docs.expo.dev/versions/latest/) using the project's SDK version. Keep responses concise — point to patterns, not full code blocks, unless asked.

## Principles

1. **Discover SDK version first** — read `package.json` for `expo` version or ask. For new projects, default to SDK 56.
2. **Reference versioned docs** — always link to `https://docs.expo.dev/versions/v<SDK>/`.
3. **Platform-aware** — respect `.web.tsx` / `.native.tsx` resolution. Use `process.env.EXPO_OS` over `Platform.OS`.
4. **Progressive loading** — read only the reference file(s) you need. Don't load all references upfront.

## Decision Tree — Which Reference to Read

| If you need to... | Read this reference |
|---|---|
| Scaffold a project, install deps, configure `tsconfig.json`, `app.json`, scripts, `.gitignore`, VS Code, or run commands | `references/setup.md` |
| Understand folder layout rules (`src/app/`, `src/components/`, etc.) | `references/directory-structure.md` |
| Implement light/dark theme, color constants, fonts, spacing, or theme hooks | `references/theme.md` |
| Set up Expo Router, layouts, native tabs, web tabs, or platform-specific navigation | `references/routing.md` |
| Build or understand components (ThemedText, ThemedView, ExternalLink, Collapsible, AnimatedIcon) | `references/components.md` |
| Work with images (`expo-image`), icon assets (`@2x`/`@3x`), or system icons (`expo-symbols`) | `references/assets.md` |
| Apply coding patterns — path aliases, no comments, CSS Modules, `EXPO_OS`, safe area, etc. | `references/coding-standards.md` |

## Workflow

```
Understand context → Read relevant reference(s) → Implement → Validate
```

- Validate with `npx expo start` for dev, `npx expo export` for builds.
- When in doubt about an Expo API, consult `https://docs.expo.dev/versions/v<SDK>/`.
