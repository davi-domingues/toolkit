# Assets & Images

## Image Naming

Images in `assets/images/` support `@2x` and `@3x` density suffixes:

```
icon.png          → 1x (baseline)
icon@2x.png       → 2x (Retina)
icon@3x.png       → 3x (high-density)
```

Tab icons go in `assets/images/tabIcons/`.

## Loading Images

Use `expo-image` (`Image` component) instead of React Native's `Image`:

```typescript
import { Image } from 'expo-image';

<Image source={require('@/assets/images/icon.png')} />
```

Use `require()` for build-time resolution (supports `@/assets/` alias).

## System Icons

Use `expo-symbols` `SymbolView` for platform-native icons:

```typescript
import { SymbolView } from 'expo-symbols';

<SymbolView name="house.fill" size={24} tintColor={colors.text} />
```

- iOS: SF Symbols
- Android: Material Icons (mapped automatically)
