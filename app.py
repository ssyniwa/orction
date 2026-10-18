import streamlit as str_lit
import random

# ==========================================
# ページ基本設定
# ==========================================
str_lit.set_page_config(
    page_title="レリック・オークション：禁忌のセリ市",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（ダークファンタジー＆サイバーパンク風）
str_lit.markdown("""
<style>
    .stApp {
        background-color: #0d0f18;
        color: #e0e6ed;
    }
    .stButton>button {
        background-color: #1a233a;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        border-radius: 4px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00f0ff;
        color: #0d0f18;
        border: 1px solid #00f0ff;
    }
    .log-box {
        background-color: #141824;
        border-left: 3px solid #00f0ff;
        padding: 10px;
        border-radius: 4px;
        font-family: monospace;
        height: 250px;
        overflow-y: auto;
    }
    .item-card {
        background-color: #161b2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# マスターデータ定義（15種類の出品アイテム）
# ==========================================
MASTER_ITEMS = [
    {"id": "item_01", "name": "魔導サイバーコア", "category": "サイバーファンタジー", "apparent_value": 300, "true_value": 800, "is_cursed": False, "image_url": "https://picsum.photos/seed/cybercore/400/300", "description": "古代の精霊結晶と量子プロセッサが融合した未知のジェネレータ。"},
    {"id": "item_02", "name": "偽りの聖剣アロンダイト", "category": "ファンタジー武器", "apparent_value": 600, "true_value": 50, "is_cursed": False, "image_url": "https://picsum.photos/seed/fake_sword/400/300", "description": "神々しい輝きを放つが、実は精巧に作られた鍍金メッキのレプリカ。"},
    {"id": "item_03", "name": "呪われたニューラル・バイザー", "category": "不法サイバーパーツ", "apparent_value": 450, "true_value": 100, "is_cursed": True, "image_url": "https://picsum.photos/seed/cursed_visor/400/300", "description": "圧倒的な処理能力を誇るが、装着者の精神を侵食するバグが潜む。"},
    {"id": "item_04", "name": "竜血の錬金薬瓶", "category": "魔法遺物", "apparent_value": 200, "true_value": 700, "is_cursed": False, "image_url": "https://picsum.photos/seed/dragon_potion/400/300", "description": "ドロリとした怪しい液体。伝説の古龍の血だと証言されている。"},
    {"id": "item_05", "name": "錆びついたAIメモリ端末", "category": "サイバー遺物", "apparent_value": 100, "true_value": 1200, "is_cursed": False, "image_url": "https://picsum.photos/seed/rusty_ai/400/300", "description": "一見ただのジャンク品。だが内部には旧時代の暗号通貨キーが眠る。"},
    {"id": "item_06", "name": "死霊術師のクロノグラフ", "category": "呪物", "apparent_value": 500, "true_value": 900, "is_cursed": True, "image_url": "https://picsum.photos/seed/necromancer_watch/400/300", "description": "針が逆回転する怪しい懐中時計。強力な時間魔術の触媒。"},
    {"id": "item_07", "name": "星詠みの水晶ドローン", "category": "サイバーファンタジー", "apparent_value": 400, "true_value": 650, "is_cursed": False, "image_url": "https://picsum.photos/seed/crystal_drone/400/300", "description": "未来予測AIと占星術アルゴリズムが同居した浮遊観測デバイス。"},
    {"id": "item_08", "name": "ブラッド・エッジブレード", "category": "ファンタジー武器", "apparent_value": 700, "true_value": 950, "is_cursed": True, "image_url": "https://picsum.photos/seed/blood_edge/400/300", "description": "持ち主の闘気を吸い取って切れ味を増す呪われた魔剣。"},
    {"id": "item_09", "name": "エーテル・チャージャー", "category": "魔法遺物", "apparent_value": 350, "true_value": 400, "is_cursed": False, "image_url": "https://picsum.photos/seed/ether_charger/400/300", "description": "魔力を無限に再充填できるとされる魔導バッテリーの試作品。"},
    {"id": "item_10", "name": "次元回廊のパスカード", "category": "サイバー遺物", "apparent_value": 800, "true_value": 1500, "is_cursed": False, "image_url": "https://picsum.photos/seed/dimension_pass/400/300", "description": "裏社会のネットワークの最深層へアクセスできるブラックパス。"},
    {"id": "item_11", "name": "模造エリクサーの空瓶", "category": "魔法遺物", "apparent_value": 150, "true_value": 20, "is_cursed": False, "image_url": "https://picsum.photos/seed/empty_elixir/400/300", "description": "かつて不老不死の薬が入っていたとされる、ただのガラスの空容器。"},
    {"id": "item_12", "name": "ゴースト・インプラント", "category": "不法サイバーパーツ", "apparent_value": 550, "true_value": 1100, "is_cursed": True, "image_url": "https://picsum.photos/seed/ghost_implant/400/300", "description": "人格データを書き換える違法チップ。前の持ち主の意識が残る噂がある。"},
    {"id": "item_13", "name": "タイタンの巨腕ガントレット", "category": "ファンタジー武器", "apparent_value": 650, "true_value": 750, "is_cursed": False, "image_url": "https://picsum.photos/seed/titan_gauntlet/400/300", "description": "圧倒的な怪力を得る代わりに、装着者の機動力を奪う重量級防具。"},
    {"id": "item_14", "name": "キメラの遺伝子サンプル", "category": "サイバーファンタジー", "apparent_value": 500, "true_value": 850, "is_cursed": True, "image_url": "https://picsum.photos/seed/chimera_dna/400/300", "description": "竜の遺伝子とナマシンセクトを掛け合わせた危険な培養カプセル。"},
    {"id": "item_15", "name": "黄昏の懐中鏡", "category": "呪物", "apparent_value": 300, "true_value": 600, "is_cursed": True, "image_url": "https://picsum.photos/seed/twilight_mirror/400/300", "description": "覗き込むと、自分自身の死に様が映し出されるという不吉な手鏡。"}
]

RIVALS = [
    {"name": "貴族オルガ", "type": "堅実派", "budget": 1200, "favorite": "ファンタジー武器", "aggressiveness": 0.4},
    {"name": "ハッカー・ゼロ", "type": "撹乱派", "budget": 1000, "favorite": "サイバー遺物", "aggressiveness": 0.7},
    {"name": "コレクター・バルト", "type": "執着派", "budget": 1800, "favorite": "魔法遺物", "aggressiveness": 0.8}
]

# ==========================================
# セッション状態の初期化
# ==========================================
if "initialized" not in str_lit.session_state:
    str_lit.session_state.initialized = True
    str_lit.session_state.player_money = 1200  # 初期所持金（万G）
    str_lit.session_state.appraisal_tickets = 3  # 初期鑑定チケット
    str_lit.session_state.day = 1
    str_lit.session_state.max_days = 5
    str_lit.session_state.items_per_day = 3
    str_lit.session_state.current_item_index = 0
    str_lit.session_state.inventory = []  # 所持アイテム
    str_lit.session_state.museum = []  # ミュージアム永久保存アイテム
    str_lit.session_state.appraised_items = {}
    str_lit.session_state.game_over = False

    str_lit.session_state.auction_active = False
    str_lit.session_state.current_price = 0
    str_lit.session_state.highest_bidder = None
    str_lit.session_state.auction_logs = []
    str_lit.session_state.daily_catalog = random.sample(MASTER_ITEMS, str_lit.session_state.items_per_day)

# ==========================================
# ロジック関数
# ==========================================
def start_next_item_auction():
    item = str_lit.session_state.daily_catalog[str_lit.session_state.current_item_index]
    str_lit.session_state.current_price = int(item["apparent_value"] * 0.5)
    str_lit.session_state.highest_bidder = "主催者"
    str_lit.session_state.auction_logs = [f"【競売開始】『{item['name']}』が出品されました！ 初期価格: {str_lit.session_state.current_price}万G"]
    str_lit.session_state.auction_active = True

def process_rival_bids():
    item = str_lit.session_state.daily_catalog[str_lit.session_state.current_item_index]
    current_p = str_lit.session_state.current_price

    bidders = []
    for rival in RIVALS:
        if rival["budget"] < current_p + 20:
            continue
        should_bid = False
        interest_mult = 1.3 if rival["favorite"] in item["category"] else 1.0
        max_bid_limit = item["apparent_value"] * interest_mult * rival["aggressiveness"]

        if rival["type"] == "堅実派" and current_p < item["apparent_value"] * 0.9:
            should_bid = random.random() < 0.6
        elif rival["type"] == "撹乱派":
            should_bid = random.random() < rival["aggressiveness"]
        elif rival["type"] == "執着派" and current_p < max_bid_limit:
            should_bid = random.random() < 0.7

        if should_bid:
            bid_raise = random.choice([20, 40, 60])
            bidders.append((rival, current_p + bid_raise))

    if bidders:
        selected_rival, new_price = max(bidders, key=lambda x: x[1])
        str_lit.session_state.current_price = new_price
        str_lit.session_state.highest_bidder = selected_rival["name"]
        str_lit.session_state.auction_logs.append(f"⚡ {selected_rival['name']} が {new_price}万G に値上げしました！")
        return True
    return False

def finalize_auction(winner, price, item):
    str_lit.session_state.auction_active = False
    if winner == "あなた":
        str_lit.session_state.player_money -= price
        str_lit.session_state.inventory.append(item)
        str_lit.toast(f"🎉 {item['name']} を {price}万G で落札しました！", icon="🎉")
    else:
        str_lit.toast(f"❌ {winner} に {price}万G で競り落とされました...", icon="💸")

    str_lit.session_state.current_item_index += 1
    if str_lit.session_state.current_item_index >= len(str_lit.session_state.daily_catalog):
        str_lit.session_state.day += 1
        str_lit.session_state.current_item_index = 0
        if str_lit.session_state.day > str_lit.session_state.max_days:
            str_lit.session_state.game_over = True
        else:
            str_lit.session_state.daily_catalog = random.sample(MASTER_ITEMS, str_lit.session_state.items_per_day)

# ==========================================
# UIサイドバー
# ==========================================
with str_lit.sidebar:
    str_lit.title("🎴 禁忌のセリ市")
    str_lit.markdown("---")
    str_lit.metric("💰 所持金", f"{str_lit.session_state.player_money} 万G")
    str_lit.metric("🏛️ ミュージアム展示数", f"{len(str_lit.session_state.museum)} 点")
    str_lit.metric("🔍 鑑定チケット", f"{str_lit.session_state.appraisal_tickets} 枚")
    str_lit.metric("📅 開催日数", f"{str_lit.session_state.day} / {str_lit.session_state.max_days} 日目")
    str_lit.markdown("---")
    
    if str_lit.button("🔄 ゲームを最初からやり直す"):
        for key in list(str_lit.session_state.keys()):
            del str_lit.session_state[key]
        str_lit.rerun()

# --- タブ構成 ---
tab1, tab2, tab3 = str_lit.tabs(["🏛️ オークション会場", "💼 所持品 & 闇市（資金調達）", "📖 レリック図鑑 & ミュージアム"])

# ==========================================
# TAB 1: オークション会場
# ==========================================
with tab1:
    if str_lit.session_state.game_over:
        str_lit.header("🏆 5日間の全日程が終了しました！")
        # 資産計算：現金 ＋ 所持品価値 ＋ ミュージアム評価（1.5倍ボーナス）
        inv_value = sum(i["true_value"] for i in str_lit.session_state.inventory)
        museum_value = sum(i["true_value"] * 1.5 for i in str_lit.session_state.museum)
        total_asset = int(str_lit.session_state.player_money + inv_value + museum_value)
        
        str_lit.subheader(f"最終評価総資産: {total_asset} 万G (現金 + 所持品 + ミュージアム展示)")

        if total_asset >= 5000:
            str_lit.balloons()
            str_lit.success("🎉 **エンディング：闇社会のフィクサー**\n圧倒的な財力と至高のコレクションで全ての権力を掌握しました！")
        elif total_asset >= 2500:
            str_lit.info("🎉 **エンディング：一流レリックディーラー**\n確かな目利きと経営手腕で巨万の富を築き上げました。")
        else:
            str_lit.error("💀 **エンディング：破産と黄昏**\n贋作と不運に惑わされ、闇の街に消えていきました…")

    else:
        current_item = str_lit.session_state.daily_catalog[str_lit.session_state.current_item_index]

        if not str_lit.session_state.auction_active:
            str_lit.subheader(f"【{str_lit.session_state.day}日目】 本日の第 {str_lit.session_state.current_item_index + 1} 品目（全3品）")
            col_img, col_info = str_lit.columns([1, 1])

            with col_img:
                str_lit.image(current_item["image_url"], caption=current_item["name"], use_container_width=True)

            with col_info:
                str_lit.markdown(f"### {current_item['name']}")
                str_lit.write(f"**カテゴリ:** {current_item['category']}")
                str_lit.write(f"**推定価値:** {current_item['apparent_value']} 万G (表向きの評価)")
                str_lit.write(f"**詳細:** {current_item['description']}")

                if current_item["id"] in str_lit.session_state.appraised_items:
                    info = str_lit.session_state.appraised_items[current_item["id"]]
                    str_lit.success(f"🔍 **鑑定結果**: 真の価値 = {info['true_value']}万G | 呪い = {'あり(⚠)' if info['is_cursed'] else 'なし'}")
                else:
                    if str_lit.button("🔍 鑑定チケットを使って真価を見破る"):
                        if str_lit.session_state.appraisal_tickets > 0:
                            str_lit.session_state.appraisal_tickets -= 1
                            str_lit.session_state.appraised_items[current_item["id"]] = {
                                "true_value": current_item["true_value"],
                                "is_cursed": current_item["is_cursed"]
                            }
                            str_lit.rerun()
                        else:
                            str_lit.error("鑑定チケットが足りません！")

                str_lit.markdown("---")
                if str_lit.button("🔨 オークション競売を開始する！", type="primary"):
                    start_next_item_auction()
                    str_lit.rerun()

        else:
            str_lit.subheader(f"🔨 競売中：{current_item['name']}")
            col_left, col_right = str_lit.columns([1, 1])

            with col_left:
                str_lit.image(current_item["image_url"], use_container_width=True)
                str_lit.metric("現在最高価格", f"{str_lit.session_state.current_price} 万G", f"最高入札者: {str_lit.session_state.highest_bidder}")

            with col_right:
                str_lit.markdown("##### 📜 オークション実況ログ")
                log_html = "<div class='log-box'>" + "<br>".join(str_lit.session_state.auction_logs) + "</div>"
                str_lit.markdown(log_html, unsafe_allow_html=True)

                str_lit.markdown("---")
                str_lit.markdown("##### 競り合いアクション")
                btn_col1, btn_col2, btn_col3 = str_lit.columns(3)

                with btn_col1:
                    if str_lit.button("＋30万G 上乗せ"):
                        bid_amount = str_lit.session_state.current_price + 30
                        if str_lit.session_state.player_money >= bid_amount:
                            str_lit.session_state.current_price = bid_amount
                            str_lit.session_state.highest_bidder = "あなた"
                            str_lit.session_state.auction_logs.append(f"🔥 あなたが {bid_amount}万G に値上げしました！")
                            if not process_rival_bids():
                                str_lit.session_state.auction_logs.append("✨ ライバルたちはこれ以上出せないようだ…あなたの落札が確定！")
                                finalize_auction("あなた", str_lit.session_state.current_price, current_item)
                            str_lit.rerun()
                        else:
                            str_lit.error("資金が足りません！")

                with btn_col2:
                    if str_lit.button("＋100万G 一発強気"):
                        bid_amount = str_lit.session_state.current_price + 100
                        if str_lit.session_state.player_money >= bid_amount:
                            str_lit.session_state.current_price = bid_amount
                            str_lit.session_state.highest_bidder = "あなた"
                            str_lit.session_state.auction_logs.append(f"💥 あなたが強力な提示 {bid_amount}万G！")
                            if not process_rival_bids():
                                str_lit.session_state.auction_logs.append("✨ 圧倒的な高値に会場が静まり返った…あなたの落札が確定！")
                                finalize_auction("あなた", str_lit.session_state.current_price, current_item)
                            str_lit.rerun()
                        else:
                            str_lit.error("資金が足りません！")

                with btn_col3:
                    if str_lit.button("🏳️ 降りる（パス）"):
                        while process_rival_bids():
                            pass
                        finalize_auction(str_lit.session_state.highest_bidder, str_lit.session_state.current_price, current_item)
                        str_lit.rerun()

# ==========================================
# TAB 2: 所持品 & 闇市（資金調達）
# ==========================================
with tab2:
    str_lit.subheader("💼 あなたの所持アイテム（出口戦略を選択）")
    if not str_lit.session_state.inventory:
        str_lit.info("落札したアイテムはまだありません。オークションでアイテムを獲得しましょう。")
    else:
        for idx, item in enumerate(str_lit.session_state.inventory):
            with str_lit.expander(f"{'⚠ ' if item['is_cursed'] else ''}{item['name']} ({item['category']})"):
                col_a, col_b = str_lit.columns([1, 2])
                with col_a:
                    str_lit.image(item["image_url"], width=150)
                with col_b:
                    str_lit.write(f"**表向き評価:** {item['apparent_value']}万G | **真の価値:** {item['true_value']}万G")
                    str_lit.write(f"**詳細:** {item['description']}")
                    str_lit.markdown("---")
                    
                    # 3つの出口戦略ボタン
                    b1, b2, b3 = str_lit.columns(3)
                    
                    # ① 即時転売
                    with b1:
                        sell_price = int(item['apparent_value'] * (0.6 if item['is_cursed'] else 0.9))
                        if str_lit.button(f"💵 即時転売\n({sell_price}万G)", key=f"sell_{idx}"):
                            str_lit.session_state.player_money += sell_price
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"{item['name']} を即時転売しました！")
                            str_lit.rerun()

                    # ② コレクターへの指名買い（同一カテゴリが2つ以上あればセットボーナス）
                    with b2:
                        same_cat_count = sum(1 for i in str_lit.session_state.inventory if i["category"] == item["category"])
                        bonus_mult = 1.4 if same_cat_count >= 2 else 1.1
                        collector_price = int(item['true_value'] * bonus_mult * (0.5 if item['is_cursed'] else 1.0))
                        
                        btn_label = f"📦 指名買い売却\n({collector_price}万G)"
                        if same_cat_count >= 2:
                            btn_label += " ⭐セットボーナス発動!"
                            
                        if str_lit.button(btn_label, key=f"collector_{idx}"):
                            str_lit.session_state.player_money += collector_price
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"コレクターに売却成功！ {collector_price}万G獲得！")
                            str_lit.rerun()

                    # ③ ミュージアム永久保存
                    with b3:
                        if str_lit.button("🏛️ ミュージアムに永久保存", key=f"museum_{idx}"):
                            str_lit.session_state.museum.append(item)
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"{item['name']} をプライベート・ミュージアムに永久展示しました！")
                            str_lit.rerun()

    str_lit.markdown("---")
    str_lit.subheader("🏬 闇市ブラックマーケット（資金調達手段）")
    
    col_shop1, col_shop2, col_shop3 = str_lit.columns(3)
    
    with col_shop1:
        str_lit.markdown("#### 🎫 鑑定アイテム")
        str_lit.write("真贋や呪いを見破るチケットを購入。")
        if str_lit.button("鑑定チケット購入 (100万G)"):
            if str_lit.session_state.player_money >= 100:
                str_lit.session_state.player_money -= 100
                str_lit.session_state.appraisal_tickets += 1
                str_lit.success("鑑定チケットを1枚補充しました。")
                str_lit.rerun()
            else:
                str_lit.error("資金が足りません！")

    with col_shop2:
        str_lit.markdown("#### 🕵️ 闇バイト・情報売買")
        str_lit.write("裏の仕事を請け負って安全に小銭を稼ぐ。")
        if str_lit.button("闇バイトで稼ぐ (+150万G)"):
            str_lit.session_state.player_money += 150
            str_lit.success("裏仕事を完遂し、150万Gを手に入れました。")
            str_lit.rerun()

    with col_shop3:
        str_lit.markdown("#### 🎰 地下カジノ（違法スロット）")
        str_lit.write("50万Gを賭けて一攫千金（成功で＋300万G）！")
        if str_lit.button("スロットを回す (賭け金: 50万G)"):
            if str_lit.session_state.player_money >= 50:
                str_lit.session_state.player_money -= 50
                if random.random() < 0.35:  # 35%の確率で当たり
                    str_lit.session_state.player_money += 300
                    str_lit.balloons()
                    str_lit.success("🎰 JACKPOT!! 300万Gを獲得しました！")
                else:
                    str_lit.error("🎰 外れ... 賭け金が没収されました。")
                str_lit.rerun()
            else:
                str_lit.error("資金が足りません！")

# ==========================================
# TAB 3: レリック図鑑 & ミュージアム
# ==========================================
with tab3:
    str_lit.subheader("🏛️ あなたのプライベート・ミュージアム（永久保存展示室）")
    str_lit.write("ミュージアムに保存されたアイテムは現金にはなりませんが、ゲームクリア時の最終資産評価に**1.5倍のプレミアムボーナス**として加算されます。")
    
    if not str_lit.session_state.museum:
        str_lit.info("ミュージアムに展示されているレリックはまだありません。所持品タブから「永久保存」を選んで展示しましょう。")
    else:
        m_cols = str_lit.columns(3)
        for m_idx, m_item in enumerate(str_lit.session_state.museum):
            with m_cols[m_idx % 3]:
                str_lit.image(m_item["image_url"], caption=m_item["name"], use_container_width=True)
                str_lit.caption(f"真価評価: {m_item['true_value']}万G (展示中)")

    str_lit.markdown("---")
    str_lit.subheader("📖 レリック・コレクション全集（全15種コンプリート状況）")
    cols = str_lit.columns(3)
    
    # 所持品 ＋ ミュージアム ＋ これまでに入手した全IDを判定
    unlocked_ids = [i["id"] for i in str_lit.session_state.inventory] + [i["id"] for i in str_lit.session_state.museum]

    for idx, item in enumerate(MASTER_ITEMS):
        with cols[idx % 3]:
            if item["id"] in unlocked_ids:
                str_lit.image(item["image_url"], caption=item["name"], use_container_width=True)
                str_lit.caption(f"真価: {item['true_value']}万G | {item['category']}")
            else:
                str_lit.markdown(f"### 🔒 {item['name']}")
                str_lit.caption("オークションで獲得すると解放されます。")
