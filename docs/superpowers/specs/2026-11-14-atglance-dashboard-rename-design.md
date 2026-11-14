# Design Specification: AtGlance Dashboard Rebranding & Migration

- **Date:** 2026-11-14
- **Author:** Adromir
- **Status:** Proposed

---

## 1. Intent & Purpose
The custom Home Assistant dashboard panel originally named **Vision Glass Dashboard** has evolved from a theme-tied Lovelace extension into an independent, all-in-one smart home operating panel featuring an asynchronous Python backend, native area/entity discovery, Bento room cards, tactile controls, and recorder statistics. 

Since the theme was completely decoupled from the dashboard, all legacy naming associations with "Vision Glass" are removed in favor of a distinct, purpose-driven brand: **AtGlance Dashboard**.

---

## 2. Goals, Non-Goals & Anti-Goals

### Goals
- Fully rename the repository, local folder, Python integration domain, custom panel endpoint, and frontend web components to `atglance`.
- Reset project version to `v1.0.0` as the official debut of AtGlance Dashboard.
- Seamless automatic configuration migration: migrate existing `.storage/vision_glass.config` into `.storage/atglance.config` on first run with zero user data loss.
- Ensure the Default Dashboard mechanism updates system-wide and user profiles to route to `/atglance`.
- Rename GitHub repository `adromir/ha-vision-glass-dashboard` -> `adromir/ha-atglance-dashboard`.
- Remove the deprecated `vision_glass` integration and install `adromir/ha-atglance-dashboard` in Home Assistant via HACS.
- Restart Home Assistant and verify operation.

### Non-Goals
- Altering user dashboard layout, existing card styling, or feature logic beyond naming and routing.
- Renaming the companion theme `ha-vision-glass-theme` (stays as separate theme companion).

### Anti-Goals
- Do not leave residual `vision_glass` domains or files in the new codebase.
- Do not require the user to re-configure their rooms, custom badges, or dock items from scratch.

---

## 3. Approaches Considered

- **Approach 1: Full Clean Rebrand with Automatic Storage Migration (PICKED)**
  - Entire codebase (`custom_components/atglance`, endpoints `atglance/*`, custom panel `/atglance`, `<atglance-panel>`) cleanly migrated.
  - Automatic migration logic reads `.storage/vision_glass.config` if `.storage/atglance.config` is missing.
  - Clean separation, zero technical debt.

- **Approach 2: Superficial Rebranding (REJECTED)**
  - Kept internal domain as `vision_glass` and only changed display titles.
  - Rejected because it preserves confusing legacy names in file structures and HACS.

---

## 4. Technical Architecture & Modifications

### 4.1. Domain & Backend (`custom_components/atglance`)
- Directory renamed: `custom_components/vision_glass/` -> `custom_components/atglance/`.
- `const.py`:
  - `DOMAIN = "atglance"`
  - `PANEL_TITLE = "AtGlance"`
  - `PANEL_ICON = "mdi:view-dashboard-outline"`
  - `PANEL_URL = "atglance"`
  - `STORAGE_KEY = "atglance.config"`
- `config_manager.py`:
  - Storage file `.storage/atglance.config`.
  - Migration check: if `atglance.config` doesn't exist, check `.storage/vision_glass.config`, read data, and write to `atglance.config`.
- `__init__.py`:
  - Register custom panel: `frontend_url_path="atglance"`, `webcomponent_name="atglance-panel"`.
  - WebSocket endpoints:
    - `atglance/config/get`
    - `atglance/config/save`
    - `atglance/discovery/rooms`
    - `atglance/stats/history`
    - `atglance/default_dashboard/set`
- `manifest.json`:
  - `domain`: `"atglance"`
  - `name`: `"AtGlance Dashboard"`
  - `version`: `"1.0.0"`
  - `documentation`: `"https://github.com/adromir/ha-atglance-dashboard"`
  - `issue_tracker`: `"https://github.com/adromir/ha-atglance-dashboard/issues"`
- Translations (`translations/de.json`, `en.json`, `id.json`): Update title to `AtGlance Dashboard`.

### 4.2. Frontend (`custom_components/atglance/frontend/`)
- Rename `vision-glass-panel.js` -> `atglance-panel.js`.
- Register webcomponent: `customElements.define('atglance-panel', AtGlancePanel)`.
- Update all WebSocket commands from `vision_glass/*` to `atglance/*`.
- Default Dashboard routing:
  - Default panel target: `atglance`.
  - Update `window.history` / hash routing to `/atglance`.
  - Update `setAsDefaultDashboard` payload to `{ default_panel: 'atglance' }`.
- Update references in `settings-view.js`, `i18n.js`, `controls.js`, `modals.js`, `icons.js`.

### 4.3. Repository, HACS & Workflows
- Rename local workspace folder: `e:\homeassistant\ha-vision-glass-dashboard` -> `e:\homeassistant\ha-atglance-dashboard`.
- Rename GitHub repository: `adromir/ha-vision-glass-dashboard` -> `adromir/ha-atglance-dashboard`.
- Update git remote origin: `https://github.com/adromir/ha-atglance-dashboard.git`.
- `hacs.json`: Update name to `"AtGlance Dashboard"`.
- `README.md`: Update title, descriptions, and HACS install badge URLs.
- Release workflow `.github/workflows/release.yml`: Validate `custom_components/atglance/manifest.json`.
- Tag: `v1.0.0`.

### 4.4. Home Assistant System Migration
1. Remove deprecated `vision_glass` integration entry from Home Assistant via API / MCP.
2. Remove deprecated `ha-vision-glass-dashboard` repository from HACS.
3. Register `adromir/ha-atglance-dashboard` as custom repository in HACS (category `integration`).
4. Download `adromir/ha-atglance-dashboard`.
5. Restart Home Assistant core.
6. Verify `/atglance` loads with all migrated settings and default dashboard status intact.
