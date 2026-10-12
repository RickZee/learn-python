[Home](../../README.md) › [Projects](../README.md) › Networking

# Networking

URLs, addresses, and sockets. Most application code should use a client library. The standard library is enough to understand the pieces.

## Tools

- urllib.parse for URLs
- ipaddress for IP addresses
- socket or asyncio for a custom protocol
- httpx for HTTP

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Reject a URL with no host, and print the path of one that has a host.
3. Keep the change small enough to finish in one sitting.

## Where it sits

HTTP calls from an application belong in [services](../04-services/README.md).

**Next:** [Projects](../README.md)
