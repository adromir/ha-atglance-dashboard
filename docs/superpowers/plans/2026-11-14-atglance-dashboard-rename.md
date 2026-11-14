# AtGlance Dashboard Rebranding & Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the Vision Glass Dashboard to AtGlance Dashboard (v1.0.0) across GitHub, the local workspace, the Python backend (`custom_components/atglance`), the frontend custom panel (`/atglance`), HACS, and Home Assistant, preserving existing user configuration via automatic migration.

**Architecture:** Python custom component with async Storage persistence (`atglance.config`), native Area/Device registry discovery, Recorder statistics downsampling, and custom panel registration (`/atglance` -> `<atglance-panel>`). On initial load, a migration adapter copies `.storage/vision_glass.config` into `.storage/atglance.config` if not already present.

**Tech Stack:** Python 3.12 (Home Assistant Core 2024.7+), Vanilla JavaScript ES modules (Lit-free webcomponents), HACS integration format, GitHub REST API, Git.

**Spec:** [docs/superpowers/specs/2026-11-14-atglance-dashboard-rename-design.md](file:///e:/homeassistant/ha-vision-glass-dashboard/docs/superpowers/specs/2026-11-14-atglance-dashboard-rename-design.md)

## Global Constraints
- Target version is `1.0.0` (reset for the new identity).
- Repository name is `ha-atglance-dashboard`.
- Integration domain is `atglance`.
- Panel URL is `/atglance`, webcomponent is `<atglance-panel>`.
- Default dashboard setting target is `default_panel: 'atglance'`.
- Configuration storage file is `.storage/atglance.config`.
- Trilingual localization (`de`, `en`, `id`) must be preserved.

## Review Focus
1. **Zero configuration data loss**: If `.storage/atglance.config` does not exist, `.storage/vision_glass.config` must be parsed and migrated automatically so room cards, custom badges, and dock preferences are preserved.
2. **Default panel setting**: Setting the default landing page must write `default_panel: 'atglance'` to system data and user profile, and navigating to `/` or `/atglance` must open the dashboard without redirect loops.
3. **WebSocket command consistency**: All frontend commands (`atglance/config/get`, `atglance/config/save`, `atglance/discovery/rooms`, `atglance/stats/history`, `atglance/default_dashboard/set`) must match the backend command decorators in `__init__.py`.
4. **HACS metadata compatibility**: `hacs.json` and `manifest.json` must reference the new repository URL, name, and domain so HACS can download and validate updates.
5. **Git & remote integrity**: GitHub repository rename and git remote update must succeed with tags pushed cleanly.

---

### Task 1: GitHub Repository & Git Remote Rename

**Files:**
- Modify: `.git/config` (remote origin URL)

- [ ] **Step 1: Rename GitHub repository via REST API**
  Rename `adromir/ha-vision-glass-dashboard` to `adromir/ha-atglance-dashboard` using `PATCH https://api.github.com/repos/adromir/ha-vision-glass-dashboard`.
  Verify response returns status 200 with new full name `adromir/ha-atglance-dashboard`.

- [ ] **Step 2: Update local git remote origin**
  Execute `git remote set-url origin https://github.com/adromir/ha-atglance-dashboard.git`.
  Verify with `git remote -v`.

---

### Task 2: Local Directory & Documentation

**Files:**
- Rename directory: `e:\homeassistant\ha-vision-glass-dashboard` -> `e:\homeassistant\ha-atglance-dashboard`
- Modify: `hacs.json`
- Modify: `.github/workflows/release.yml`
- Modify: `README.md`

- [ ] **Step 1: Rename workspace folder**
  Move `e:\homeassistant\ha-vision-glass-dashboard` to `e:\homeassistant\ha-atglance-dashboard`.

- [ ] **Step 2: Update `hacs.json`**
  Update `"name": "AtGlance Dashboard"`.

- [ ] **Step 3: Update `.github/workflows/release.yml`**
  Update paths validating `custom_components/atglance/manifest.json`.

- [ ] **Step 4: Update `README.md`**
  Update title to `# 👁️ AtGlance Dashboard for Home Assistant`, update HACS badges and URLs to `adromir/ha-atglance-dashboard`, and document `/atglance`.

---

### Task 3: Backend Python Integration (`custom_components/atglance`)

**Files:**
- Rename folder: `custom_components/vision_glass` -> `custom_components/atglance`
- Modify: `custom_components/atglance/const.py`
- Modify: `custom_components/atglance/manifest.json`
- Modify: `custom_components/atglance/config_manager.py`
- Modify: `custom_components/atglance/__init__.py`
- Modify: `custom_components/atglance/config_flow.py`
- Modify: `custom_components/atglance/translations/*.json`

- [ ] **Step 1: Rename component directory**
  Move `custom_components/vision_glass` to `custom_components/atglance`.

- [ ] **Step 2: Update `const.py`**
  Set `DOMAIN = "atglance"`, `PANEL_TITLE = "AtGlance"`, `PANEL_URL = "atglance"`, `STORAGE_KEY = "atglance.config"`, `LEGACY_STORAGE_KEY = "vision_glass.config"`.

- [ ] **Step 3: Update `manifest.json`**
  Set `"domain": "atglance"`, `"name": "AtGlance Dashboard"`, `"version": "1.0.0"`, `"documentation": "https://github.com/adromir/ha-atglance-dashboard"`.

- [ ] **Step 4: Implement automatic migration in `config_manager.py`**
  When loading config: if `atglance.config` is missing, check if `vision_glass.config` exists. If so, copy contents and save to `atglance.config`.

- [ ] **Step 5: Update `__init__.py` and WebSocket endpoints**
  Update custom panel registration to `frontend_url_path="atglance"` and `webcomponent_name="atglance-panel"`.
  Update WebSocket commands to `atglance/config/get`, `atglance/config/save`, `atglance/discovery/rooms`, `atglance/stats/history`, `atglance/default_dashboard/set`.

- [ ] **Step 6: Update translations and config_flow**
  Update `translations/de.json`, `en.json`, `id.json` and `config_flow.py` domain references.

- [ ] **Step 7: Run Python compileall check**
  Execute `python -m compileall -q custom_components/atglance` to ensure no syntax errors exist.

---

### Task 4: Frontend Rebranding & Default Dashboard Routing

**Files:**
- Rename: `custom_components/atglance/frontend/vision-glass-panel.js` -> `atglance-panel.js`
- Modify: `custom_components/atglance/frontend/atglance-panel.js`
- Modify: `custom_components/atglance/frontend/settings-view.js`
- Modify: `custom_components/atglance/frontend/i18n.js`

- [ ] **Step 1: Rename panel entry script**
  Rename `vision-glass-panel.js` to `atglance-panel.js`.

- [ ] **Step 2: Update Webcomponent definition in `atglance-panel.js`**
  Register `customElements.define('atglance-panel', AtGlancePanel)`.
  Update hash/url routing listeners to match `/atglance`.
  Update all WebSocket calls to `atglance/*`.

- [ ] **Step 3: Update Default Dashboard helper**
  Ensure clicking "Als Standard-Dashboard aktualisieren" sets `default_panel: 'atglance'`.
  Update `settings-view.js` WebSocket calls to `atglance/*`.

- [ ] **Step 4: Update `i18n.js` branding strings**
  Update titles, descriptions, and auto-localized names to AtGlance Dashboard across `de`, `en`, and `id`.

---

### Task 5: Git Commit, Tag v1.0.0 & Release

**Files:**
- Git repository `ha-atglance-dashboard`

- [ ] **Step 1: Stage and commit all changes**
  Commit message: `feat(v1.0.0): rebrand Vision Glass to AtGlance Dashboard with seamless config migration`.

- [ ] **Step 2: Tag `v1.0.0`**
  Execute `git tag v1.0.0`.

- [ ] **Step 3: Push main and tag to GitHub**
  Execute `git push origin main` and `git push origin v1.0.0`.

---

### Task 6: Home Assistant Migration & Verification

- [ ] **Step 1: Remove old `vision_glass` from HACS**
  Call `ha_manage_hacs(action="remove", repository_id="1453888825")`.

- [ ] **Step 2: Add `adromir/ha-atglance-dashboard` to HACS**
  Call `ha_manage_hacs(action="add_repository", repository="adromir/ha-atglance-dashboard", category="integration")`.

- [ ] **Step 3: Download `adromir/ha-atglance-dashboard`**
  Call `ha_manage_hacs(action="download", repository_id=<new_id>)`.

- [ ] **Step 4: Restart Home Assistant**
  Trigger Home Assistant restart via service `homeassistant.restart`.

- [ ] **Step 5: Verify migration and Default Dashboard**
  Verify `/atglance` is registered, active, and retains the user's rooms and configurations.
