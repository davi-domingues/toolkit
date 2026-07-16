# Coding Standards

## 1. No Comments in Production Code

Do not add comments to production code. Code should be self-documenting.

## 2. Path Aliases

```typescript
import { Something } from '@/components/something';     // src/components/something
import icon from '@/assets/images/icon.png';             // assets/images/icon.png
```

Configured in `tsconfig.json` paths: `@/*` → `./src/*`, `@/assets/*` → `./assets/*`.

## 3. Platform-Specific Files

- `component.tsx` → native (iOS/Android)
- `component.web.tsx` → web
- `component.native.tsx` → both iOS and Android

Expo auto-resolves the correct file at build time based on platform.

## 4. CSS Modules for Web

For web-specific styles, use `*.module.css`:

```typescript
import classes from './style.module.css';
// <div className={classes.xxx} />
```

Only in `.web.tsx` components. DOM elements use `className`, not `style`.

## 5. Theme via Hooks

Use `useTheme()` to access current colors. Use `ThemedText` and `ThemedView` for theme-aware elements.

## 6. Icons

Use `SymbolView` from `expo-symbols` for system icons (SF Symbols on iOS, Material Icons on Android).

## 7. Safe Area

Use `react-native-safe-area-context`:

```typescript
import { SafeAreaView } from 'react-native-safe-area-context';
// or
import { useSafeAreaInsets } from 'react-native-safe-area-context';
const insets = useSafeAreaInsets();
```

## 8. Animations

Use `react-native-reanimated` with `Keyframe` for entrance animations. Use `react-native-worklets` for calling `setState` from worklet threads.

## 9. Images

Always use `Image` from `expo-image` over React Native's `Image` component.

## 10. External Links

Use `ExternalLink` component (wraps `expo-router` `Link` + `expo-web-browser` on native).

## 11. `EXPO_OS` Over `Platform.OS`

```typescript
if (process.env.EXPO_OS !== 'web') { /* native-only logic */ }
```

Prefer `process.env.EXPO_OS` over `Platform.OS` for platform-conditional code.

## 12. Versioned Documentation

Always consult `https://docs.expo.dev/versions/v<SDK>/` for the correct API for the target SDK version.
