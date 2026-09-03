## Why

In load-balanced deployments (e.g., Docker, Kubernetes), multiple Hue server instances sit behind a reverse proxy or load balancer. When debugging issues or analyzing logs, operators need to identify which specific backend server handled a given request. Currently, Hue provides no server-side identifier in HTTP responses, making it impossible to distinguish backend instances from the client perspective.

## What Changes

- Add a new Django middleware `ServerIdentityMiddleware` that injects a configurable HTTP response header identifying the server.
- Introduce three new configuration options in `desktop.conf`:
  - `server_identity_header_enabled` — toggle the feature (default: `false`)
  - `server_identity_header_name` — custom header name (default: `X-Hue-Server-Name`)
  - `server_identity_header_value` — custom value; falls back to `socket.gethostname()` when empty
- Register the middleware in `desktop.settings.MIDDLEWARE`.
- Add unit tests in `middleware_test.py` covering enabled/disabled states and custom header values.

## Capabilities

### New Capabilities
- `server-identity`: HTTP response server identity header injection for backend traceability in load-balanced deployments.

### Modified Capabilities
- None

## Impact

- **Code**: `desktop/core/src/desktop/middleware.py`, `desktop/core/src/desktop/conf.py`, `desktop/core/src/desktop/settings.py`, `desktop/core/src/desktop/middleware_test.py`
- **Behavior**: No change by default (feature is opt-in). When enabled, every HTTP response includes an additional header.
- **Compatibility**: Fully backward-compatible; default is disabled.
