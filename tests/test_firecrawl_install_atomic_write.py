"""Static contract for firecrawl's install.ps1 ~/.claude.json write.

install.ps1 cannot be executed in CI (no PowerShell on the Linux/macOS
runners that run the main suite; see docs/WORKFLOW-public-private.md and the
windows-smoke workflow for the executed coverage). This test asserts the
source text contains the temp-then-move write pattern and the -Depth 100
serialisation depth needed to round-trip an existing ~/.claude.json.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_firecrawl_install_ps1_writes_mcp_config_atomically() -> None:
    text = (ROOT / "extensions/firecrawl/install.ps1").read_text(encoding="utf-8")

    assert "$TempConfigFile" in text
    assert "Move-Item -Path $TempConfigFile -Destination $McpConfigFile -Force" in text
    # The final Set-Content must target the temp file, not $McpConfigFile
    # directly, so a crash mid-write cannot leave it truncated.
    assert "Set-Content $TempConfigFile -Encoding UTF8" in text
    assert "Set-Content $McpConfigFile -Encoding UTF8" not in text


def test_firecrawl_install_ps1_uses_depth_100() -> None:
    text = (ROOT / "extensions/firecrawl/install.ps1").read_text(encoding="utf-8")

    assert "ConvertTo-Json -Depth 100" in text
    assert "ConvertTo-Json -Depth 10 " not in text
    assert "ConvertTo-Json -Depth 10\n" not in text
