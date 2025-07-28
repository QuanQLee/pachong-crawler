from __future__ import annotations

from .platforms.ecommerce import FakeStorePlatform
from .platforms.social import FakeSocialPlatform


def main() -> None:
    ecommerce = FakeStorePlatform()
    social = FakeSocialPlatform()

    print("E-commerce products:")
    for item in ecommerce.fetch_items():
        print(item)

    print("\nSocial trending posts:")
    for item in social.fetch_items():
        print(item)


if __name__ == "__main__":
    main()
