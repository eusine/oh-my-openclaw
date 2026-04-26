# Visual Ralph

Visual Ralph is the Oh My OpenClaw import of upstream OMX's v0.15.0 visual UI workflow.

It is for frontend work where subjective description is not enough. A visual reference becomes the source of truth, Ralph implements against it, and `visual-verdict` plus screenshot evidence drives iteration.

## Flow

1. Inspect the target repo: framework, styling system, scripts, screenshot tooling, and reusable components.
2. Establish a reference:
   - generated mockup,
   - static image supplied by the user,
   - or live URL-derived baseline.
3. Stop for explicit user approval of that reference before implementation.
4. Implement through Ralph or a persistent executor lane.
5. Capture screenshots at the recorded viewport/state.
6. Run `visual-verdict` before the next edit.
7. Use pixel diff only as secondary debug evidence.
8. Encode the result into repo-native reusable tokens/components.

## Live URL baseline requirements

For URL-driven visual cloning or migration, preserve:

- source URL and permission/scope note,
- viewport(s), route/state, and seed/login assumptions,
- baseline screenshot path or capture command,
- visible-control interaction notes,
- exclusions such as auth, backend/API, personalized data, third-party widgets, or multi-page crawling.

## Approval boundary

Before approval, do not start implementation. The reference may be regenerated or adjusted.

After approval, the reference is the visual source of truth. Do not make major design pivots unless the user explicitly changes direction.

## Pass threshold

`visual-verdict` must score the final screenshot at **90+** unless a lower threshold is explicitly accepted for a documented reason.

The final artifact should include:

- approved reference path,
- screenshot command and viewport,
- final screenshot path,
- final verdict JSON,
- optional pixel diff/overlay,
- design token/component notes,
- build/lint/test evidence.
