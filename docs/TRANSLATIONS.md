# Adding a New Language

> 添加新语言 · 新しい言語の追加 · 새 언어 추가

The UI translations are plain JSON files loaded from `resources/locales/`. Adding a language is just dropping in one new file — no recompilation needed.

## How it works

Each locale file maps dotted translation keys to localized strings:

```json
{
  "_language_name": "Français",
  "menu": {
    "file": "Fichier",
    "file.new_project": "Nouveau Projet"
  },
  "getting_started": {
    "welcome": "Bienvenue !"
  }
}
```

The runtime calls `lf.ui.tr("menu.file.new_project")` — the key is resolved against the active locale file (falling back to English if missing).

## Step-by-step

1. **Copy the template**: start from `en.json` (the source of truth with all 2,049 keys):

   ```bash
   cp resources/locales/en.json resources/locales/ru.json
   ```

2. **Translate the values** (never touch the keys, keep JSON valid — no trailing commas).

3. **Set the language name**:

   ```json
   { "_language_name": "Русский", ... }
   ```

4. **Test**: launch the app and switch language in Settings → Preferences → Language.

5. **Share it**: open a PR or issue on the repository, or just publish the file for others to download into their `resources/locales/`.

## Tips

- Keep `_language_name` in the language's own script (e.g. `Русский`, `العربية`).
- If a key is missing in your file, the UI falls back to English — safe to ship partial translations.
- Preserve `{placeholder}` tokens in strings like `"Downloading {url}..."`.
- Keep the file UTF-8 encoded (no BOM).

## Checklist

- [ ] All 2,049 keys from `en.json` present
- [ ] `_language_name` set in the language's own script
- [ ] Valid JSON (no trailing commas, UTF-8)
- [ ] `{placeholders}` preserved
