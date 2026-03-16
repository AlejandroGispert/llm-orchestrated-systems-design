"""Minimal direct Gemini test using google-genai.

Run from the project root with the venv active:

    source .venv/bin/activate
    set -a && . .env && set +a
    python test_gemini.py
"""

import os

from google import genai


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not set in the environment.")

    client = genai.Client(api_key=api_key)

    print("Models that support generateContent:\n")
    available_models: list[str] = []
    for m in client.models.list():
        # API may expose either supported_generation_methods or supported_actions
        methods = getattr(m, "supported_generation_methods", []) or getattr(
            m, "supported_actions", []
        )
        if "generateContent" in methods:
            print(f"  - {m.name}")
            available_models.append(m.name)

    # Prefer a 2.0 flash model if available, otherwise first generateContent model.
    preferred = None
    for candidate in ("gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-001"):
        if candidate in available_models or f"models/{candidate}" in available_models:
            preferred = candidate
            break
    if preferred is None and available_models:
        preferred = available_models[0]

    if not preferred:
        print("\nNo models with generateContent found for this API key.")
        return

    print(f"\nTesting content generation with model: {preferred}\n")
    try:
        resp = client.models.generate_content(
            model=preferred,
            contents=[{"role": "user", "parts": [{"text": "Say hello in one short sentence."}]}],
        )
    except Exception as e:  # noqa: BLE001
        print(f"  ERROR calling {preferred}: {e!r}")
        return

    text = getattr(resp, "text", None)
    if text:
        print(f"  Response text: {text!r}")
    else:
        print(f"  Raw response object: {resp!r}")


if __name__ == "__main__":
    main()

