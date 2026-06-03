import re


VIDEO_PATTERN = re.compile(r"!\[video(?::(?P<label>[^\]]+))?\]\((?P<src>[^)\s]+)(?:\s+\"(?P<title>[^\"]+)\")?\)")


def expand_media_shortcodes(markdown_text: str) -> str:
    def replace_video(match: re.Match[str]) -> str:
        src = match.group("src")
        title = match.group("title") or match.group("label") or ""
        caption = f"<figcaption>{title}</figcaption>" if title else ""
        return (
            '<figure class="media-embed video-embed">'
            f'<video controls preload="metadata" src="{src}"></video>'
            f"{caption}"
            "</figure>"
        )

    lines: list[str] = []
    in_fence = False

    for line in markdown_text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            lines.append(line)
            continue

        lines.append(line if in_fence else VIDEO_PATTERN.sub(replace_video, line))

    return "\n".join(lines)
