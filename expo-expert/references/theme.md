# Theme System

## Color Constants (`src/constants/theme.ts`)

```typescript
export const Colors = {
  light: {
    text: '#000000',
    background: '#ffffff',
    backgroundElement: '#F0F0F3',
    backgroundSelected: '#E0E1E6',
    textSecondary: '#60646C',
  },
  dark: {
    text: '#ffffff',
    background: '#000000',
    backgroundElement: '#212225',
    backgroundSelected: '#2E3135',
    textSecondary: '#B0B4BA',
  },
} as const;

export type ThemeColor = keyof typeof Colors.light & keyof typeof Colors.dark;
```

Use 5 semantic colors: `text`, `background`, `backgroundElement`, `backgroundSelected`, `textSecondary`.

## Fonts

```typescript
export const Fonts = Platform.select({
  ios: { sans: 'system-ui', serif: 'ui-serif', rounded: 'ui-rounded', mono: 'ui-monospace' },
  default: { sans: 'normal', serif: 'serif', rounded: 'normal', mono: 'monospace' },
  web: { sans: 'var(--font-display)', serif: 'var(--font-serif)', rounded: 'var(--font-rounded)', mono: 'var(--font-mono)' },
});
```

## Spacing

```typescript
export const Spacing = { half: 2, one: 4, two: 8, three: 16, four: 24, five: 32, six: 64 } as const;
```

## Theme Hooks

**`use-color-scheme.ts`** (native): re-exports `useColorScheme` from `react-native`.

**`use-color-scheme.web.ts`** (web SSR-safe):
```typescript
export function useColorScheme() {
  const [hasHydrated, setHasHydrated] = useState(false);
  useEffect(() => { setHasHydrated(true); }, []);
  const colorScheme = useRNColorScheme();
  return hasHydrated ? colorScheme : 'light';
}
```

**`use-theme.ts`**:
```typescript
export function useTheme() {
  const scheme = useColorScheme();
  return Colors[scheme === 'unspecified' ? 'light' : scheme];
}
```

## Web CSS Variables (`src/global.css`)

```css
:root {
  --font-display: Spline Sans, Inter, ui-sans-serif, system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
  --font-rounded: 'SF Pro Rounded', 'Hiragino Maru Gothic ProN', sans-serif;
  --font-serif: Georgia, 'Times New Roman', serif;
}
```

Import in `theme.ts` via `import '@/global.css'`.

## Other Constants

```typescript
export const BottomTabInset = Platform.select({ ios: 50, android: 80 }) ?? 0;
export const MaxContentWidth = 800;
```

## Enabling Theme

Set `"userInterfaceStyle": "automatic"` in `app.json`.
