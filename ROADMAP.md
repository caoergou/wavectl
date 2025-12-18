# Roadmap

This roadmap outlines the development plan for `wavectl`.

## Phase 1: Core Interaction & Configuration Coverage

The goal of Phase 1 is to establish a robust interactive foundation and support the full breadth of WaveTerm configurations.

- [ ] **Project Skeleton & TUI Foundation:**
    - [ ] Set up project structure (Python/Typer/Rich or similar).
    - [ ] Implement the core TUI engine for navigation and menus.
    - [ ] Auto-detection of WaveTerm configuration paths.
- [ ] **Interactive Configuration Modules:**
    - [ ] **AI Module:** Interactive setup for API keys and model selection.
    - [ ] **SSH Module:** Wizard for adding/editing SSH connections.
    - [ ] **Theme Module:** Visual selector for themes and color schemes.
    - [ ] **Widget/Layout Module:** Configuration for terminal widgets.
- [ ] **Validation:** Real-time validation of user inputs (e.g., file paths, basic syntax).

## Phase 2: Data Management & Sync

The goal of Phase 2 is to ensure user configurations are safe, portable, and shareable.

- [ ] **Presets System:**
    - [ ] Save current configurations as named presets.
    - [ ] Quickly switch between presets (e.g., "Work", "Home", "Presentation").
- [ ] **Backup & Restore:**
    - [ ] Local backup of configuration files.
    - [ ] Restore from previous local backups.
- [ ] **Cloud Sync (GitHub):**
    - [ ] Integration with Git to version control configurations.
    - [ ] Automated push/pull to a user-specified private GitHub repository.

## Phase 3: Advanced Ecosystem

- [ ] **Plugin/Extension Manager:** Interface for managing WaveTerm extensions.
- [ ] **Community Hub:** (Potential) Browse and download themes/presets shared by the community.

## Versioning

We follow [Semantic Versioning](https://semver.org/).
