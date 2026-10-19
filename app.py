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

# カスタムCSS（ダークファンタジー＆サイバーパンク風 ＆ オークション対戦カード用）
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
        height: 220px;
        overflow-y: auto;
    }
    .bidder-card {
        background-color: #161b2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .bidder-card-active {
        background-color: #1a365d;
        border: 2px solid #00f0ff;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# マスターデータ定義（30種類の出品アイテム）
# ==========================================
MASTER_ITEMS = [
    {"id": "item_01", "name": "魔導サイバーコア", "category": "サイバーファンタジー", "apparent_value": 300, "true_value": 800, "is_cursed": False, "image_url": "images/cybercore.jpg", "description": "古代の精霊結晶と量子プロセッサが融合した未知のジェネレータ。"},
    {"id": "item_02", "name": "偽りの聖剣アロンダイト", "category": "ファンタジー武器", "apparent_value": 600, "true_value": 50, "is_cursed": False, "image_url": "images/fake_sword.jpg", "description": "神々しい輝きを放つが、実は精巧に作られた鍍金メッキのレプリカ。"},
    {"id": "item_03", "name": "呪われたニューラル・バイザー", "category": "不法サイバーパーツ", "apparent_value": 450, "true_value": 1000, "is_cursed": True, "unpurifiable": True, "image_url": "images/cursed_visor.jpg", "description": "圧倒的な処理能力を誇るが、装着者の精神を侵食するバグが潜む。"},
    {"id": "item_04", "name": "竜血の錬金薬瓶", "category": "魔法遺物", "apparent_value": 200, "true_value": 700, "is_cursed": False, "image_url": "images/dragon_potion.jpg", "description": "ドロリとした怪しい液体。伝説の古龍の血だと証言されている。"},
    {"id": "item_05", "name": "錆びついたAIメモリ端末", "category": "サイバー遺物", "apparent_value": 100, "true_value": 1200, "is_cursed": False, "image_url": "images/rusty_ai.jpg", "description": "一見ただのジャンク品。だが内部には旧時代の暗号通貨キーが眠る。"},
    {"id": "item_06", "name": "死霊術師のクロノグラフ", "category": "呪物", "apparent_value": 500, "true_value": 900, "is_cursed": True, "unpurifiable": True, "image_url": "images/necromancer_watch.jpg", "description": "針が逆回転する怪しい懐中時計。強力な時間魔術の触媒。"},
    {"id": "item_07", "name": "星詠みの水晶ドローン", "category": "サイバーファンタジー", "apparent_value": 400, "true_value": 650, "is_cursed": False, "image_url": "images/crystal_drone.jpg", "description": "未来予測AIと占星術アルゴリズムが同居した浮遊観測デバイス。"},
    {"id": "item_08", "name": "ブラッド・エッジブレード", "category": "ファンタジー武器", "apparent_value": 700, "true_value": 950, "is_cursed": True, "image_url": "images/blood_edge.jpg", "description": "持ち主の闘気を吸い取って切れ味を増す呪われた魔剣。"},
    {"id": "item_09", "name": "エーテル・チャージャー", "category": "魔法遺物", "apparent_value": 350, "true_value": 400, "is_cursed": False, "image_url": "images/ether_charger.jpg", "description": "魔力を無限に再充填できるとされる魔導バッテリーの試作品。"},
    {"id": "item_10", "name": "次元回廊のパスカード", "category": "サイバー遺物", "apparent_value": 800, "true_value": 1500, "is_cursed": False, "image_url": "images/dimension_pass.jpg", "description": "裏社会のネットワークの最深層へアクセスできるブラックパス。"},
    {"id": "item_11", "name": "模造エリクサーの空瓶", "category": "魔法遺物", "apparent_value": 150, "true_value": 20, "is_cursed": False, "image_url": "images/empty_elixir.jpg", "description": "かつて不老不死の薬が入っていたとされる、ただのガラスの空容器。"},
    {"id": "item_12", "name": "ゴースト・インプラント", "category": "不法サイバーパーツ", "apparent_value": 550, "true_value": 1100, "is_cursed": True, "image_url": "images/ghost_implant.jpg", "description": "人格データを書き換える違法チップ。前の持ち主の意識が残る噂がある。"},
    {"id": "item_13", "name": "タイタンの巨腕ガントレット", "category": "ファンタジー武器", "apparent_value": 650, "true_value": 750, "is_cursed": False, "image_url": "images/titan_gauntlet.jpg", "description": "圧倒的な怪力を得る代わりに、装着者の機動力を奪う重量級防具。"},
    {"id": "item_14", "name": "キメラの遺伝子サンプル", "category": "サイバーファンタジー", "apparent_value": 500, "true_value": 850, "is_cursed": True, "image_url": "images/chimera_dna.jpg", "description": "竜の遺伝子とナマシンセクトを掛け合わせた危険な培養カプセル。"},
    {"id": "item_15", "name": "黄昏の懐中鏡", "category": "呪物", "apparent_value": 300, "true_value": 600, "is_cursed": True, "unpurifiable": True, "image_url": "images/twilight_mirror.jpg", "description": "覗き込むと、自分自身の死に様が映し出されるという不吉な手鏡。"},
    # --- 🔽 ここから新規追加の15種類 ---
    {"id": "item_16", "name": "量子結界のオーブ", "category": "サイバーファンタジー", "apparent_value": 500, "true_value": 1100, "is_cursed": False, "image_url": "images/quantum_orb.jpg", "description": "高密度エネルギーを圧縮し、周囲に絶対防御フィールドを展開する球体。"},
    {"id": "item_17", "name": "オーガの破城槌", "category": "ファンタジー武器", "apparent_value": 450, "true_value": 500, "is_cursed": False, "image_url": "images/ogre_hammer.jpg", "description": "城門すらも一撃で粉砕すると伝えられる、無骨な巨木の大槌。"},
    {"id": "item_18", "name": "怨念を宿すパペット", "category": "呪物", "apparent_value": 350, "true_value": 900, "is_cursed": True, "unpurifiable": True, "image_url": "images/cursed_puppet.jpg", "description": "夜な夜な勝手に動き出し、不気味な笑い声をあげる不吉な人形。"},
    {"id": "item_19", "name": "賢者のホログラム書物", "category": "魔法遺物", "apparent_value": 700, "true_value": 1400, "is_cursed": False, "image_url": "images/sage_book.jpg", "description": "失われた古代魔法の全知識が光の投影として記録された魔導書。"},
    {"id": "item_20", "name": "クラック・インプラントアイ", "category": "不法サイバーパーツ", "apparent_value": 400, "true_value": 850, "is_cursed": True, "image_url": "images/crack_eye.jpg", "description": "視界のすべてがデータ化されるが、視神経を徐々に焼き切る義眼。"},
    {"id": "item_21", "name": "電脳魔獣の心臓", "category": "サイバー遺物", "apparent_value": 900, "true_value": 1800, "is_cursed": False, "image_url": "images/cyber_heart.jpg", "description": "メカと生体組織が複雑に絡み合い、今なお脈動を続ける巨大なコア。"},
    {"id": "item_22", "name": "月光のシルクローブ", "category": "魔法遺物", "apparent_value": 300, "true_value": 600, "is_cursed": False, "image_url": "images/moon_robe.jpg", "description": "月の光を浴びることで、着用者の気配を完全に遮断する神秘の布衣。"},
    {"id": "item_23", "name": "血塗られた処刑人の斧", "category": "ファンタジー武器", "apparent_value": 550, "true_value": 800, "is_cursed": True, "image_url": "images/executioner_axe.jpg", "description": "数多の罪人の血を吸い、持つ者に血の渇望を引き起こす戦斧。"},
    {"id": "item_24", "name": "ガイアの生体プラグ", "category": "サイバーファンタジー", "apparent_value": 600, "true_value": 1250, "is_cursed": False, "image_url": "images/gaia_plug.jpg", "description": "プラネットネットワークと直接同調し、環境エネルギーを直接引き出す。"},
    {"id": "item_25", "name": "ファントム・ドライヴ", "category": "サイバー遺物", "apparent_value": 750, "true_value": 1600, "is_cursed": False, "image_url": "images/phantom_drive.jpg", "description": "存在そのものを一時的にデータ化し、あらゆる物理障害をすり抜ける基盤。"},
    {"id": "item_26", "name": "黄泉還りの香炉", "category": "呪物", "apparent_value": 400, "true_value": 1000, "is_cursed": True, "unpurifiable": True, "image_url": "images/yomi_censer.jpg", "description": "焚きしめると死者の幻影を呼び寄せる、狂気と神秘の香炉。"},
    {"id": "item_27", "name": "ミスリル合金のバックラー", "category": "ファンタジー武器", "apparent_value": 500, "true_value": 700, "is_cursed": False, "image_url": "images/mithril_buckler.jpg", "description": "極めて軽量かつ高い硬度を誇る、エルフ族秘伝の小型盾。"},
    {"id": "item_28", "name": "暴走する自律型ドローン", "category": "不法サイバーパーツ", "apparent_value": 350, "true_value": 600, "is_cursed": True, "image_url": "images/rogue_drone.jpg", "description": "ハッキングによって制御を失い、周囲の動くものに銃口を向け続ける機体。"},
    {"id": "item_29", "name": "星図の刻まれたアストロラーベ", "category": "魔法遺物", "apparent_value": 650, "true_value": 1300, "is_cursed": False, "image_url": "images/astrolabe.jpg", "description": "宇宙の真理と未来の天体配置を正確無比に指し示す魔導天体儀。"},
    {"id": "item_30", "name": "パンドラのブラックボックス", "category": "呪物", "apparent_value": 1000, "true_value": 2500, "is_cursed": True, "unpurifiable": True, "image_url": "images/pandora_box.jpg", "description": "いかなる解析も受け付けない、開けた者に破滅か無限の富をもたらす謎の箱。"}
]


RIVALS = [
    {"name": "貴族オルガ", "type": "堅実派", "budget": 1200, "favorite": "ファンタジー武器", "aggressiveness": 0.4, "image": "https://picsum.photos/seed/rival_olga/100/100"},
    {"name": "ハッカー・ゼロ", "type": "撹乱派", "budget": 1000, "favorite": "サイバー遺物", "aggressiveness": 0.7, "image": "https://picsum.photos/seed/rival_zero/100/100"},
    {"name": "コレクター・バルト", "type": "執着派", "budget": 1800, "favorite": "魔法遺物", "aggressiveness": 0.8, "image": "https://picsum.photos/seed/rival_valto/100/100"}
]

# ==========================================
# セッション状態の初期化
# ==========================================
if "initialized" not in str_lit.session_state:
    str_lit.session_state.initialized = True
    str_lit.session_state.player_money = 1200  # 初期所持金（万G）
    str_lit.session_state.debt = 0             # 借金（万G）
    str_lit.session_state.appraisal_tickets = 3  # 初期鑑定チケット
    str_lit.session_state.day = 1
    str_lit.session_state.max_days = 5  
    str_lit.session_state.items_per_day = 3
    str_lit.session_state.current_item_index = 0
    str_lit.session_state.inventory = []  # 所持アイテム
    str_lit.session_state.museum = []  # ミュージアム永久保存アイテム
    str_lit.session_state.unlocked_collection = set() # 一度でも獲得したアイテムIDを永続保存
    str_lit.session_state.appraised_items = {}
    str_lit.session_state.game_over = False

    # バイト回数制限管理（日ごと）
    str_lit.session_state.part_time_jobs_today = 0

    # 🔽【追加】一度も出品されていないマスターアイテムのプールを作成
    str_lit.session_state.available_pool = MASTER_ITEMS.copy()

    str_lit.session_state.auction_active = False
    str_lit.session_state.current_price = 0
    str_lit.session_state.highest_bidder = "主催者"
    str_lit.session_state.rival_bids = {r["name"]: "パス" for r in RIVALS}
    str_lit.session_state.auction_logs = []
    
    # 🔽【変更】プールから初日のカタログを抽選（足りない場合はプール全体から）
    sample_count = min(str_lit.session_state.items_per_day, len(str_lit.session_state.available_pool))
    str_lit.session_state.daily_catalog = random.sample(str_lit.session_state.available_pool, sample_count)
    # 選択されたアイテムをプールから除外
    for item in str_lit.session_state.daily_catalog:
        str_lit.session_state.available_pool.remove(item)

# ==========================================
# ロジック関数
# ==========================================
def apply_turn_penalties():
    """ターン経過時のペナルティ（呪いアイテムの悪影響 ＆ 借金の利息）＆ バイト回数リセット"""
    curse_count = sum(1 for item in str_lit.session_state.inventory if item.get("is_cursed", False))
    if curse_count > 0:
        penalty = curse_count * 50
        str_lit.session_state.player_money = max(0, str_lit.session_state.player_money - penalty)
        str_lit.session_state.auction_logs.append(f"💀【呪いの災厄】呪物の悪影響により、資金が {penalty}万G 削られました...")
    
    if str_lit.session_state.debt > 0:
        interest = int(str_lit.session_state.debt * 0.2)
        str_lit.session_state.debt += interest
        str_lit.session_state.auction_logs.append(f"💳【闇金からの取り立て】借金の利息が発生しました (+{interest}万G)。残高: {str_lit.session_state.debt}万G")

    str_lit.session_state.part_time_jobs_today = 0

def start_next_item_auction():
    item = str_lit.session_state.daily_catalog[str_lit.session_state.current_item_index]
    str_lit.session_state.current_price = int(item["apparent_value"] * 0.5)
    str_lit.session_state.highest_bidder = "主催者"
    str_lit.session_state.rival_bids = {r["name"]: "待機中" for r in RIVALS}
    str_lit.session_state.auction_logs = [f"【競売開始】『{item['name']}』が出品されました！ 初期価格: {str_lit.session_state.current_price}万G"]
    str_lit.session_state.auction_active = True

def process_rival_bids():
    item = str_lit.session_state.daily_catalog[str_lit.session_state.current_item_index]
    current_p = str_lit.session_state.current_price

    bidders = []
    for rival in RIVALS:
        if rival["budget"] < current_p + 20:
            str_lit.session_state.rival_bids[rival["name"]] = "資金切れ/パス"
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
        else:
            str_lit.session_state.rival_bids[rival["name"]] = "様子見"

    if bidders:
        selected_rival, new_price = max(bidders, key=lambda x: x[1])
        str_lit.session_state.current_price = new_price
        str_lit.session_state.highest_bidder = selected_rival["name"]
        str_lit.session_state.rival_bids[selected_rival["name"]] = f"{new_price}万G (最高値)"
        str_lit.session_state.auction_logs.append(f"⚡ {selected_rival['name']} が {new_price}万G に値上げしました！")
        return True
    return False

def finalize_auction(winner, price, item):
    str_lit.session_state.auction_active = False
    if winner == "あなた":
        str_lit.session_state.player_money -= price
        item_copy = item.copy()
        str_lit.session_state.inventory.append(item_copy)
        str_lit.session_state.unlocked_collection.add(item["id"])
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
            apply_turn_penalties()
            
            # 🔽【変更】未出品プールから本日のカタログを抽選（プールが空の場合はマスターからフォールバック）
            if len(str_lit.session_state.available_pool) > 0:
                sample_count = min(str_lit.session_state.items_per_day, len(str_lit.session_state.available_pool))
                str_lit.session_state.daily_catalog = random.sample(str_lit.session_state.available_pool, sample_count)
                for d_item in str_lit.session_state.daily_catalog:
                    str_lit.session_state.available_pool.remove(d_item)
            else:
                str_lit.session_state.daily_catalog = random.sample(MASTER_ITEMS, str_lit.session_state.items_per_day)

# ==========================================
# UIサイドバー
# ==========================================
with str_lit.sidebar:
    str_lit.title("🎴 禁忌のセリ市")
    str_lit.markdown("---")
    str_lit.metric("💰 所持金", f"{str_lit.session_state.player_money} 万G")
    if str_lit.session_state.debt > 0:
        str_lit.metric("💳 借金残高", f"{str_lit.session_state.debt} 万G", delta_color="inverse")
    str_lit.metric("🏛️ ミュージアム展示数", f"{len(str_lit.session_state.museum)} 点")
    str_lit.metric("🔍 鑑定チケット", f"{str_lit.session_state.appraisal_tickets} 枚")
    str_lit.metric("📅 開催日数", f"{str_lit.session_state.day} / {str_lit.session_state.max_days} 日目")
    str_lit.markdown("---")
    
    if str_lit.button("🔄 ゲームを最初からやり直す"):
        for key in list(str_lit.session_state.keys()):
            del str_lit.session_state[key]
        str_lit.rerun()

# --- タブ構成 ---
tab1, tab2, tab3 = str_lit.tabs(["🏛️ オークション会場", "💼 所持品 & 闇市（資金調達・返済）", "📖 レリック図鑑 & ミュージアム"])

# ==========================================
# TAB 1: オークション会場
# ==========================================
with tab1:
    if str_lit.session_state.game_over:
        str_lit.header("🏆 5日間の全日程が終了しました！")
        inv_value = sum(i["true_value"] for i in str_lit.session_state.inventory)
        museum_value = sum(i["true_value"] * 1.5 for i in str_lit.session_state.museum)
        total_asset = int(str_lit.session_state.player_money + inv_value + museum_value - str_lit.session_state.debt)
        
        # 特殊エンド判定
        museum_count = len(str_lit.session_state.museum)
        cursed_in_inv = sum(1 for i in str_lit.session_state.inventory if i.get("is_cursed", False))
        
        str_lit.subheader(f"最終評価総資産（借金返済後）: {total_asset} 万G")

        # 分岐によるエンド判定と画像の表示
        if museum_count >= 5:
            str_lit.balloons()
            str_lit.success("🏛️ **エンディング1：【伝説の館長・ミュージアム支配者】**\n圧倒的な数の至高のレリックを後世に残し、闇社会の文化の父となりました！")
            str_lit.image("images/ending_museum.jpg", caption="エンドイラスト：伝説のミュージアム")
        elif cursed_in_inv >= 2:
            str_lit.error("☠️ **エンディング2：【呪いの亡者】**\n強力な呪物を所持し続けた代償に魂を侵食され、闇の美術館の新たな「展示物」となってしまいました……")
            str_lit.image("images/ending_cursed.jpg", caption="エンドイラスト：呪いに呑まれたディーラー")
        elif str_lit.session_state.debt >= 500:
            str_lit.error("💳 **エンディング3：【闇金の奴隷】**\n膨れ上がった借金を返済できず、組織の底辺労働者として永遠に働き続けることになりました……")
            str_lit.image("images/ending_debt.jpg", caption="エンドイラスト：影に沈む借金生活")
        elif total_asset >= 5000:
            str_lit.balloons()
            str_lit.success("🎉 **エンディング4：【闇社会のフィクサー】**\n圧倒的な財力と至高のコレクションで全ての権力を掌握しました！")
            str_lit.image("images/ending_fixer.jpg", caption="エンドイラスト：夜の街を統べる者")
        elif total_asset >= 2500:
            str_lit.info("🎉 **エンディング5：【一流レリックディーラー】**\n確かな目利きと経営手腕で巨万の富を築き上げました。")
            str_lit.image("images/ending_dealer.jpg", caption="エンドイラスト：華やかなオークション会場")
        else:
            str_lit.error("💀 **エンディング6：【破産と黄昏】**\n借金と呪いに押しつぶされ、闇の街の底に消えていきました…")
            str_lit.image("images/ending_bankruptcy.jpg", caption="エンドイラスト：黄昏の裏路地")

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
                    curse_msg = "解呪不能の絶対的呪物(⚠⚠)" if current_item.get("unpurifiable") else ("あり(⚠)" if info['is_cursed'] else "なし")
                    str_lit.success(f"🔍 **鑑定結果**: 真の価値 = {info['true_value']}万G | 呪い = {curse_msg}")
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
            
            str_lit.markdown("#### 👥 参加者リアルタイム状況")
            p_col, r1_col, r2_col, r3_col = str_lit.columns(4)

            with p_col:
                is_p_active = str_lit.session_state.highest_bidder == "あなた"
                box_class = "bidder-card-active" if is_p_active else "bidder-card"
                str_lit.markdown(f"""
                <div class="{box_class}">
                    <b>あなた（プレイヤー）</b><br>
                    所持金: {str_lit.session_state.player_money}万G<br>
                    状態: {'🌟 最高入札中！' if is_p_active else '参加中'}
                </div>
                """, unsafe_allow_html=True)

            for r_idx, rival in enumerate(RIVALS):
                r_col = [r1_col, r2_col, r3_col][r_idx]
                is_r_active = str_lit.session_state.highest_bidder == rival["name"]
                r_box_class = "bidder-card-active" if is_r_active else "bidder-card"
                r_status = str_lit.session_state.rival_bids.get(rival["name"], "待機中")
                with r_col:
                    str_lit.markdown(f"""
                    <div class="{r_box_class}">
                        <b>{rival['name']}</b><br>
                        <span style="font-size:0.85em; color:#a0aec0;">{rival['type']}</span><br>
                        提示: <b>{r_status}</b>
                    </div>
                    """, unsafe_allow_html=True)

            str_lit.markdown("---")
            col_left, col_right = str_lit.columns([1, 1])

            with col_left:
                str_lit.image(current_item["image_url"], use_container_width=True)
                

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
# TAB 2: 所持品 & 闇市（資金調達・返済）
# ==========================================
with tab2:
    str_lit.subheader("💼 あなたの所持アイテム（出口戦略 & 解呪判定）")
    if not str_lit.session_state.inventory:
        str_lit.info("落札したアイテムはまだありません。オークションでアイテムを獲得しましょう。")
    else:
        for idx, item in enumerate(str_lit.session_state.inventory):
            if item.get("unpurifiable", False):
                status_text = "☠ 【解呪不能】絶対的呪物 (浄化不可・所持ペナルティ大)"
            elif item.get("is_cursed", False):
                status_text = "⚠ 呪われています (浄化可能)"
            else:
                status_text = "✨ 浄化済み (安全)"

            with str_lit.expander(f"{'☠ ' if item.get('unpurifiable') else ('⚠ ' if item.get('is_cursed') else '')}{item['name']} ({item['category']}) - {status_text}"):
                col_a, col_b = str_lit.columns([1, 2])
                with col_a:
                    str_lit.image(item["image_url"], width=150)
                with col_b:
                    str_lit.write(f"**表向き評価:** {item['apparent_value']}万G | **真の価値:** {item['true_value']}万G")
                    str_lit.write(f"**詳細:** {item['description']}")
                    str_lit.markdown("---")
                    
                    if item.get("is_cursed", False):
                        if item.get("unpurifiable", False):
                            str_lit.error("☠ このアイテムは専門家の力でも**解呪不能**な絶対的呪物です！ 浄化することができません。")
                        else:
                            if str_lit.button("🔮 呪い専門家に封印・浄化を依頼する (150万G)", key=f"purify_{idx}"):
                                if str_lit.session_state.player_money >= 150:
                                    str_lit.session_state.player_money -= 150
                                    item["is_cursed"] = False
                                    str_lit.success(f"{item['name']} の呪いが完全に浄化されました！")
                                    str_lit.rerun()
                                else:
                                    str_lit.error("浄化費用（150万G）が足りません！")
                        str_lit.markdown("---")

                    b1, b2, b3 = str_lit.columns(3)
                    
                    with b1:
                        sell_price = int(item['apparent_value'] * (0.4 if item.get('unpurifiable') else (0.6 if item.get('is_cursed') else 0.9)))
                        if str_lit.button(f"💵 即時転売\n({sell_price}万G)", key=f"sell_{idx}"):
                            str_lit.session_state.player_money += sell_price
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"{item['name']} を即時転売しました！")
                            str_lit.rerun()

                    with b2:
                        same_cat_count = sum(1 for i in str_lit.session_state.inventory if i["category"] == item["category"])
                        bonus_mult = 1.4 if same_cat_count >= 2 else 1.1
                        collector_price = int(item['true_value'] * bonus_mult * (0.3 if item.get('unpurifiable') else (0.5 if item.get('is_cursed') else 1.0)))
                        
                        btn_label = f"📦 指名買い売却\n({collector_price}万G)"
                        if same_cat_count >= 2:
                            btn_label += " ⭐セットボーナス!"
                            
                        if str_lit.button(btn_label, key=f"collector_{idx}"):
                            str_lit.session_state.player_money += collector_price
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"コレクターに売却成功！ {collector_price}万G獲得！")
                            str_lit.rerun()

                    with b3:
                        if str_lit.button("🏛️ ミュージアムに永久保存", key=f"museum_{idx}"):
                            str_lit.session_state.museum.append(item)
                            str_lit.session_state.inventory.pop(idx)
                            str_lit.success(f"{item['name']} をプライベート・ミュージアムに永久展示しました！")
                            str_lit.rerun()

    str_lit.markdown("---")
    str_lit.subheader("🏬 闇市ブラックマーケット（資金調達 ＆ 返済・リスクメニュー）")
    
    col_shop1, col_shop2, col_shop3, col_shop4, col_shop5 = str_lit.columns(5)
    
    with col_shop1:
        str_lit.markdown("#### 🎫 鑑定アイテム")
        str_lit.write("真贋や呪いを見破るチケット。")
        if str_lit.button("鑑定券購入 (100万G)"):
            if str_lit.session_state.player_money >= 100:
                str_lit.session_state.player_money -= 100
                str_lit.session_state.appraisal_tickets += 1
                str_lit.success("鑑定チケットを1枚補充しました。")
                str_lit.rerun()
            else:
                str_lit.error("資金が足りません！")

    with col_shop2:
        str_lit.markdown("#### 🕵️ 闇バイト")
        jobs_left = 2 - str_lit.session_state.get("part_time_jobs_today", 0)
        str_lit.write(f"安全に稼ぐ（本日残り: {jobs_left}回）")
        if str_lit.button("闇バイト (+150万G)"):
            if str_lit.session_state.get("part_time_jobs_today", 0) < 2:
                str_lit.session_state.player_money += 150
                str_lit.session_state.part_time_jobs_today = str_lit.session_state.get("part_time_jobs_today", 0) + 1
                str_lit.success("裏仕事を完遂し、150万Gを手に入れました。")
                str_lit.rerun()
            else:
                str_lit.error("本日の闇バイト回数制限（2回）に達しました！日が変わると回復します。")

    with col_shop3:
        str_lit.markdown("#### 💳 闇金の借入")
        str_lit.write("今すぐ500万G得るが利息が発生。")
        if str_lit.button("闇金から借金 (+500万G)"):
            str_lit.session_state.player_money += 500
            str_lit.session_state.debt += 500
            str_lit.warning("⚠️ 闇金から500万Gを借り入れました。毎ターン利息が膨らみます！")
            str_lit.rerun()

    with col_shop4:
        str_lit.markdown("#### 💰 借金返済")
        str_lit.write("借金を500万Gずつ返済する。")
        if str_lit.button("借金を500万G返済"):
            if str_lit.session_state.debt > 0:
                repay_amount = min(500, str_lit.session_state.debt)
                if str_lit.session_state.player_money >= repay_amount:
                    str_lit.session_state.player_money -= repay_amount
                    str_lit.session_state.debt -= repay_amount
                    str_lit.success(f"💳 借金を {repay_amount}万G 返済しました！ 残り借金: {str_lit.session_state.debt}万G")
                    str_lit.rerun()
                else:
                    str_lit.error("返済する資金が足りません！")
            else:
                str_lit.info("現在、返済すべき借金はありません。")

    with col_shop5:
        str_lit.markdown("#### 🧪 違法人体実験")
        str_lit.write("【ハイリスク】40%大金、60%所持金半減。")
        if str_lit.button("実験台になる"):
            if random.random() < 0.40:
                str_lit.session_state.player_money += 600
                str_lit.balloons()
                str_lit.success("✨ 実験成功！ 600万Gの報酬を獲得！")
            else:
                loss = int(str_lit.session_state.player_money * 0.5)
                str_lit.session_state.player_money -= loss
                str_lit.error(f"💥 実験の副作用で精神を病み、資金が {loss}万G 消失しました...")
            str_lit.rerun()

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
    str_lit.subheader(f"📖 レリック・コレクション全集（全{len(MASTER_ITEMS)}種コンプリート状況）")
    str_lit.write("※一度でもオークションで落札・獲得したアイテムは、売却しても図鑑に記録され続けます。")
    cols = str_lit.columns(3)
    
    unlocked_ids = str_lit.session_state.unlocked_collection

    for idx, item in enumerate(MASTER_ITEMS):
        with cols[idx % 3]:
            if item["id"] in unlocked_ids:
                str_lit.image(item["image_url"], caption=item["name"], use_container_width=True)
                str_lit.caption(f"真価: {item['true_value']}万G | {item['category']} (入手済✨)")
            else:
                str_lit.markdown(f"### 🔒 {item['name']}")
                str_lit.caption("オークションで獲得すると解放されます。")
