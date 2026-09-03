## Purpose

Enables operators to identify individual Hue backend server instances in load-balanced deployments by injecting a configurable HTTP response header on every outgoing response.

## ADDED Requirements

### Requirement: Server identity header injection
When the server identity feature is enabled, the system SHALL include a server identity header in every HTTP response.

#### Scenario: Feature enabled
- **WHEN** the server identity feature is enabled via configuration
- **THEN** every HTTP response SHALL include the configured server identity header with the configured value

#### Scenario: Feature disabled
- **WHEN** the server identity feature is disabled via configuration
- **THEN** HTTP responses SHALL NOT include the server identity header

### Requirement: Configurable header name and value
The system SHALL support operator-defined header names and values through configuration.

#### Scenario: Custom header name
- **WHEN** a custom header name is configured
- **THEN** the system SHALL use that name in HTTP responses instead of the default

#### Scenario: Custom header value
- **WHEN** a custom header value is configured
- **THEN** the system SHALL use that value in HTTP responses

#### Scenario: Default value fallback
- **WHEN** no custom header value is configured
- **THEN** the system SHALL use the server's hostname as the header value

### Requirement: Safe default behavior
The system SHALL disable the server identity header by default to avoid unintended information disclosure.

#### Scenario: Default configuration
- **WHEN** no explicit configuration is provided
- **THEN** the server identity feature SHALL be disabled and no header SHALL be injected
