# Burp Cloudflare Header Sanitizer

A small [mitmproxy](https://mitmproxy.org/) addon that sits downstream of Burp Suite and rewrites every outgoing request to look like a real Chrome browser. It strips proxy and scanner artifacts and sets a consistent browser header set, so Cloudflare's header-based blocking stops dropping your traffic during an authorized test.

> **Scope:** For targets you own or are explicitly authorized to test. This gets your authorized traffic through to the application behind the WAF. Only point it at targets you have permission to assess.

Full write-up, including why it works and where it does not: [LINK TO POST]

## What it does

- Strips `Via`, `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`, and `X-BlueCoat-Via`.
- Sets a Chrome `User-Agent`, matching `sec-ch-ua` client hints, and the usual `Accept-*` headers.

## What it does not do

Header rewriting does not beat TLS fingerprinting (JA3/JA4), JavaScript or managed challenges, or IP reputation. If you are still blocked after this, you are fighting one of those, not a header. The write-up covers the details.

## Requirements

- Burp Suite
- Python3
- mitmproxy

## Quickstart

1. Start Burp with its proxy listener on `127.0.0.1:8080`.
2. Start mitmproxy with the addon, upstream of the target:
```bash
   mitmdump -s cloudflare_bypass.py --listen-port 8082 --ssl-insecure
```
3. In Burp, add an upstream proxy (**Settings > Network > Connections > Upstream Proxy Servers**): destination `*`, host `127.0.0.1`, port `8082`.

Now use Burp normally. Every request is sanitized on the way out.

## Keeping it current

The `User-Agent` and `sec-ch-ua` values name a specific Chrome version. Keep them matched to each other, and bump them to a current Chrome release now and then, or the mismatch becomes its own tell.

## License

MIT. See [LICENSE](LICENSE).
