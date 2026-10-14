from mitmproxy import http


class CloudflareBypass:
    def request(self, flow: http.HTTPFlow):

        # Strip headers that expose a proxy or scanner in the path.
        headers_to_remove = [
            "x-forwarded-for",
            "via",
            "x-bluecoat-via",
            "x-forwarded-host",
            "x-forwarded-proto",
        ]
        for h in headers_to_remove:
            if h in flow.request.headers:
                del flow.request.headers[h]

        # Set headers that match a real Chrome browser.
        flow.request.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/132.0.0.0 Safari/537.36"
        )
        flow.request.headers["Accept"] = (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        )
        flow.request.headers["Accept-Language"] = "en-US,en;q=0.9"
        flow.request.headers["Accept-Encoding"] = "gzip, deflate, br"
        flow.request.headers["Connection"] = "keep-alive"

        
        flow.request.headers["sec-ch-ua"] = (
            '"Chromium";v="132", "Google Chrome";v="132", '
            '"Not_A Brand";v="99"'
        )
        flow.request.headers["sec-ch-ua-mobile"] = "?0"
        flow.request.headers["sec-ch-ua-platform"] = '"Windows"'


addons = [CloudflareBypass()]
