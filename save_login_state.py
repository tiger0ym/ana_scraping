from playwright.sync_api import sync_playwright
from config import ANA_ID, ANA_PASS
import time, sys

STATE_FILE = "storage_state.json"

with sync_playwright() as p:
    # 最初はheadful+slowで“人間っぽく”動かす
    browser = p.chromium.launch(headless=False, slow_mo=80)
    ctx = browser.new_context(
        locale="ja-JP",
        viewport={"width": 1280, "height": 900},
    )
    page = ctx.new_page()

    # 1) トップ→ログイン導線へ（実サイトの導線に合わせて調整）
    page.goto("https://www.ana.co.jp/ja/jp/")
    page.get_by_role("link", name=" ログイン").click()

    # 2) ログインフォーム入力（実際のname/idに置換）
    page.fill('input[name="member_no"]', ANA_ID)
    page.fill('input[name="member_password"]', ANA_PASS)
    
    page.wait_for_selector("#login")
    page.click("#login")

    # ここで手動対応しやすいよう20秒ほど待機（2FA/CAPTCHA等）
    print("手動でログイン操作を完了してください…20秒待ちます")
    time.sleep(20)

    # ログイン後の見出しやユーザ名などで“成功”を軽く確認してから保存するのが安全
    ctx.storage_state(path=STATE_FILE)
    print("✅ ログイン状態を保存しました:", STATE_FILE)
    # browser.close()
