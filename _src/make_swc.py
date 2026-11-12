"""SWT版 ver2.3 の index.html から SWC版を作る（原稿_メンテナンス事務局_SWC_261112.docx の文言に合わせる）
使い方: python3 make_swc.py <SWT ver2.3 のフォルダ> <出力フォルダ>
"""
import sys, pathlib, shutil
from PIL import Image, ImageDraw, ImageFont

src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
(out / 'images').mkdir(parents=True, exist_ok=True)
t = (src / 'index.html').read_text(encoding='utf-8')

def rep(old, new, n=1):
    global t
    c = t.count(old)
    if c != n:
        raise SystemExit(f'置換数が違う: {old[:50]!r} {c}件（期待 {n}）')
    t = t.replace(old, new)

# BUILD_TAG
rep('<!-- BUILD_TAG: swt2026_maintenance_ver2.3 / 2026-11-12 -->',
    '<!-- BUILD_TAG: swc2026_maintenance_ver1.0 / 2026-11-12 -->')

# チーム名
rep('サイエンスウェブ株式会社 SWT</title>', 'サイエンスウェブ株式会社 SWC</title>')
rep('content="サイエンスウェブ株式会社 SWT"', 'content="サイエンスウェブ株式会社 SWC"')

# URL・メールアドレス
rep('https://science-web.tokyo/maintenance/', 'https://science-web.co.jp/maintenance/', 4)
rep('maintenance@science-web.tokyo', 'maintenance@science-web.co.jp', 10)

# 原稿の文言（SWT は「システム環境」、SWC は「ホームページ環境」）
rep('システム環境の安定運用を支える', 'ホームページ環境の安定運用を支える')
rep('システム環境のことでお困りのことがありましたら', 'ホームページ環境のことで<span class="nobr">お困りのことがありましたら</span>')

# 表記：原稿どおり、ファーストビューと01は「サーバー」、02〜04は「サーバ」
rep('<title>メンテナンス事務局｜サーバ・ドメイン・メールの管理',
    '<title>メンテナンス事務局｜サーバー・ドメイン・メールの管理')
rep('content="メンテナンス事務局が、サーバ・ドメイン・メールの管理をまるごとサポートします。サーバの保守管理、メールサーバの管理、',
    'content="メンテナンス事務局が、サーバー・ドメイン・メールの管理をまるごとサポートします。サーバーの保守管理、メールサーバーの管理、')
rep('content="メンテナンス事務局｜サーバ・ドメイン・メールの管理をまるごとサポート">',
    'content="メンテナンス事務局｜サーバー・ドメイン・メールの管理をまるごとサポート">')
rep('安心・安全に使い続けるために。サーバ・ドメイン・メールの管理をまるごとサポートします。">',
    '安心・安全に使い続けるために。サーバー・ドメイン・メールの管理をまるごとサポートします。">')
rep('<span class="mt-line">サーバとメールを</span>', '<span class="mt-line">サーバーとメールを</span>')
# スマホ幅で「た」だけが折り返さないよう、「・」の後ろで折り返す
rep('<li>サーバの調子が悪い・障害が発生した</li>', '<li>サーバーの調子が悪い・<span class="nobr">障害が発生した</span></li>')
rep('<br>サーバ・ドメイン・メールに関することをまとめてお任せください。',
    '<br>サーバー・ドメイン・メールに関することをまとめてお任せください。')
rep('<h3>サーバの保守管理</h3>', '<h3>サーバーの保守管理</h3>')
rep('<h3>メールサーバの管理</h3>', '<h3>メールサーバーの管理</h3>')

rep('文字を少し小さく（SWT ver1.0） */', '文字を少し小さく */')

# 更新日（原稿は空欄。公開日で入れる）
rep('<time datetime="2026-11-11">2026年11月11日</time>', '<time datetime="2026-11-16">2026年11月16日</time>')

for w in ('SWT', 'science-web.tokyo', 'システム環境', 'swt2026'):
    if w in t:
        raise SystemExit(f'SWT の語が残っている: {w} {t.count(w)}件')

(out / 'index.html').write_text(t, encoding='utf-8')
shutil.copy(src / 'images' / 'swc-logo.png', out / 'images' / 'swc-logo.png')

# メールアドレスの画像（SWO・SWT と同じ作り）
NAVY = '#0F62B4'
txt = 'maintenance@science-web.co.jp'
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 56)
W, H = 1040, 96
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
bb = d.textbbox((0, 0), txt, font=font)
assert bb[2] - bb[0] < W - 20, bb
d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=font, fill=NAVY)
d.line([(W - (bb[2] - bb[0])) / 2, H - 6, (W + (bb[2] - bb[0])) / 2, H - 6], fill=NAVY, width=3)
im.save(out / 'images' / 'mail-maintenance.png', optimize=True)
print('ok', len(t))
