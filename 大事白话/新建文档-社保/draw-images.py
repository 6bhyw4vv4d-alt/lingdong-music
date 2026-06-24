from pathlib import Path
import math
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "output"
WIDTH = 1080
HEIGHT = 1440
PAD = 62
INK = (22, 22, 22)
PAPER = (255, 253, 245)
WHITE = (255, 255, 255)
MUTED = (82, 74, 64)


CARDS = [
    {
        "tag": "总览",
        "title": "一生社保闯关图",
        "subtitle": "别先背比例，先看人生什么时候会用到社保。",
        "quote": "社保不是工资条上的一行扣款，而是一套遇事能用的基础工具。",
        "explain": "这组图按出生、上学、入职、看病、生育、工伤、失业、换城、自由职业、退休、失能照护的顺序讲。全国讲规则，各地看细则。",
        "panels": [
            ("是什么", "五险先分清", "养老、医疗、失业、工伤、生育属于社会保险；住房公积金是住房相关制度，不是社保本身。"),
            ("怎么用", "遇到事再找对应险种", "看病找医保，生育看生育待遇，受伤走工伤，失业查失业保险，退休看养老记录。"),
            ("注意事项", "别把外地经验当本地规则", "缴费基数、报销比例、津贴标准、办理时限都可能按地区调整。"),
            ("讲法", "按人生顺序最容易听懂", "先讲人会遇到什么事，再讲哪项社保上场，比直接讲政策条文更清楚。"),
        ],
        "takeaway": "介绍社保，先讲它解决什么问题，再讲怎么查、怎么用、哪里要看本地政策。",
        "color": ("#ffd166", "#f9a03f", "#ffe9a9"),
        "role": "讲解员",
    },
    {
        "tag": "第 1 站",
        "title": "出生、上学：先把医保上车",
        "subtitle": "孩子、学生、未就业居民，通常先接触城乡居民医保。",
        "quote": "居民医保像一张基础门票：平时参保，生病时才有机会按规则结算。",
        "explain": "居民医保多按年缴费，孩子看户籍地、居住地或学校所在地政策。别等生病住院了，才想起这张“门票”还没买。",
        "panels": [
            ("是什么", "未就业人群的基础医保", "没参加职工医保时，孩子、学生、未就业居民常通过城乡居民医保获得基本医疗保障。"),
            ("怎么用", "就医先看四件事", "医院药店是否定点，费用是否进目录，有没有起付线，报销比例和封顶线怎么定。"),
            ("注意事项", "集中缴费期别错过", "不少地区有固定参保缴费期，错过后可能影响待遇等待期。"),
            ("举个例子", "不要重复参保", "已经有职工医保，又交居民医保，很多情况下不能重复报销。身份变化时先问怎么接。"),
        ],
        "takeaway": "居民医保不是“有病再买”的临时票，参保地、缴费期和待遇等待期都要提前确认。",
        "color": ("#a8dadc", "#74c0c3", "#e3f6f5"),
        "role": "小保",
    },
    {
        "tag": "第 2 站",
        "title": "毕业入职：五险正式登场",
        "subtitle": "有了劳动关系，职工社保就是单位和个人都要面对的法定事项。",
        "quote": "签了劳动合同，社保不是公司福利，是基本配置。",
        "explain": "职工养老、医疗、失业通常由单位和个人共同缴；工伤保险主要由单位缴。生育保险和职工医保合并实施后，经办更统一。",
        "panels": [
            ("是什么", "职工社保就是常说的五险", "养老管退休，医疗管看病，失业管过渡保障，工伤管工作相关伤害，生育管生育相关待遇。"),
            ("怎么用", "入职后先查参保记录", "通过当地人社、医保平台或政务服务 App，看有没有按时参保、参保地是否正确。"),
            ("注意事项", "试用期也应依法参保", "不要接受“多发点现金、不交社保”的安排，短期多拿可能换来长期风险。"),
            ("举个例子", "工资条只显示一部分", "个人缴费会扣工资，单位缴费不进到手工资，但会进入相关账户和基金记录。"),
        ],
        "takeaway": "入职别只看工资，先确认社保有没有缴、按什么基数缴、参保地对不对。",
        "color": ("#ffb4a2", "#fb6f5b", "#ffe3d8"),
        "role": "新人",
    },
    {
        "tag": "第 3 站",
        "title": "每月工资条：社保费从哪来",
        "subtitle": "缴费基数像一把尺子，会影响现在扣多少，也会影响一些未来权益。",
        "quote": "看工资条，别只看扣了多少钱，还要看按什么基数扣。",
        "explain": "缴费基数一般和本人上年度工资、当地社会平均工资、当地上下限有关。不同城市工资水平不同，上下限也会不同。",
        "panels": [
            ("是什么", "缴费基数是计算尺子", "同样费率下，基数越高，个人和单位缴费金额越高，部分待遇记录也会更扎实。"),
            ("怎么用", "定期查个人权益记录", "重点看有没有漏缴，缴费基数是否明显异常，参保地是否和实际情况一致。"),
            ("注意事项", "别只听“公司都这样”", "不同年度、城市、单位用工情况都可能不一样，发现问题要尽早问清。"),
            ("举个例子", "月薪一万却按低基数缴", "短期看个人少扣钱，但医保、生育、养老金等权益可能受到影响。"),
        ],
        "takeaway": "缴费基数不是小数字，它连接现在的工资条，也连接以后的待遇账。",
        "color": ("#caffbf", "#73d673", "#edffe9"),
        "role": "工资条",
    },
    {
        "tag": "第 4 站",
        "title": "生病看医生：医保怎么报",
        "subtitle": "医保不是花多少报多少，而是按规则结算。",
        "quote": "医保像菜单：菜单内按规则结算，菜单外通常自己付。",
        "explain": "讲医保先讲五个词：定点医药机构、医保目录、起付线、报销比例、封顶线。门诊、住院、慢特病、异地就医规则也会不同。",
        "panels": [
            ("是什么", "医保管符合规则的医疗费用", "不是所有医院、所有药品、所有项目都能按医保报销。"),
            ("怎么用", "看病前先查定点和目录", "住院或大额治疗前，问清哪些能医保结算，哪些属于自费。"),
            ("注意事项", "异地就医先查备案", "跨省就医要问需不需要备案、去哪家医院、按哪里规则结算、失败后怎么报销。"),
            ("举个例子", "不要只问能不能报", "更准确的问法是：在哪里看、报什么项目、按什么比例、有没有封顶线。"),
        ],
        "takeaway": "医保报销要把地点、目录、门槛、比例一起看，不能只听一句“能报”。",
        "color": ("#bde0fe", "#5aa9e6", "#eaf6ff"),
        "role": "医保卡",
    },
    {
        "tag": "第 5 站",
        "title": "生育阶段：不是只有住院费",
        "subtitle": "生育待遇通常涉及医疗费用和生育津贴。",
        "quote": "柜台合在一起办了，但生育相关待遇仍然按规定保障。",
        "explain": "生育保险和职工基本医保合并实施后，经办更统一。具体能报什么、津贴怎么算、材料何时交，仍要看参保地规则。",
        "panels": [
            ("是什么", "两类待遇要分开看", "一类是产检、分娩、计划生育等医疗费用；一类是生育津贴。"),
            ("怎么用", "怀孕前后先问四件事", "连续缴费多久，产检分娩怎么结算，津贴谁申请发给谁，需要哪些材料。"),
            ("注意事项", "别照搬外地生育津贴", "同叫生育津贴，计算基数、发放路径、材料要求、产假天数都可能不同。"),
            ("举个例子", "男职工也别完全不看", "配偶未就业、护理假、陪产假等事项，各地规定不一样。"),
        ],
        "takeaway": "生育待遇最怕临到用时才问，准备阶段就要查参保地规则。",
        "color": ("#ffc8dd", "#f06292", "#fff0f6"),
        "role": "准爸妈",
    },
    {
        "tag": "第 6 站",
        "title": "工作受伤：工伤保险出场",
        "subtitle": "工伤保险看流程，也看证据。",
        "quote": "先救治，再留证，再按流程认定，别只等一句口头承诺。",
        "explain": "工伤判断常看工作时间、工作场所、工作原因。上下班途中交通事故、出差、职业病等场景，还要按具体规则认定。",
        "panels": [
            ("是什么", "工作相关伤害的保障", "用人单位按规定参加，职工发生符合条件的事故伤害或职业病时，按流程申请待遇。"),
            ("怎么用", "三步走", "先治疗；再留诊断、事故经过、考勤、聊天记录等证据；再走认定、鉴定、待遇核定。"),
            ("注意事项", "别把“算不算”讲死", "工伤要依法认定，材料散、时间拖、劳动关系说不清，都会影响结果。"),
            ("举个例子", "岗位操作受伤更接近工伤逻辑", "下班后个人活动受伤就不同。具体仍要看事实和认定结果。"),
        ],
        "takeaway": "工伤不是先算赔多少钱，而是先把救治、证据和认定流程走对。",
        "color": ("#f4d35e", "#ee964b", "#fff4c7"),
        "role": "安全帽",
    },
    {
        "tag": "第 7 站",
        "title": "失业阶段：不是离职就能领",
        "subtitle": "失业保险是符合条件时的过渡保障。",
        "quote": "主动辞职、被裁、合同到期，后面待遇判断可能不一样。",
        "explain": "一般要看缴费是否满规定期限，是否非本人意愿中断就业，是否办理失业登记并有求职要求。",
        "panels": [
            ("是什么", "失业后的过渡保障", "不是所有离职都有失业金，要先看参保记录和离职原因。"),
            ("怎么用", "离职后按当地流程申领", "符合条件的，可线上或线下申请；还可能涉及医保待遇、职业培训、就业服务。"),
            ("注意事项", "离职证明别随便写", "材料写主动辞职，和实际被单位解除劳动合同，后续判断可能不同。"),
            ("举个例子", "失业金没有全国统一金额", "标准和可领期限各地不同，宣传时不要写成全国一样。"),
        ],
        "takeaway": "失业保险看缴费、原因和登记，离职材料要和真实情况一致。",
        "color": ("#d0bfff", "#9775fa", "#f2edff"),
        "role": "待业中",
    },
    {
        "tag": "第 8 站",
        "title": "换工作、换城市：社保别掉线",
        "subtitle": "换城市不是只搬行李，社保关系也要接上。",
        "quote": "人搬家，水电网要迁移；换城市，社保记录也要接得上。",
        "explain": "养老、医保、失业、工伤、生育背后有不同经办系统和地方规则。跨城前最好先问清停缴、起缴、接续和异地就医。",
        "panels": [
            ("是什么", "社保关系接续问题", "换城市后，原地记录和新地参保要接起来，不能只看新公司有没有发工资。"),
            ("怎么用", "换城前问四件事", "原城市何时停，新城市何时缴，医保有没有等待期，养老关系需不需要转移接续。"),
            ("注意事项", "地方资格要分开看", "购房、落户、车牌、子女入学等连续缴费要求，多是地方政策，不是全国统一待遇。"),
            ("举个例子", "长期跨城要提前看退休地", "不要临近退休才发现年限、参保地、户籍地之间还有条件。"),
        ],
        "takeaway": "换城市前先查会不会断、怎么接、哪些本地资格受影响。",
        "color": ("#9bf6ff", "#48cae4", "#e9fcff"),
        "role": "搬家人",
    },
    {
        "tag": "第 9 站",
        "title": "自由职业：自己当人事",
        "subtitle": "没有单位，也要自己盯参保和缴费。",
        "quote": "自由职业不是没有社保，而是自己要把参保这件事管起来。",
        "explain": "灵活就业人员通常可按当地政策参加职工养老、职工医保；也可根据自身条件参加城乡居民养老、城乡居民医保。",
        "panels": [
            ("是什么", "两条常见路径", "一条是灵活就业职工社保，缴费压力通常更高；一条是居民社保，待遇按居民制度理解。"),
            ("怎么用", "先算三笔账", "现金流能不能承受，看病和生育需求高不高，以后是否可能回单位就业。"),
            ("注意事项", "警惕违规挂靠代缴", "看似帮你交社保，实际可能带来劳动关系、骗保、补缴和待遇风险。"),
            ("举个例子", "把缴费日写进日历", "自由职业最怕忘记缴费，断缴可能影响医保待遇和连续性。"),
        ],
        "takeaway": "自由职业参保要看预算、健康需求和长期规划，别把代缴挂靠当捷径。",
        "color": ("#ffd6a5", "#ff9f1c", "#fff2df"),
        "role": "自由人",
    },
    {
        "tag": "第 10 站",
        "title": "退休：养老保险兑现长期积累",
        "display_title": "退休：养老保险\n兑现长期积累",
        "subtitle": "养老保险看长期记录，不看某一个月。",
        "quote": "养老金不是临退休那一下决定的，是多年缴费记录慢慢攒出来的。",
        "explain": "2025 年起实施渐进式延迟法定退休年龄。2030 年起，职工按月领取基本养老金最低缴费年限由 15 年逐步提高至 20 年。",
        "panels": [
            ("是什么", "养老保险是一笔长期账", "缴费年限、缴费基数、个人账户、退休年龄、退休地和计发规则都会影响结果。"),
            ("怎么用", "临近退休提前查四件事", "法定退休年龄、累计缴费年限、养老关系和退休地、职工医保退休待遇所需年限。"),
            ("注意事项", "养老和医保退休别混着讲", "养老最低缴费年限有全国安排，职工医保退休待遇所需年限由地方规定。"),
            ("举个例子", "不够年限别自己猜", "达到年龄但年限不够的，按规定延长缴费等方式处理，以当时政策和经办结果为准。"),
        ],
        "takeaway": "退休要早查年龄表、年限、退休地和医保年限，别到最后一年才补课。",
        "color": ("#cdb4db", "#9d4edd", "#f7edff"),
        "role": "退休前",
    },
    {
        "tag": "第 11 站",
        "title": "失能照护：长期护理保险来了",
        "display_title": "失能照护：长期护理\n保险来了",
        "subtitle": "当人需要长期照护，医保之外还需要专门制度。",
        "quote": "去医院治病看医保，长期有人照护，看长期护理保险怎么落地。",
        "explain": "2026 年国家医保局等部门印发实施方案，明确用 3 年左右时间基本建立长期护理保险制度，保障长期护理基本需求。",
        "panels": [
            ("是什么", "失能照护的基础保障", "它主要管符合规定的长期护理基本服务费用，不是普通看病报销。"),
            ("怎么用", "先参保，再评估", "一般要按规定参保缴费，失能状态长期持续，并经过评估认定。起步阶段重点保障重度失能人员。"),
            ("注意事项", "不是人人立刻领钱", "各地实施时间、参保范围、评估流程、待遇标准会逐步细化。"),
            ("举个例子", "基金主要买服务", "机构护理、居家护理、社区护理等服务按规定支付，原则上不直接发现金。"),
        ],
        "takeaway": "长期护理保险正在落地，具体能不能用、怎么评估、怎么结算，要看当地实施方案。",
        "color": ("#b8f2e6", "#00b4d8", "#effffb"),
        "role": "照护",
    },
    {
        "tag": "地区差异",
        "title": "同叫社保，各地像不同套餐",
        "subtitle": "全国有共同框架，地方有具体参数。",
        "quote": "同一类社保问题，换个城市，答案可能就变了。",
        "explain": "社保的底层制度有全国共同规则，但缴费、待遇、办理、附加资格经常由统筹地区细化。",
        "panels": [
            ("是什么", "地方参数不同", "缴费基数上下限、费率、医保个人账户、门诊住院报销、生育津贴、失业金等都可能不同。"),
            ("怎么用", "先讲全国逻辑，再讲本地规则", "比如医保先讲定点、目录、起付线、比例、封顶线，再讲本地门诊住院怎么报。"),
        ],
        "map_items": ["缴费基数上下限", "社保费率", "医保个人账户", "门诊住院报销", "生育津贴口径", "失业金标准", "工伤补助标准", "长护险落地规则"],
        "takeaway": "报具体数字时，必须写清城市、年度、参保类型和官方来源。",
        "color": ("#b7e4c7", "#52b788", "#f0fff4"),
        "role": "地图",
    },
    {
        "tag": "收尾",
        "title": "社保避坑五问",
        "subtitle": "讲完一圈，让读者带走五个能马上自查的问题。",
        "quote": "听懂社保，不是背一堆比例，而是知道遇事先问哪几句。",
        "explain": "这页适合作为公众号结尾，也适合单独发给准备入职、换城市、自由职业、准备生育或临近退休的人。",
        "panels": [
            ("一问", "我现在是哪种参保？", "职工、灵活就业、居民，缴费和待遇逻辑不一样。"),
            ("二问", "单位按什么基数缴？", "按最低基数、实际工资，还是有漏缴断缴，都要查记录。"),
            ("三问", "医保在哪里能用？", "看定点、目录、异地备案和等待期，别只问“能不能报”。"),
            ("四问", "换城市会影响什么？", "社保接续、医保待遇、连续缴费、购房落户等资格要分开查。"),
            ("五问", "遇事找谁办？", "养老、失业、工伤看人社；医疗、生育看医保；缴费看税务。"),
            ("口径", "以最新官方通知为准", "2026-06-22 整理；个人权益以本人记录和当地经办结果为准。"),
        ],
        "takeaway": "平时按时参保、定期查记录，换身份或换城市前先问清规则。",
        "color": ("#f1fa8c", "#ffd43b", "#fffad1"),
        "role": "清单",
    },
]


def pick_font(candidates):
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
    return None


BOLD_FONT = pick_font([
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
])
REGULAR_FONT = pick_font([
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
])


def font(size, bold=False):
    path = BOLD_FONT if bold else REGULAR_FONT
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def hex_to_rgb(value):
    value = value.strip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def text_width(draw, text, fnt):
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw, text, fnt, max_width):
    lines = []
    for para in str(text).split("\n"):
        current = ""
        for ch in para:
            trial = current + ch
            if text_width(draw, trial, fnt) <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines or [""]


def draw_fit_text(draw, text, box, size, min_size, fill=INK, bold=False, line_gap=1.18, align="left", max_lines=None):
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    max_height = y2 - y1
    chosen = font(min_size, bold)
    chosen_lines = wrap_text(draw, text, chosen, max_width)
    chosen_line_h = int(min_size * line_gap)

    for candidate_size in range(size, min_size - 1, -2):
        fnt = font(candidate_size, bold)
        lines = wrap_text(draw, text, fnt, max_width)
        if max_lines and len(lines) > max_lines:
            continue
        line_h = int(candidate_size * line_gap)
        total_h = line_h * len(lines)
        if total_h <= max_height:
            chosen = fnt
            chosen_lines = lines
            chosen_line_h = line_h
            break

    max_allowed = max(1, max_height // max(chosen_line_h, 1))
    if max_lines:
        max_allowed = min(max_allowed, max_lines)
    lines = chosen_lines[:max_allowed]
    if len(chosen_lines) > max_allowed and lines:
        while lines[-1] and text_width(draw, lines[-1] + "…", chosen) > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"

    y = y1
    for line in lines:
        if align == "center":
            x = x1 + (max_width - text_width(draw, line, chosen)) / 2
        else:
            x = x1
        draw.text((x, y), line, font=chosen, fill=fill)
        y += chosen_line_h
    return y


def rounded(draw, xy, radius, fill, outline=INK, width=5, shadow=True, shadow_offset=(7, 7)):
    if shadow:
        sx1, sy1, sx2, sy2 = xy
        ox, oy = shadow_offset
        draw.rounded_rectangle((sx1 + ox, sy1 + oy, sx2 + ox, sy2 + oy), radius=radius, fill=(22, 22, 22, 45))
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def dashed_rect(draw, xy, radius=28, fill=None):
    x1, y1, x2, y2 = xy
    dash = 18
    gap = 10
    color = (22, 22, 22, 60)
    # Straight dashed border, rounded corners are suggested by gaps and the outer border.
    for x in range(x1 + radius, x2 - radius, dash + gap):
        draw.line((x, y1, min(x + dash, x2 - radius), y1), fill=color, width=3)
        draw.line((x, y2, min(x + dash, x2 - radius), y2), fill=color, width=3)
    for y in range(y1 + radius, y2 - radius, dash + gap):
        draw.line((x1, y, x1, min(y + dash, y2 - radius)), fill=color, width=3)
        draw.line((x2, y, x2, min(y + dash, y2 - radius)), fill=color, width=3)


def make_background(bg_a, bg_b):
    a = hex_to_rgb(bg_a)
    b = hex_to_rgb(bg_b)
    img = Image.new("RGB", (WIDTH, HEIGHT), a)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        draw.line((0, y, WIDTH, y), fill=mix(a, b, t), width=1)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((840, 35, 1035, 230), fill=(255, 255, 255, 96))
    for x in range(0, WIDTH, 48):
        for y in range(0, HEIGHT, 48):
            if (x + y) % 96 == 0:
                od.ellipse((x, y, x + 5, y + 5), fill=(22, 22, 22, 22))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def draw_badge(draw, text, x, y, accent):
    fnt = font(24, True)
    w = text_width(draw, text, fnt) + 68
    rounded(draw, (x, y, x + w, y + 54), 27, WHITE, width=4, shadow=True, shadow_offset=(5, 5))
    draw.ellipse((x + 16, y + 16, x + 36, y + 36), fill=accent, outline=INK, width=4)
    draw.text((x + 48, y + 12), text, font=fnt, fill=INK)


def draw_date_pill(draw):
    text = "社保生命周期漫画科普"
    fnt = font(18, True)
    w = text_width(draw, text, fnt) + 32
    x = WIDTH - PAD - w
    y = 56
    rounded(draw, (x, y, x + w, y + 48), 14, WHITE, width=4, shadow=True, shadow_offset=(5, 5))
    draw.text((x + 16, y + 10), text, font=fnt, fill=INK)


def draw_stars(draw):
    for idx in range(3):
        cx = 890 + idx * 34
        cy = 190 + (idx % 2) * 10
        points = [(cx, cy - 15), (cx + 15, cy), (cx, cy + 15), (cx - 15, cy)]
        draw.polygon(points, fill=WHITE, outline=INK)
        draw.line((cx, cy - 15, cx + 15, cy), fill=INK, width=4)


def draw_person(draw, x, y, accent):
    # x, y mark the center top of the figure.
    left = x - 85
    draw.ellipse((left + 42, y, left + 130, y + 88), fill=(255, 216, 168), outline=INK, width=5)
    draw.rounded_rectangle((left + 50, y - 8, left + 122, y + 34), radius=24, fill=(43, 33, 24), outline=INK, width=5)
    draw.ellipse((left + 66, y + 38, left + 76, y + 52), fill=INK)
    draw.ellipse((left + 98, y + 38, left + 108, y + 52), fill=INK)
    draw.arc((left + 78, y + 56, left + 104, y + 76), start=0, end=180, fill=INK, width=4)
    draw.rounded_rectangle((left + 30, y + 88, left + 142, y + 198), radius=28, fill=accent, outline=INK, width=5)
    draw.line((left + 29, y + 118, left + 0, y + 142), fill=INK, width=15)
    draw.line((left + 142, y + 118, left + 172, y + 142), fill=INK, width=15)
    draw.line((left + 52, y + 195, left + 52, y + 230), fill=INK, width=22)
    draw.line((left + 100, y + 195, left + 100, y + 230), fill=INK, width=22)
    draw.ellipse((left + 43, y + 220, left + 69, y + 238), fill=INK)
    draw.ellipse((left + 91, y + 220, left + 117, y + 238), fill=INK)


def draw_mascot_panel(draw, x, y, w, h, role, accent):
    rounded(draw, (x, y, x + w, y + h), 26, (255, 253, 242), width=5, shadow=True)
    role_fnt = font(18, True)
    role_w = text_width(draw, role, role_fnt) + 24
    draw.rounded_rectangle((x + 18, y + 16, x + 18 + role_w, y + 50), radius=17, fill=accent, outline=INK, width=3)
    draw.text((x + 30, y + 22), role, font=role_fnt, fill=INK)
    draw_person(draw, x + w // 2, y + 76, accent)


def draw_speech_panel(draw, x, y, w, h, quote, explain):
    tail = [(x - 4, y + h - 105), (x - 38, y + h - 66), (x - 4, y + h - 30)]
    draw.polygon([(p[0] + 7, p[1] + 7) for p in tail], fill=(22, 22, 22, 45))
    draw.polygon(tail, fill=PAPER, outline=INK)
    draw.line((x - 4, y + h - 105, x - 4, y + h - 30), fill=PAPER, width=8)
    rounded(draw, (x, y, x + w, y + h), 28, PAPER, width=5, shadow=True)
    draw_fit_text(draw, quote, (x + 30, y + 26, x + w - 30, y + 155), 44, 33, fill=INK, bold=True, line_gap=1.16, max_lines=3)
    draw_fit_text(draw, explain, (x + 30, y + 170, x + w - 30, y + h - 24), 25, 19, fill=MUTED, bold=True, line_gap=1.36)


def draw_panel(draw, box, panel, accent, small=False):
    x1, y1, x2, y2 = box
    bg = (255, 255, 255) if not small else (255, 252, 232)
    rounded(draw, box, 24, bg, width=5, shadow=True, shadow_offset=(6, 6))
    kicker, title, body = panel
    kf = font(17 if not small else 15, True)
    kw = min(text_width(draw, kicker, kf) + 24, x2 - x1 - 28)
    draw.rounded_rectangle((x1 + 18, y1 + 17, x1 + 18 + kw, y1 + 47), radius=15, fill=(255, 255, 255), outline=INK, width=3)
    draw.text((x1 + 30, y1 + 22), kicker, font=kf, fill=INK)
    title_size = 30 if not small else 23
    body_size = 21 if not small else 17
    title_bottom = draw_fit_text(draw, title, (x1 + 22, y1 + 60, x2 - 22, y1 + 124), title_size, 20, fill=INK, bold=True, line_gap=1.12, max_lines=2)
    draw_fit_text(draw, body, (x1 + 22, max(title_bottom + 4, y1 + 112), x2 - 22, y2 - 18), body_size, 15, fill=(60, 53, 44), bold=True, line_gap=1.35)
    draw.ellipse((x2 - 28, y1 + 20, x2 - 13, y1 + 35), fill=accent, outline=INK, width=3)


def draw_map_panel(draw, box, items, accent):
    x1, y1, x2, y2 = box
    rounded(draw, box, 24, WHITE, width=5, shadow=True, shadow_offset=(6, 6))
    cols = 4
    gap = 12
    cell_w = (x2 - x1 - 44 - gap * (cols - 1)) // cols
    cell_h = 78
    start_x = x1 + 22
    start_y = y1 + 26
    for idx, item in enumerate(items):
        col = idx % cols
        row = idx // cols
        cx = start_x + col * (cell_w + gap)
        cy = start_y + row * (cell_h + 16)
        draw.rounded_rectangle((cx, cy, cx + cell_w, cy + cell_h), radius=16, fill=(255, 252, 232), outline=INK, width=3)
        draw_fit_text(draw, item, (cx + 8, cy + 14, cx + cell_w - 8, cy + cell_h - 8), 19, 15, fill=INK, bold=True, align="center", line_gap=1.16)
        draw.ellipse((cx + 8, cy + 8, cx + 20, cy + 20), fill=accent, outline=INK, width=2)


def draw_takeaway(draw, text, accent):
    x1, y1, x2, y2 = PAD, 1280, WIDTH - PAD, 1398
    rounded(draw, (x1, y1, x2, y2), 26, INK, outline=INK, width=5, shadow=False)
    label = "这一页记住"
    lf = font(21, True)
    lw = text_width(draw, label, lf) + 28
    draw.rounded_rectangle((x1 + 26, y1 + 35, x1 + 26 + lw, y1 + 74), radius=20, fill=accent, outline=WHITE, width=3)
    draw.text((x1 + 40, y1 + 42), label, font=lf, fill=INK)
    draw_fit_text(draw, text, (x1 + 190, y1 + 22, x2 - 26, y2 - 18), 24, 18, fill=WHITE, bold=True, line_gap=1.34)


def draw_page_number(draw, idx):
    x1, y1 = 976, 1198
    draw.ellipse((x1 + 5, y1 + 5, x1 + 75, y1 + 75), fill=(22, 22, 22, 45))
    draw.ellipse((x1, y1, x1 + 70, y1 + 70), fill=WHITE, outline=INK, width=4)
    label = f"{idx:02d}"
    fnt = font(24, True)
    tw = text_width(draw, label, fnt)
    draw.text((x1 + (70 - tw) / 2, y1 + 20), label, font=fnt, fill=INK)


def draw_panels(draw, card, accent):
    panels = card["panels"]
    area_x = PAD
    area_y = 738
    area_w = WIDTH - PAD * 2
    area_h = 520
    gap = 22
    col_w = (area_w - gap) // 2

    if "map_items" in card:
        row_h = 190
        draw_panel(draw, (area_x, area_y, area_x + col_w, area_y + row_h), panels[0], accent)
        draw_panel(draw, (area_x + col_w + gap, area_y, area_x + area_w, area_y + row_h), panels[1], accent)
        draw_map_panel(draw, (area_x, area_y + row_h + gap, area_x + area_w, area_y + area_h), card["map_items"], accent)
        return

    rows = math.ceil(len(panels) / 2)
    row_h = (area_h - gap * (rows - 1)) // rows
    small = len(panels) >= 6
    for idx, panel in enumerate(panels):
        col = idx % 2
        row = idx // 2
        x1 = area_x + col * (col_w + gap)
        y1 = area_y + row * (row_h + gap)
        draw_panel(draw, (x1, y1, x1 + col_w, y1 + row_h), panel, accent, small=small)


def slug(text):
    cleaned = re.sub(r"[：:，,。、“”\"']", "", text)
    cleaned = re.sub(r"\s+", "-", cleaned)
    return cleaned[:28]


def draw_card(card, idx):
    bg_a, accent_hex, bg_b = card["color"]
    accent = hex_to_rgb(accent_hex)
    img = make_background(bg_a, bg_b)
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=INK, width=5)
    dashed_rect(draw, (18, 18, WIDTH - 18, HEIGHT - 18))
    draw_stars(draw)
    draw_badge(draw, card["tag"], PAD, 56, accent)
    draw_date_pill(draw)

    title_text = card.get("display_title", card["title"])
    title_bottom = draw_fit_text(draw, title_text, (PAD, 126, 960, 288), 74, 54, fill=INK, bold=True, line_gap=1.0, max_lines=2)
    subtitle_y = max(300, title_bottom + 14)
    draw_fit_text(draw, card["subtitle"], (PAD, subtitle_y, 950, 374), 30, 22, fill=(45, 41, 36), bold=True, line_gap=1.28, max_lines=2)

    comic_y = 390
    draw_mascot_panel(draw, PAD, comic_y, 274, 320, card["role"], accent)
    draw_speech_panel(draw, 360, comic_y, 658, 320, card["quote"], card["explain"])

    draw_panels(draw, card, accent)
    draw_page_number(draw, idx)
    draw_takeaway(draw, card["takeaway"], accent)
    return img


def make_contact_sheet(paths):
    thumb_w = 270
    thumb_h = 360
    cols = 4
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (236, 229, 216))
    for idx, path in enumerate(paths):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w - 18, thumb_h - 18), Image.Resampling.LANCZOS)
        x = (idx % cols) * thumb_w + (thumb_w - img.width) // 2
        y = (idx // cols) * thumb_h + (thumb_h - img.height) // 2
        sheet.paste(img, (x, y))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "contact-sheet.png"
    sheet.save(out)
    return out


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for idx, card in enumerate(CARDS, start=1):
        img = draw_card(card, idx)
        filename = f"{idx:02d}-{slug(card['title'])}.png"
        out = IMAGES_DIR / filename
        img.save(out)
        generated.append(out)
        print(out)
    sheet = make_contact_sheet(generated)
    print(sheet)


if __name__ == "__main__":
    main()
