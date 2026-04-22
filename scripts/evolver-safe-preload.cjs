'use strict';

const LOCAL_HOSTS = new Set(['localhost', '::1']);

function extractUrl(input) {
  if (!input) return null;
  if (typeof input === 'string') return input;
  if (typeof URL !== 'undefined' && input instanceof URL) return input.toString();
  if (typeof Request !== 'undefined' && input instanceof Request) return input.url;
  if (typeof input.url === 'string') return input.url;
  return null;
}

function isAllowedUrl(raw) {
  if (!raw) return true;
  let url;
  try {
    url = new URL(raw);
  } catch (_err) {
    return false;
  }

  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    return true;
  }

  return LOCAL_HOSTS.has(url.hostname) || url.hostname.startsWith('127.');
}

if (typeof globalThis.fetch === 'function') {
  const originalFetch = globalThis.fetch.bind(globalThis);
  globalThis.fetch = async function patchedFetch(input, init) {
    const raw = extractUrl(input);
    if (!isAllowedUrl(raw)) {
      return new Response(JSON.stringify({ ok: false, blocked: true, url: raw }), {
        status: 451,
        headers: { 'content-type': 'application/json' },
      });
    }
    return originalFetch(input, init);
  };
}
