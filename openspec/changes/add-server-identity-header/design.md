## Context

Hue is a Django-based web application with a middleware chain defined in `desktop/core/src/desktop/settings.py`. The project already uses `Django4MiddlewareAdapterMixin` as a base class for custom middleware and follows a pattern where middleware can conditionally unload itself via `exceptions.MiddlewareNotUsed` in `__init__` based on configuration.

Existing examples such as `CacheControlMiddleware` and `ContentSecurityPolicyMiddleware` demonstrate the pattern of reading configuration in `__init__` and modifying response headers in `process_response`. The `AuditLoggingMiddleware` shows how to retrieve client IP in a proxy environment, but no middleware currently injects server-side identity into responses.

The hostname is already obtained in other parts of the codebase (`desktop/log/api.py`) using `socket.gethostname()`, establishing a precedent for this approach.

See [proposal.md](proposal.md) for the motivation behind this change.

## Goals / Non-Goals

**Goals:**
- Provide an opt-in mechanism to inject a server identity header into every HTTP response.
- Allow operators to customize both the header name and value.
- Fall back to `socket.gethostname()` when no custom value is provided.
- Follow existing Hue middleware patterns and configuration conventions.
- Cover the middleware with unit tests mirroring the existing `middleware_test.py` style.

**Non-Goals:**
- No changes to existing logging or audit systems.
- No support for dynamic value resolution per-request (e.g., per-thread hostnames).
- No changes to load balancer or reverse proxy configuration.

## Decisions

### Decision: Implement as Django middleware rather than WSGI or proxy layer
**Rationale:** A Django middleware keeps the feature within the application codebase, making it configurable through Hue's existing `desktop.conf` system and manageable within the same deployment artifact. WSGI middleware would require changes at the server entry point; proxy-layer changes would be outside Hue's control.
**Alternative considered:** Nginx `add_header` — rejected because it requires per-deployment infrastructure changes and would not be present when accessing the app server directly.

### Decision: Use `socket.gethostname()` as the default value
**Rationale:** This is already used elsewhere in Hue (`log/api.py`), ensuring consistency. In Docker, the hostname can be set explicitly via `--hostname` or Docker Compose; in Kubernetes, it resolves to the pod name when the pod's hostname is configured accordingly.
**Alternative considered:** `socket.gethostbyname(socket.gethostname())` to expose IP instead of hostname — rejected because the user explicitly prefers hostname over IP, and IP can be less readable in containerized environments.

### Decision: Default the feature to disabled
**Rationale:** Exposing server identity in HTTP headers can leak internal infrastructure details to external clients. An opt-in model follows the principle of safe defaults and aligns with the security-conscious nature of enterprise deployments.

### Decision: Store configuration in `desktop.conf` rather than environment variables only
**Rationale:** Hue's configuration system already supports environment variable interpolation in `hue.ini`. Using `Config` objects allows the feature to be toggled via `hue.ini`, environment variables, or programmatic overrides, providing maximum deployment flexibility.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Information disclosure if enabled on public-facing instances | Default is disabled; documentation and help text clearly describe the security implication. Operators must explicitly opt in. |
| Hostname in Docker defaults to an opaque container ID | Operators can set `--hostname` or configure `server_identity_header_value` to a meaningful identifier (e.g., pod name via env var). |
| Additional middleware adds negligible per-request overhead | The middleware performs a single dictionary assignment on the response object. The value is resolved once at middleware initialization, not per request. |

## Migration Plan

No migration is required. The change is purely additive and backward-compatible:
1. Deploy the updated code.
2. Optionally add the configuration to `hue.ini` and restart Hue to enable the header.
3. To disable, remove or set `server_identity_header_enabled=false` and restart.

## Open Questions

None.
