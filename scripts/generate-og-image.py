#!/usr/bin/env python3
"""
parkseongjin.me 의 OG(공유 카드) 기본 이미지를 생성합니다.

링크를 SNS/메신저에 공유할 때 뜨는 1200x630 미리보기 이미지입니다.
문구만 바꿔 재실행하면 됩니다 (아래 CONFIG 부분).

실행:
    PYTHONPATH="$KIROCREW_SCRATCH/pylibs" python3 scripts/generate-og-image.py

의존성:
    Pillow (프로젝트 의존성 아님 — 스크래치에만 설치해서 쓰세요)
        python3 -m pip install --target "$KIROCREW_SCRATCH/pylibs" Pillow

출력:
    src/assets/og-default.png  (1200x630 PNG)

주의:
    OG 이미지는 SVG가 안 됩니다 (대부분 플랫폼이 래스터만 지원). 반드시 PNG.
    색은 src/styles/global.css 의 다크 테마 토큰과 맞춰져 있습니다.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── CONFIG ─────────────────────────────────────────────────────────────
# 문구를 바꾸려면 여기만 고치면 됩니다.
PROMPT = "parkseongjin.me:~$"
TITLE = "만들면서 배우는 기록"
SUBTITLE = "# 배운 것, 삽질한 것, 만든 것을 하나씩 적어둡니다."

# 다크 테마 토큰 (src/styles/global.css 의 html[data-theme='dark'] 와 일치)
BG = (12, 14, 12)          # #0c0e0c  배경
ACCENT = (74, 222, 128)    # #4ade80  액센트 (초록)
INK = (215, 224, 212)      # #d7e0d4  본문
MUTED = (99, 112, 95)      # #63705f  흐린 텍스트
PANEL = (20, 23, 20)       # #141714  패널

# 폰트 (macOS 시스템 폰트)
FONT_KR = "/System/Library/Fonts/AppleSDGothicNeo.ttc"   # index 0 = regular, 1 = bold
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"            # index 0 = regular

W, H = 1200, 630
# ───────────────────────────────────────────────────────────────────────

OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "og-default.png"


def load(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 점선 테두리 — 사이트의 '파일 프리뷰' 모티프.
    margin = 48
    box = (margin, margin, W - margin, H - margin)
    dash, gap = 14, 10
    x0, y0, x1, y1 = box
    def dashed_h(y):
        x = x0
        while x < x1:
            d.line([(x, y), (min(x + dash, x1), y)], fill=MUTED, width=2)
            x += dash + gap
    def dashed_v(x):
        y = y0
        while y < y1:
            d.line([(x, y), (x, min(y + dash, y1))], fill=MUTED, width=2)
            y += dash + gap
    dashed_h(y0); dashed_h(y1); dashed_v(x0); dashed_v(x1)

    # 좌상단 틸데(~) 마크 — 파비콘과 동일.
    tilde_font = load(FONT_MONO, 120)
    pad = margin + 44
    d.text((pad, pad - 24), "~", font=tilde_font, fill=ACCENT)

    # 프롬프트 (모노)
    prompt_font = load(FONT_MONO, 30)
    prompt_y = pad + 150
    d.text((pad, prompt_y), PROMPT, font=prompt_font, fill=MUTED)

    # 제목 (한글 bold)
    title_font = load(FONT_KR, 92, index=1)
    title_y = prompt_y + 60
    d.text((pad, title_y), TITLE, font=title_font, fill=INK)

    # 부제 — 한글이 들어가므로 한글 폰트로 렌더합니다.
    # (Menlo 같은 모노 폰트에는 한글 글리프가 없어 폴백되면 폭이 어긋납니다.)
    sub_font = load(FONT_KR, 34)
    sub_y = title_y + 138
    d.text((pad, sub_y), SUBTITLE, font=sub_font, fill=ACCENT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
