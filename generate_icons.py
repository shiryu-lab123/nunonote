"""
ぬのーと アイコン生成スクリプト
実行方法: このファイルと同じフォルダで PowerShell または コマンドプロンプトを開き
    python generate_icons.py
と入力してください。Pillow が必要です（pip install Pillow）
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# ===== 設定 =====
BG_COLOR = (160, 106, 53)       # #A06A35 ブラウン
TEXT_COLOR = (255, 255, 255)     # 白
SUB_COLOR  = (255, 255, 255, 184) # 半透明白

# Windows に標準でインストールされている日本語フォントを優先順に探す
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\YuGothB.ttc",        # Yu Gothic Bold
    r"C:\Windows\Fonts\YuGothM.ttc",        # Yu Gothic Medium
    r"C:\Windows\Fonts\yugothb.ttc",
    r"C:\Windows\Fonts\meiryo.ttc",         # Meiryo
    r"C:\Windows\Fonts\meiryob.ttc",        # Meiryo Bold
    r"C:\Windows\Fonts\msgothic.ttc",       # MS Gothic
    r"C:\Windows\Fonts\msmincho.ttc",       # MS Mincho
    r"C:\Windows\Fonts\BIZ-UDGothicR.ttc",
    r"C:\Windows\Fonts\BIZ-UDGothicB.ttc",
]

def find_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            print(f"  フォント: {path}")
            return path
    print("  警告: 日本語フォントが見つかりません。デフォルトフォントを使用します")
    return None

def make_icon(size, out_path):
    img = Image.new("RGBA", (size, size), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)
    font_path = find_font()

    # ===== 大きな「ぬ」=====
    main_font_size = int(size * 0.58)
    if font_path:
        font_main = ImageFont.truetype(font_path, main_font_size)
    else:
        font_main = ImageFont.load_default()

    char = "ぬ"
    bbox = draw.textbbox((0, 0), char, font=font_main)
    char_w = bbox[2] - bbox[0]
    char_h = bbox[3] - bbox[1]

    # 「のーと」サブテキスト
    sub_font_size = max(int(size * 0.12), 8)
    if font_path:
        font_sub = ImageFont.truetype(font_path, sub_font_size)
    else:
        font_sub = ImageFont.load_default()

    sub_text = "のーと"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_h = sub_bbox[3] - sub_bbox[1]

    gap = int(size * 0.03)
    total_h = char_h + gap + sub_h

    # 中央配置
    y_start = (size - total_h) // 2

    x_char = (size - char_w) // 2 - bbox[0]
    y_char = y_start - bbox[1]
    draw.text((x_char, y_char), char, font=font_main, fill=TEXT_COLOR)

    x_sub = (size - sub_w) // 2 - sub_bbox[0]
    y_sub = y_start + char_h + gap - sub_bbox[1]
    draw.text((x_sub, y_sub), sub_text, font=font_sub, fill=(255, 255, 255, 184))

    # 角丸マスク
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(size * 0.22)
    mask_draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
    img.putalpha(mask)

    # 白背景で合成（PNG保存時に透過なし）
    bg = Image.new("RGB", (size, size), BG_COLOR)
    bg.paste(img, mask=img.split()[3])
    bg.save(out_path, "PNG")
    print(f"  保存: {out_path}  ({size}x{size}px)")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    sizes = [
        (180, "icon.png"),
        (192, "icon-192.png"),
        (512, "icon-512.png"),
    ]

    print("アイコンを生成しています...\n")
    for size, filename in sizes:
        out = os.path.join(script_dir, filename)
        make_icon(size, out)

    print("\n✅ 完了！ icon.png / icon-192.png / icon-512.png を上書き保存しました。")
    print("   GitHubにプッシュすれば、スマホのホーム画面に反映されます。")
    input("\nEnterキーを押して終了...")
