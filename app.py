import streamlit as st
import random
import time

# ==========================================
# ページ基本設定
# ==========================================
st.set_page_config(
    page_title="レリック・オークション：禁忌のセリ市",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（ダークファンタジー＆サイバーパンク風）
st.markdown("""
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
# マスターデータ定義（出品アイテム ＆ ライバル）
# ==========================================
MASTER_ITEMS = [
    {
        "id": "item_01",
        "name": "魔導サイバーコア",
        "category": "サイバーファンタジー",
        "apparent_value": 300,
        "true_value": 800,
        "is_cursed": False,
        "image_url": "https://picsum.photos/seed/cybercore/400/300",
        "description": "古代の精霊結晶と量子プロセッサが融合した未知のジェネレータ。"
    },
    {
        "id": "item_02",
        "name": "偽りの聖剣アロンダイト",
        "category": "ファンタジー武器",
        "apparent_value": 600,
        "true_value": 50,
        "is_cursed": False,
        "image_url": "https://picsum.photos/seed/fake_sword/400/300",
        "description": "神々しい輝きを放つが、実は精巧に作られた鍍金メッキのレプリカ。"
    },
    {
        "id": "item_03",
        "name": "呪われたニューラル・バイザー",
        "category": "不法サイバーパーツ",
        "apparent_value": 450,
        "true_value": 100,
        "is_cursed": True,
        "image_url": "https://picsum.photos/seed/cursed_visor/400/300",
        "description": "圧倒的な処理能力を誇るが、装着者の精神を侵食するバグが潜む。"
    },
    {
        "id": "item_04",
        "name": "竜血の錬金薬瓶",
        "category": "魔法遺物",
        "apparent_value": 200,
        "true_value": 700,
        "is_cursed": False,
        "image_url": "https://picsum.photos/seed/dragon_potion/400/300",
        "description": "ドロリとした怪しい液体。伝説の古龍の血だと証言されている。"
    },
    {
        "id": "item_05",
        "name": "錆びついたAIメモリ端末",
        "category": "サイバー遺物",
        "apparent_value": 100,
        "true_value": 1200,
        "is_cursed": False,
        "image_url": "https://picsum.photos/seed/rusty_ai/400/300",
        "description": "一見ただのジャンク品。だが内部には旧時代の暗号通貨キーが眠る。"
    },
    {
        "id": "item_06",
        "name": "死霊術師のクロノグラフ",
        "category": "呪物",
        "apparent_value": 500,
        "true_value": 900,
        "is_cursed": True,
        "image_url": "https://picsum.photos/seed/necromancer_watch/400/300",
        "description": "針が逆回転する怪しい懐中時計。強力な時間魔術の触媒。"
    }
]

RIVALS = [
    {"name": "貴族オルガ", "type": "堅実派", "budget": 1000, "favorite": "ファンタジー武器", "aggressiveness": 0.4},
    {"name": "ハッカー・ゼロ", "type": "撹乱派", "budget": 800, "favorite": "サイバー遺物", "aggressiveness": 0.7},
    {"name": "コレクター・バルト", "type": "執着派", "budget": 1500, "favorite": "魔法遺物", "aggressiveness": 0.8}
]

# ==========================================
# セッション状態の初期化 (`st.session_state`)
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player_money = 1000  # 初期所持金（万G）
    st.session_state.appraisal_tickets = 2  # 初期鑑定チケット
    st.session_state.day = 1
    st.session_state.max_days = 3
    st.session_state.items_per_day = 2
    st.session_state.current_item_index = 0
    st.session_state.inventory = []  # 所持アイテム
    st.session_state.appraised_items = {}  # 鑑定済み情報 {item_id: dict}
    st.session_state.game_over = False

    # 現在のオークション状態
    st.session_state.auction_active = False
    st.session_state.current_price = 0
    st.session_state.highest_bidder = None
    st.session_state.auction_logs = []
    st.session_state.daily_catalog = random.sample(MASTER_ITEMS, min(st.session_state.items_per_day, len(MASTER_ITEMS)))

# ==========================================
# ゲームロジック補助関数
# ==========================================
def start_next_item_auction():
    """次のアイテムのオークションを開始"""
    item = st.session_state.daily_catalog[st.session_state.current_item_index]
    st.session_state.current_price = int(item["apparent_value"] * 0.5)  # スタート価格は見た目価値の半額
    st.session_state.highest_bidder = "主催者"
    st.session_state.auction_logs = [f"【競売開始】『{item['name']}』が出品されました！ 初期価格: {st.session_state.current_price}万G"]
    st.session_state.auction_active = True

def process_rival_bids():
    """ライバルAIの入札ロジック（ライバルが上乗せできたらTrue、誰も上乗せできずパスならFalse）"""
    item = st.session_state.daily_catalog[st.session_state.current_item_index]
    current_p = st.session_state.current_price

    bidders = []
    for rival in RIVALS:
        if rival["budget"] < current_p + 20:
            continue
        
        # 思考判定
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
        # 一番高値をつけたライバルを採用
        selected_rival, new_price = max(bidders, key=lambda x: x[1])
        st.session_state.current_price = new_price
        st.session_state.highest_bidder = selected_rival["name"]
        st.session_state.auction_logs.append(f"⚡ {selected_rival['name']} が {new_price}万G に値上げしました！")
        return True
    
    return False

def finalize_auction(winner, price, item):
    """オークション終了時の処理と次のアイテムへの移行"""
    st.session_state.auction_active = False

    if winner == "あなた":
        st.session_state.player_money -= price
        st.session_state.inventory.append(item)
        st.toast(f"🎉 {item['name']} を {price}万G で落札しました！", icon="🎉")
    else:
        st.toast(f"❌ {winner} に {price}万G で競り落とされました...", icon="💸")

    # 次のアイテムへ進む処理
    st.session_state.current_item_index += 1
    if st.session_state.current_item_index >= len(st.session_state.daily_catalog):
        st.session_state.day += 1
        st.session_state.current_item_index = 0
        if st.session_state.day > st.session_state.max_days:
            st.session_state.game_over = True
        else:
            st.session_state.daily_catalog = random.sample(MASTER_ITEMS, min(st.session_state.items_per_day, len(MASTER_ITEMS)))

# ==========================================
# UI & メイン画面レイアウト
# ==========================================

# --- サイドバー (ステータス表示) ---
with st.sidebar:
    st.title("🎴 禁忌のセリ市")
    st.markdown("---")
    st.metric("💰 所持金", f"{st.session_state.player_money} 万G")
    st.metric("🔍 鑑定チケット", f"{st.session_state.appraisal_tickets} 枚")
    st.metric("📅 開催日数", f"{st.session_state.day} / {st.session_state.max_days} 日目")
    st.markdown("---")
    
    if st.button("🔄 ゲームを最初からやり直す"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- メインエリア タブ構成 ---
tab1, tab2, tab3 = st.tabs(["🏛️ オークション会場", "💼 所持品 & 闇市", "📖 レリック図鑑"])

# ==========================================
# TAB 1: オークション会場
# ==========================================
with tab1:
    if st.session_state.game_over:
        st.header("🏆 オークション全日程終了！")
        total_asset = st.session_state.player_money + sum(i["true_value"] for i in st.session_state.inventory)
        st.subheader(f"最終評価総資産: {total_asset} 万G")

        if total_asset >= 3000:
            st.balloons()
            st.success("🎉 **エンディング：闇社会のフィクサー**\n圧倒的な財力でオークションの支配者となりました！")
        elif total_asset >= 1500:
            st.info("🎉 **エンディング：一流レリックディーラー**\n確かな目利きで巨万の富を築きました。")
        else:
            st.error("💀 **エンディング：破産と黄昏**\n贋作と呪いに惑わされ、闇の街に消えていきました…")

    else:
        current_item = st.session_state.daily_catalog[st.session_state.current_item_index]

        # 準備状態（オークション未スタート）
        if not st.session_state.auction_active:
            st.subheader(f"【本日第 {st.session_state.current_item_index + 1} 品目】 出品物の下調べ")
            col_img, col_info = st.columns([1, 1])

            with col_img:
                st.image(current_item["image_url"], caption=current_item["name"], use_container_width=True)

            with col_info:
                st.markdown(f"### {current_item['name']}")
                st.write(f"**カテゴリ:** {current_item['category']}")
                st.write(f"**推定価値:** {current_item['apparent_value']} 万G (表向きの評価)")
                st.write(f"**詳細:** {current_item['description']}")

                # 鑑定済みチェック
                if current_item["id"] in st.session_state.appraised_items:
                    info = st.session_state.appraised_items[current_item["id"]]
                    st.success(f"🔍 **鑑定結果**: 真の価値 = {info['true_value']}万G | 呪い = {'あり(⚠)' if info['is_cursed'] else 'なし'}")
                else:
                    if st.button("🔍 鑑定チケットを使って真価を見破る"):
                        if st.session_state.appraisal_tickets > 0:
                            st.session_state.appraisal_tickets -= 1
                            st.session_state.appraised_items[current_item["id"]] = {
                                "true_value": current_item["true_value"],
                                "is_cursed": current_item["is_cursed"]
                            }
                            st.rerun()
                        else:
                            st.error("鑑定チケットが足りません！")

                st.markdown("---")
                if st.button("🔨 オークション競売を開始する！", type="primary"):
                    start_next_item_auction()
                    st.rerun()

        # オークション進行中
        else:
            st.subheader(f"🔨 競売中：{current_item['name']}")

            col_left, col_right = st.columns([1, 1])

            with col_left:
                st.image(current_item["image_url"], use_container_width=True)
                st.metric("現在最高価格", f"{st.session_state.current_price} 万G", f"最高入札者: {st.session_state.highest_bidder}")

            with col_right:
                st.markdown("##### 📜 オークション実況ログ")
                log_html = "<div class='log-box'>" + "<br>".join(st.session_state.auction_logs) + "</div>"
                st.markdown(log_html, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("##### 競り合いアクション")
                btn_col1, btn_col2, btn_col3 = st.columns(3)

                with btn_col1:
                    if st.button("＋30万G 上乗せ"):
                        bid_amount = st.session_state.current_price + 30
                        if st.session_state.player_money >= bid_amount:
                            st.session_state.current_price = bid_amount
                            st.session_state.highest_bidder = "あなた"
                            st.session_state.auction_logs.append(f"🔥 あなたが {bid_amount}万G に値上げしました！")
                            
                            # ライバルが追いついてくるか判定
                            has_rival_countered = process_rival_bids()
                            if not has_rival_countered:
                                # ライバルが誰も追いつけなければ、プレイヤーの即時落札成立！
                                st.session_state.auction_logs.append("✨ ライバルたちはこれ以上出せないようだ…あなたの落札が確定！")
                                finalize_auction("あなた", st.session_state.current_price, current_item)
                            
                            st.rerun()
                        else:
                            st.error("資金が足りません！")

                with btn_col2:
                    if st.button("＋100万G 一発強気"):
                        bid_amount = st.session_state.current_price + 100
                        if st.session_state.player_money >= bid_amount:
                            st.session_state.current_price = bid_amount
                            st.session_state.highest_bidder = "あなた"
                            st.session_state.auction_logs.append(f"💥 あなたが強力な提示 {bid_amount}万G！")
                            
                            # 強気な金額なのでライバルが追いつく確率は低いが判定する
                            has_rival_countered = process_rival_bids()
                            if not has_rival_countered:
                                st.session_state.auction_logs.append("✨ 圧倒的な高値に会場が静まり返った…あなたの落札が確定！")
                                finalize_auction("あなた", st.session_state.current_price, current_item)
                            
                            st.rerun()
                        else:
                            st.error("資金が足りません！")

                with btn_col3:
                    if st.button("🏳️ 降りる（パス）"):
                        # 降りた場合はライバルの中から最高値の人が落札
                        while process_rival_bids():
                            pass
                        
                        winner = st.session_state.highest_bidder
                        price = st.session_state.current_price
                        finalize_auction(winner, price, current_item)
                        st.rerun()

# ==========================================
# TAB 2: 所持品 & 闇市
# ==========================================
with tab2:
    st.subheader("💼 あなたの所持アイテム（インベントリ）")
    if not st.session_state.inventory:
        st.info("落札したアイテムはまだありません。")
    else:
        for idx, item in enumerate(st.session_state.inventory):
            with st.expander(f"{'⚠ ' if item['is_cursed'] else ''}{item['name']} (購入価格: ???)"):
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.image(item["image_url"], width=150)
                with col_b:
                    st.write(f"**真の価値:** {item['true_value']} 万G")
                    st.write(f"**状態:** {'呪われている (売却額減少)' if item['is_cursed'] else '正常'}")
                    sell_price = int(item['true_value'] * (0.5 if item['is_cursed'] else 0.9))
                    if st.button(f"コレクターに売却 ({sell_price}万G)", key=f"sell_{idx}"):
                        st.session_state.player_money += sell_price
                        st.session_state.inventory.pop(idx)
                        st.success(f"{item['name']} を売却しました！")
                        st.rerun()

    st.markdown("---")
    st.subheader("🏬 闇市ブラックマーケット")
    if st.button("💳 鑑定チケットを購入する (100万G)"):
        if st.session_state.player_money >= 100:
            st.session_state.player_money -= 100
            st.session_state.appraisal_tickets += 1
            st.success("鑑定チケットを1枚補充しました。")
            st.rerun()
        else:
            st.error("資金が足りません。")

# ==========================================
# TAB 3: レリック図鑑
# ==========================================
with tab3:
    st.subheader("📖 レリック・コレクション全集")
    cols = st.columns(3)
    unlocked_ids = [i["id"] for i in st.session_state.inventory]

    for idx, item in enumerate(MASTER_ITEMS):
        with cols[idx % 3]:
            if item["id"] in unlocked_ids:
                st.image(item["image_url"], caption=item["name"], use_container_width=True)
                st.caption(f"真価: {item['true_value']}万G | {item['category']}")
            else:
                st.markdown("### 🔒 未解放")
                st.caption("オークションで獲得すると解放されます。")
