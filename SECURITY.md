# Security policy

## Baseline
This scaffold has no application authentication. It must remain private until integrated with the company's identity provider, server-side authorization checks, session/token policy, CSRF posture and audit requirements.

The default Compose port is bound to `127.0.0.1` only. Do not change it to a wildcard host bind unless an approved protected ingress and the application authorization controls are in place.

- Store secrets in the deployment secret manager, never `.env` in Git.
- Restrict CORS and trusted hosts in production.
- Terminate TLS at the approved ingress and set security headers there.
- Classify data before adding fields; redact PII and credentials from logs.
- Pin/lock dependencies and review automated updates.
- Report vulnerabilities privately to the internal security contact defined by the generated project's owner.

Supported releases are the current `main` branch and latest tagged release only.
