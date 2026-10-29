# Directory Structure

## Standard Layout

```
my-app/
├── assets/
│   ├── images/           # Static images (supports @2x, @3x)
│   │   ├── tabIcons/     # Tab bar icons
│   │   ├── icon.png
│   │   ├── splash-icon.png
│   │   └── favicon.png
│   └── expo.icon/        # iOS app icon format
├── scripts/
│   └── reset-project.js
├── src/
│   ├── app/              # Routes ONLY (file-based routing)
│   │   ├── _layout.tsx   # Root layout
│   │   ├── index.tsx     # Home screen (/)
│   │   └── explore.tsx   # Explore screen (/explore)
│   ├── components/       # Reusable UI components
│   │   ├── ui/           # Sub-components grouped by domain
│   ├── constants/        # Theme, config, spacing
│   ├── hooks/            # Custom hooks
│   └── global.css        # CSS variables for web
├── app.json
├── tsconfig.json
├── package.json
└── .gitignore
```

## Directory Rules

| Directory | Contains | Rule |
|---|---|---|
| `src/app/` | Routes only | Each file = one route. No non-route files. |
| `src/components/` | Reusable UI | Organize by domain with subdirectories as needed. |
| `src/hooks/` | Custom hooks | One hook per file. |
| `src/constants/` | Constants | Theme, spacing, global config. |
| `assets/images/` | Static images | Supports `@2x` and `@3x` density suffixes. |

## Platform-Specific Files

Expo resolves platform-specific extensions automatically:

- `component.tsx` — used on native (iOS/Android)
- `component.web.tsx` — used on web
- `component.native.tsx` — used on both iOS and Android

Import without extension — Expo picks the right file at build time.
