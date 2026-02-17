# CHANGELOG

<!-- version list -->

## v1.2.2 (2026-02-17)

### Bug Fixes

- Skip diagnostics for template variables (unquoted names)
  ([`e247437`](https://github.com/jordannpenn/hx-requests-lsp/commit/e247437d715d53e0834e7ac31d05b16a40dfdcc4))

### Documentation

- Update VS Code extension publisher to jordanpenn
  ([`db46156`](https://github.com/jordannpenn/hx-requests-lsp/commit/db46156761321febc2c3a605344cb42759694275))


## v1.2.1 (2026-02-16)

### Bug Fixes

- Resolve base classes from any installed package
  ([`4ab803f`](https://github.com/jordannpenn/hx-requests-lsp/commit/4ab803f631a679ae9eec1467bb8a33156b19c839))


## v1.2.0 (2026-02-16)

### Documentation

- Improve Neovim configuration examples
  ([`5d4eb2c`](https://github.com/jordannpenn/hx-requests-lsp/commit/5d4eb2cd407156c55cb3a0e46e2d831a8d3a6930))

- Streamline README and move dev docs to CONTRIBUTING.md
  ([`276be88`](https://github.com/jordannpenn/hx-requests-lsp/commit/276be8872637fc2c8db1044f738bd0fb18cd6b93))

### Features

- Add clickable base class links in hover
  ([`5c8605a`](https://github.com/jordannpenn/hx-requests-lsp/commit/5c8605a3cbafb5ce5a2a0481ffed072fe7ad1587))


## v1.1.2 (2026-02-13)

### Bug Fixes

- Read version from package metadata instead of hardcoding
  ([`85b31cc`](https://github.com/jordannpenn/hx-requests-lsp/commit/85b31cc1f23f8c473e458b4a124c0e51a8feb2bc))


## v1.1.1 (2026-02-12)

### Bug Fixes

- Update README with new autocomplete features
  ([`1a92234`](https://github.com/jordannpenn/hx-requests-lsp/commit/1a92234b8e034b2a4955a9e1aa933862484170f5))


## v1.1.0 (2026-02-12)

### Bug Fixes

- **ci**: Use version comparison instead of git diff to detect releases
  ([`3644162`](https://github.com/jordannpenn/hx-requests-lsp/commit/364416268596221f88bbbe1e26e43715a1df21af))

### Continuous Integration

- Consolidate release workflow to handle PyPI publish and extension trigger
  ([`ad2f4e7`](https://github.com/jordannpenn/hx-requests-lsp/commit/ad2f4e7e5125503a563dadd343f38dbb99fd5d71))

### Features

- Prioritize current app's hx_requests in autocomplete suggestions
  ([`ae1ab8d`](https://github.com/jordannpenn/hx-requests-lsp/commit/ae1ab8d3c7f730e46e39e7e8decfe824e4d1f808))


## v1.0.1 (2026-02-12)

### Bug Fixes

- Improve autocomplete to work without quotes and with trailing code
  ([`9fe7b4f`](https://github.com/jordannpenn/hx-requests-lsp/commit/9fe7b4fab46a66d6487a156a9ad66efcf0885b42))

### Continuous Integration

- Rename workflow to match PyPI trusted publisher config
  ([`1ea84be`](https://github.com/jordannpenn/hx-requests-lsp/commit/1ea84be5c5d5c41b7ac5a93caa26cea03abdc001))

- Split release and publish workflows
  ([`dc5a85b`](https://github.com/jordannpenn/hx-requests-lsp/commit/dc5a85b7307f6fbdc0cfe53814799cbcb0847bac))

- Trigger extension rebuild on LSP release
  ([`5cb08e0`](https://github.com/jordannpenn/hx-requests-lsp/commit/5cb08e0d3871ace4dcccb3fd1b304d1f1c850f29))


## v1.0.0 (2026-02-11)

### Continuous Integration

- Add semantic-release for automatic versioning and publishing
  ([`71ec00b`](https://github.com/jordannpenn/hx-requests-lsp/commit/71ec00bb1c70f093426323ec8bd0141725f01f6f))


## v0.1.1 (2026-02-11)

### Bug Fixes

- Recognize classes inheriting from *Hx base classes and improve autocomplete context detection
  ([`fc91328`](https://github.com/jordannpenn/hx-requests-lsp/commit/fc91328b97c9ad23e54d66df51a64aeb948a62e5))


## v0.1.0 (2026-02-10)

- Initial Release
