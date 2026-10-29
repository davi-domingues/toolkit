# Routing & Navigation

Expo uses **Expo Router** — file-based routing powered by `react-native-screens`.

## Layout (`src/app/_layout.tsx`)

```typescript
import { DarkTheme, DefaultTheme, ThemeProvider } from 'expo-router';
import { useColorScheme } from 'react-native';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      {/* navigation content */}
    </ThemeProvider>
  );
}
```

Each file in `src/app/` becomes a route: `index.tsx` → `/`, `explore.tsx` → `/explore`.

Enable typed routes in `app.json`: `"experiments.typedRoutes": true`.

## Native Tabs (Android/iOS)

Uses `expo-router/unstable-native-tabs`:

```typescript
import { NativeTabs } from 'expo-router/unstable-native-tabs';

<NativeTabs backgroundColor={...} indicatorColor={...}>
  <NativeTabs.Trigger name="index">
    <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
    <NativeTabs.Trigger.Icon src={require('...')} renderingMode="template" />
  </NativeTabs.Trigger>
</NativeTabs>
```

## Web Tabs

Uses `expo-router/ui` (`Tabs`, `TabList`, `TabTrigger`, `TabSlot`):

```typescript
import { Tabs, TabList, TabTrigger, TabSlot } from 'expo-router/ui';

<Tabs>
  <TabSlot style={{ height: '100%' }} />
  <TabList asChild>
    <CustomTabList>
      <TabTrigger name="home" href="/" asChild>
        <TabButton>Home</TabButton>
      </TabTrigger>
    </CustomTabList>
  </TabList>
</Tabs>
```

## Platform-Specific Component Pattern

Every component with different native vs web behavior gets two files:

- `app-tabs.tsx` → native implementation
- `app-tabs.web.tsx` → web implementation

Expo auto-resolves `.web.tsx` on web, `.tsx` on native.

## Deep Linking

Define `"scheme": "myapp"` in `app.json` → routes accessible via `myapp://route-path`.
