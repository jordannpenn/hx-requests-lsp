# CHANGELOG

<!-- version list -->

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
