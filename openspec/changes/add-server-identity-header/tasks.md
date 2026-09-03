## 1. Configuration

- [x] 1.1 Add `SERVER_IDENTITY_HEADER_ENABLED` Config to `desktop/core/src/desktop/conf.py`
- [x] 1.2 Add `SERVER_IDENTITY_HEADER_NAME` Config to `desktop/core/src/desktop/conf.py`
- [x] 1.3 Add `SERVER_IDENTITY_HEADER_VALUE` Config to `desktop/core/src/desktop/conf.py`

## 2. Middleware Implementation

- [x] 2.1 Create `ServerIdentityMiddleware` class in `desktop/core/src/desktop/middleware.py`
- [x] 2.2 Implement conditional unload via `MiddlewareNotUsed` when disabled
- [x] 2.3 Implement `process_response` to inject the configured header

## 3. Middleware Registration

- [x] 3.1 Append `desktop.middleware.ServerIdentityMiddleware` to `MIDDLEWARE` in `desktop/core/src/desktop/settings.py`

## 4. Testing

- [x] 4.1 Add test for enabled middleware injecting default header with hostname
- [x] 4.2 Add test for disabled middleware raising `MiddlewareNotUsed`
- [x] 4.3 Add test for custom header name and value
- [x] 4.4 Run existing middleware tests to verify no regressions
