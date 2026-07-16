# Components

## ThemedText

A text component with predefined types and theme-aware colors:

```typescript
type ThemedTextProps = TextProps & {
  type?: 'default' | 'title' | 'small' | 'smallBold' | 'subtitle' | 'link' | 'linkPrimary' | 'code';
  themeColor?: ThemeColor;
};
```

## ThemedView

A view with theme-aware background color:

```typescript
type ThemedViewProps = ViewProps & {
  type?: ThemeColor;  // 'background' | 'backgroundElement' | 'backgroundSelected'
};
```

## ExternalLink

Opens in system browser (native) or new tab (web):

```typescript
export function ExternalLink({ href, ...rest }: Props) {
  return (
    <Link target="_blank" {...rest} href={href}
      onPress={async (event) => {
        if (process.env.EXPO_OS !== 'web') {
          event.preventDefault();
          await openBrowserAsync(href, { presentationStyle: WebBrowserPresentationStyle.AUTOMATIC });
        }
      }}
    />
  );
}
```

Uses `expo-web-browser` on native, `<a target="_blank">` on web.

## Collapsible

Expandable section with `react-native-reanimated` animation:

```typescript
export function Collapsible({ children, title }: PropsWithChildren & { title: string }) {
  const [isOpen, setIsOpen] = useState(false);
  // Uses Animated.View with entering={FadeIn.duration(200)}
}
```

## AnimatedIcon / AnimatedSplashOverlay

Splash animation using `react-native-reanimated` `Keyframe`:
- **Native**: scales a giant icon down to normal size, then hides overlay.
- **Web**: simpler elastic bounce animation, no splash overlay.

Uses `react-native-worklets` with `scheduleOnRN` for `setState` outside worklet thread.
