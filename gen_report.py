# -*- coding: utf-8 -*-
import json, base64, os, re
from collections import Counter

# ============================================================
# Load data
# ============================================================
msgs = []
with open('/Users/jiangtao/.wechat-insight/data/星城神仙小分队.jsonl') as f:
    for line in f:
        msgs.append(json.loads(line))
text_msgs = [m for m in msgs if m.get('msg_type') == 1]
non_text_count = len(msgs) - len(text_msgs)
total_all = len(msgs)
total_text = len(text_msgs)

# Stats
sender_counter = Counter()
for m in text_msgs:
    sender_counter[m.get('sender_name', '未知')] += 1
unique_senders = len(sender_counter)

dates = sorted(set(m['datetime'][:10] for m in text_msgs))
daily_counter = Counter()
for m in text_msgs:
    daily_counter[m['datetime'][:10]] += 1

# Active stars (>= 10)
stars_raw = [(n, c) for n, c in sender_counter.most_common(30) if c >= 10]

# Trend data (daily for weekly)
trend_data = [[d, daily_counter.get(d, 0)] for d in sorted(daily_counter.keys())]

# ============================================================
# QR code
# ============================================================
skill_dir = "/Users/jiangtao/.claude/skills/wechat-group-report-cc"
qr_path = os.path.join(skill_dir, "assets", "coffee-support-qr.jpg")
with open(qr_path, "rb") as f:
    qr_data = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"

# ============================================================
# Summary cards
# ============================================================
summary_cards = f"""
<div class="summary-card">
  <span class="summary-label">总消息数</span>
  <span class="summary-value">{total_all}</span>
</div>
<div class="summary-card">
  <span class="summary-label">文本消息</span>
  <span class="summary-value">{total_text}</span>
</div>
<div class="summary-card">
  <span class="summary-label">活跃参与人数</span>
  <span class="summary-value">{unique_senders}</span>
</div>
<div class="summary-card">
  <span class="summary-label">非文本消息</span>
  <span class="summary-value">{non_text_count}</span>
</div>
"""

# Trend card
trend_card = """
<div class="trend-card">
  <div class="trend-head">
    <span class="trend-title">发言时段分布</span>
    <span>按天统计</span>
  </div>
  <canvas id="trend" class="trend-canvas"></canvas>
  <div class="trend-note">消息量在 07/27 达到峰值（1232条），晚间至凌晨为群聊高频时段。</div>
</div>
"""

# Summary line
summary_line = """
<div class="summary-line">
  <span class="summary-line-label">高频情绪：</span>\U0001f525 调侃互损 \U0001fae3 两性八卦 \U0001f602 捧场起哄 \U0001f914 情感咨询 \U0001f373 生活分享
</div>
"""

# ============================================================
# Hot Topics
# ============================================================
hot_topics = """
<li>
  <span class="topic-title">\U0001f525 03年弟弟与98年姐姐：一天五次的姐弟恋传说</span>
  <span class="topic-act">第一幕：猛料引爆</span>
  <span class="topic-step">超级丹\U0001f497 抛出重磅八卦：和一个03年弟弟吃饭，对方吐槽姐弟恋"太色了顶不住"，每天五次、见面三天15次</span>
  <span class="topic-step">全场炸锅——峰哥从生理学角度认证"姐弟配合理"，沐沐、丑东西、摄影师纷纷加入吃瓜队列</span>
  <span class="topic-step">丑东西精准追问"这么饿吗"，摄影师质疑"天天四五次不可能"</span>
  <span class="topic-act">第二幕：角色代入</span>
  <span class="topic-step">拉金子的猴子 抛出"一晚上7次都有"的新鲜感理论，把讨论从个例拉向普遍规律</span>
  <span class="topic-step">后来发现当事人已经谈了一年多还是每天四五次，全场从质疑转为震惊</span>
  <span class="topic-step">话题持续发酵到第二天，脑壳炸直接劝超级丹"老公不行就休了"，掘炭仔帮腔"你老公被你榨干了"</span>
  <span class="topic-step">小辣椒顺势科普"一天五次，还没老就不行了"，九思从男性视角分析"可能前几次都没出"</span>
  <span class="topic-act">第三幕：食疗求救</span>
  <span class="topic-step">超级丹 认真发问"吃韭菜到底好用吗"，引爆新一轮食疗可行性讨论</span>
  <span class="topic-step">峰哥淡定回复"吃韭菜有用的话全是猛男了"，丑东西推荐蛇羹，H补刀"按吨吃可能有点用"</span>
  <span class="topic-step">掘炭仔总结"没啥用，要接受老公不行的事实"，拉金子的猴子补刀"吃伟哥也没用"</span>
  <span class="topic-step">齐齐大圣一锤定音"这没用那没用，剁了算了"，全场以哄笑收场</span>
  <div class="highlight-quote">
    <span class="highlight-text">"按生理强度来说，就应该姐弟配，比较合理"</span>
    <span class="highlight-author">— 峰哥-长沙卖房人</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：一条八卦从"太色了"一路滚到割以永治，群友用三天时间完成了从震惊、论证、劝分到放弃治疗的全套流程。表面上在帮超级丹找办法，实际上每个人都在借题发挥自己的两性观——韭菜不是重点，重点是大家聊得很爽。</span>
  <span class="topic-participants">主要参与者：超级丹\U0001f497、拉金子的猴子、九思、掘炭仔、峰哥-长沙卖房人、丑东西、齐齐大圣</span>
</li>

<li>
  <span class="topic-title">\U0001f494 前任图鉴：黄金、出轨、小三与九百克真爱</span>
  <span class="topic-act">第一幕：拉金子的猴子讲朋友的故事</span>
  <span class="topic-step">深夜话题从"前任格局"切入——拉金子的猴子分享好朋友的极品前任：给她买了900多克黄金（金价三四百时买的），送了一辆42万奥迪</span>
  <span class="topic-step">转折来了：这么"完美"的前任出轨多次，有小三小四小五，小三把怀孕5个月的女方从5楼推到3楼，孩子没了，医院住了三个月</span>
  <span class="topic-step">群友集体倒吸冷气——沐沐感叹"这是用钱能弥补的？"</span>
  <span class="topic-act">第二幕：这个前任又体面又不体面</span>
  <span class="topic-step">拉金子的猴子继续爆：分手后前任表弟送了一万块花篮，前任本人还给她转了5000块买化妆品外加888.88红包</span>
  <span class="topic-step">丑东西精准总结"这才是正常状态，门当户对很重要"，群友陷入"这个前任到底算好还是坏"的复杂情绪</span>
  <span class="topic-step">沐沐拉回现实"我前任和新欢都是天使"</span>
  <span class="topic-act">第三幕：猴子自己的故事</span>
  <span class="topic-step">话题滑向各自的前任——拉金子的猴子坦白前任想让她拿房子抵押给他，沐沐感慨"按你身边人这些例子，你还算幸运的"</span>
  <span class="topic-step">娄底抵押车二手车买卖 加入群聊，分享前任弯道差点撞人反嫌他烦的故事，拉金子的猴子感慨"不会吵不会发生正面冲突"</span>
  <span class="topic-step">话题在"互相付出"与"门当户对"之间兜了一圈，最后停在吃软饭的玩笑上</span>
  <div class="highlight-quote">
    <span class="highlight-text">"突然有一天，他就带着小三来到我朋友家里，小三也是怀孕了"</span>
    <span class="highlight-author">— 拉金子的猴子</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：一场从"别人家的黄金男友"急转直下到"被小三推下楼梯"的深夜故事会。拉金子的猴子用朋友和自己两代人的血泪史，给群友上了一堂"钱给到位不代表人靠谱"的情感公开课。群友们的表情在羡慕、震惊和庆幸之间反复横跳，最终集体决定吃点好的压压惊。</span>
  <span class="topic-participants">主要参与者：拉金子的猴子、沐沐不找对象、丑东西、娄底抵押车二手车买卖</span>
</li>

<li>
  <span class="topic-title">\U0001f9e0 "心情不好影响性致吗？"——超级丹的今日议题</span>
  <span class="topic-act">第一幕：问题抛出</span>
  <span class="topic-step">超级丹\U0001f497 因老公工作不顺、性致全无，发起灵魂拷问"心情不好会不会影响兴致"</span>
  <span class="topic-step">丑东西简短回答"会"，W补刀"你心情不好的时候，未必有兴致？"</span>
  <span class="topic-act">第二幕：九思的传奇发言</span>
  <span class="topic-step">九思发表长篇雄文：心情开心来一次、烦躁来一次、郁闷来一次、平静来一次——只有身体不支持，没有心情影响</span>
  <span class="topic-step">更搬出当年当小阳人"半死不活状态还跟女生开黑打吃鸡到凌晨、打完立刻登机"的故事</span>
  <span class="topic-step">不过很快补了一句"以上纯属吹牛"，齐齐大圣追问"登机去哪里、还回来吗"</span>
  <span class="topic-act">第三幕：男女思维碰撞</span>
  <span class="topic-step">超级丹代表女方阵营表态"心情影响所有，女孩子比较情绪化"</span>
  <span class="topic-step">W抛出灵魂追问"心情差的时候你老公在你旁边呼吸都是错吗"，超级丹承认那是不讲理</span>
  <span class="topic-step">话题以两性差异的调侃收场——没有结论，但每个人都站好了自己的队</span>
  <div class="highlight-quote">
    <span class="highlight-text">"只有身体不支持，没有心情影响，都是骗你的——宝宝今天太累了，下回补回来，都是虚假的"</span>
    <span class="highlight-author">— 九思</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：超级丹以亲身困境发起了一场关于男性心理的田野调查。九思用一篇半真半假的"阳人登机文学"把气氛从心理咨询拉到了传奇故事会。最终结论：男女确实不一样，但心情不好的时候对方连呼吸都是错这件事——不分性别。</span>
  <span class="topic-participants">主要参与者：超级丹\U0001f497、九思、W、丑东西、齐齐大圣</span>
</li>

<li>
  <span class="topic-title">\U0001f3b0 五万俩的男朋友：澳门赌王级男友横空出世</span>
  <span class="topic-act">第一幕：壕气出场</span>
  <span class="topic-step">群友 。（句号哥/姐）轻描淡写抛出"5万两个"的男友消费力，九思和掘炭仔同时惊呼"妈耶，是5万两个啊，不是5000"</span>
  <span class="topic-step">紧接着补刀："每个月还有一万给我打麻将的零花钱"——群友表示受到了亿点暴击</span>
  <span class="topic-act">第二幕：群友集体求收留</span>
  <span class="topic-step">九思大喊"我这一个月1800我真受不了了"，掘炭仔完美复制粘贴</span>
  <span class="topic-step">峰哥情商上线"能给大家发个红包我们去买眼药水吗"</span>
  <span class="topic-step">。淡定回应"早就不在群里发红包了，之前有个傻逼怼我"，峰哥火速表示"那个傻逼已经不在群里了"</span>
  <span class="topic-step">掘炭仔和脑壳炸组队复读"报告顶美，那个傻逼已经不在群里了"</span>
  <div class="highlight-quote">
    <span class="highlight-text">"我苏总要卖屁股了"</span>
    <span class="highlight-author">— 九思</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：句号哥/姐用两句话完成了本群本周最成功的凡尔赛——先是"5万两个"，再补一句"一万零花钱打麻将"，杀伤力拉满。九思和掘炭仔的双人复读式破防堪称标准跟风教材，而峰哥见风使舵的眼力见证明了他为什么能在长沙卖房。</span>
  <span class="topic-participants">主要参与者：。、九思、掘炭仔、峰哥-长沙卖房人、小苏爱吃糖</span>
</li>

<li>
  <span class="topic-title">\U0001f47b "我是男的，加我干啥"——樱桃小丸犊子的奇怪好友申请</span>
  <span class="topic-act">第一幕：深夜来客</span>
  <span class="topic-step">樱桃小丸犊子\U0001f352\U0001f471 一早发来"卧槽"——一个妹子突然加她微信，朋友圈全是性感照片，她一脸问号"我又不是男的"</span>
  <span class="topic-step">峰哥发表视觉评论"犹抱琵琶半遮面比较吸引人，每张图都露半个奶只会让人觉得低俗"</span>
  <span class="topic-step">齐齐大圣从男性视角补充"网上都很大，现实中又大又好看少见"</span>
  <span class="topic-act">第二幕：群友职业分析</span>
  <span class="topic-step">拉金子的猴子一针见血"也有可能是做那个的，妈咪吧"</span>
  <span class="topic-step">沐沐不找对象诚实发言"我要是男的，身材真这么好，我是愿意消费的"</span>
  <span class="topic-step">九思直接定性"这种一般是个人，鸡，卖的"</span>
  <span class="topic-step">拉金子的猴子接梗"10个男人只有9个不想带"，话题从黄色交友滑向安全性行为科普</span>
  <span class="topic-act">第三幕：浪子的前女友</span>
  <span class="topic-step">梅溪湖-浪子\U0001f3f8 突然插入："昨天刷到前前任的朋友圈，很多被钓成翘嘴了"</span>
  <span class="topic-step">丑东西光速接话"可以推一下吗，没别的，单纯想认识一下"</span>
  <span class="topic-step">九思调侃浪子"吃那么好，你还分手"——全场再次歪楼</span>
  <div class="highlight-quote">
    <span class="highlight-text">"其实犹抱琵琶半遮面是比较吸引人的，这种每张图都露半个奶的，只会让人觉得低俗"</span>
    <span class="highlight-author">— 峰哥-长沙卖房人</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：樱桃小丸犊子的一张好友申请截图，演变成了一场关于"美女加错人"的群聊侦探剧。从职业鉴定到安全性教育再到浪子前女友突然出场——话题走向堪比悬疑片。丑东西的"单纯想认识一下"堪称本周最不单纯的一句话。</span>
  <span class="topic-participants">主要参与者：樱桃小丸犊子\U0001f352\U0001f471、拉金子的猴子、峰哥-长沙卖房人、九思、沐沐不找对象、梅溪湖-浪子\U0001f3f8、丑东西</span>
</li>

<li>
  <span class="topic-title">\U0001f373 超级丹的厨房：从排骨到榴莲的驯夫记</span>
  <span class="topic-act">第一幕：排骨难题</span>
  <span class="topic-step">超级丹\U0001f497 日常买菜吐槽"老公天天想吃排骨，每次都要炖一个小时"</span>
  <span class="topic-step">拉金子的猴子光速接梗"老公天天想要咋办"，小苏爱吃糖完美复读</span>
  <span class="topic-step">齐齐大圣称赞"胃口好，精力也好"，超级丹羞涩承认"画风逐渐变态了"</span>
  <span class="topic-step">\U0001f49b the first 发出灵魂之问"这个是黄色群嘛"</span>
  <span class="topic-act">第二幕：榴莲外交</span>
  <span class="topic-step">几天后超级丹更新：上次生气对象用50个榴莲哄好的，截止今天买了18个还差32</span>
  <span class="topic-step">拉金子的猴子建议"尝试各种品种的榴莲口感"，并透露自己想去马来西亚榴莲园的梦想</span>
  <span class="topic-step">超级丹67块钱买的榴莲被齐齐大圣夸"好好看"，群友隔着屏幕感受到了金钱的味道</span>
  <div class="highlight-quote">
    <span class="highlight-text">"我上次生气，对象用50个榴莲哄好的——截止今天买18个还差32"</span>
    <span class="highlight-author">— 超级丹\U0001f497</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：超级丹把日常买菜硬是聊成了群内连续剧——排骨是引子，榴莲是高潮。50个榴莲的哄人KPI比大多数人的年终目标还具体。而\U0001f49b the first 那句"这个是黄色群嘛"可能是本周最诚实的提问，只可惜没人正经回答他。</span>
  <span class="topic-participants">主要参与者：超级丹\U0001f497、拉金子的猴子、齐齐大圣、小苏爱吃糖、\U0001f49b the first</span>
</li>

<li>
  <span class="topic-title">\U0001f491 九思相亲记：奶奶安排的"95后"神秘对象</span>
  <span class="topic-act">第一幕：奶奶登场</span>
  <span class="topic-step">九思在群里透露奶奶要给他安排相亲，群友瞬间来劲——掘炭仔起哄"给你相个大姨嘛"</span>
  <span class="topic-step">九思实况转播：女生在问工作，媒人问他奶奶，奶奶再问他，层层传递的古典相亲模式</span>
  <span class="topic-act">第二幕：群友在线助攻</span>
  <span class="topic-step">齐齐大圣叮嘱"别说漏嘴了"，超级丹八卦"姐姐真跑啦？"</span>
  <span class="topic-step">掘炭仔传授秘诀"要搞饥饿营销噻，专注质量"</span>
  <span class="topic-step">九思透露对方95年的，群友表示妹子年龄合适，期待后续发展</span>
  <span class="topic-step">然而到周末也没后续进展——看来还在奶奶和媒人的信息高速公路上一站一站传递</span>
  <div class="highlight-quote">
    <span class="highlight-text">"媒人问我奶奶，我奶奶问我……我问心无愧，不怕"</span>
    <span class="highlight-author">— 九思</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：九思以一己之力把中国传统相亲流程做了全透明直播——从媒人到奶奶再到本人，每个环节都不落下。掘炭仔的"饥饿营销"建议堪称群友金句，不过以九思在群里的发言风格，不知道奶奶知道他平时都在聊什么之后，还让不让媒人继续推微信。</span>
  <span class="topic-participants">主要参与者：九思、掘炭仔、齐齐大圣、超级丹\U0001f497</span>
</li>

<li>
  <span class="topic-title">\U0001f3b2 跑得快与红中：群友的麻将焦虑症</span>
  <span class="topic-act">第一幕：深夜牌瘾</span>
  <span class="topic-step">Mo 深夜寂寞发问"有没有打跑得快的，太无聊了"，"5毛一分娱乐娱乐"</span>
  <span class="topic-step">几天后再次出现"我好想打红中，找不到人咋办，怎么一块钱的都没人玩"</span>
  <span class="topic-act">第二幕：日常麻将局</span>
  <span class="topic-step">笃定加入群聊后也问"有木有铁道学院这边的"，被拉金子的猴子回以意味深长的表情</span>
  <span class="topic-step">笃定惦记着鱼生局"啥时候吃鱼生"，拉金子的猴子答应"下个月回来"</span>
  <span class="topic-step">笃定开始畅想"鱼生+生腌，一次爽嗨"</span>
  <span class="topic-act">第三幕：日常小确幸</span>
  <span class="topic-step">小苏爱吃糖晒出窗边风景，拉金子的猴子自嘲"猴子是乡里别，没见过这么好的风景"</span>
  <span class="topic-step">钟兆松精准定位到农业大学对面，长沙真的小</span>
  <span class="topic-step">峰哥组织溯溪活动，"男生已满，还可来一个女生"，群内社交生态活络</span>
  <div class="highlight-quote">
    <span class="highlight-text">"鱼生+生腌，一次爽嗨"</span>
    <span class="highlight-author">— 笃定</span>
  </div>
  <span class="ai-note">\U0001f4ac AI 锐评：Mo 用一周时间持续表达了同一个诉求——想打牌。从跑得快到红中，从五毛到一块，跨度不大但执念很深。群友的麻将热情明显不如两性话题高涨，但鱼生约饭的响应率还算可观。建议拉金子的猴子和笃定尽快落实鱼生局，给群里增加一个美食话题分支。</span>
  <span class="topic-participants">主要参与者：Mo、笃定、拉金子的猴子、小苏爱吃糖、峰哥-长沙卖房人</span>
</li>
"""

# ============================================================
# Active Stars HTML
# ============================================================
star_profiles = {
    '拉金子的猴子': ('拉金子的猴子', 827,
        '本周期当之无愧的话量女王——800多条发言让她稳坐C位。从深夜情感故事会到八卦现场解说，从榴莲建议到前任经济学分析，猴子是群聊的活火山口：别人还在酝酿措辞她已经发了三条。叙事节奏堪比说书人，一个"朋友的故事"能讲出三幕反转，让人怀疑这是朋友的素材还是她的编剧天赋。',
        ['话题点火人', '故事女王', '八卦发动机']),
    '超级丹💗': ('超级丹💗', 293,
        '群聊女主角没跑了。本周的每一次大话题几乎都由她引爆——从"一天五次"的姐弟恋八卦到"心情不好影响性致"的社会学调查，从67块的榴莲炫富到50个榴莲的哄人KPI。超级丹的聊天风格是"抛出一个钩子、退后一步看大家反应"，把日常活生生聊成了群内连续剧。',
        ['话题女王', '剧情推动者', '榴莲推广大使']),
    '掘炭仔': ('掘炭仔', 268,
        '群里的捧哏天花板。掘炭仔不负责发起话题，但他负责让话题变得更离谱——"给你老公补补""休了吧""搞饥饿营销"每句话都在给对话加温。复读功力一流，九思说什么他接什么，是那种你不想跟他当对手、但绝对想在群里拥有他的队友。',
        ['捧哏王', '节奏助推器', '复读机艺术家']),
    '九思': ('九思', 243,
        '本周金句贡献者。"只有身体不支持，没有心情影响"这篇小作文让他一战封神，虽然结尾补了句"纯属吹牛"但群友已经笑到手抖。相亲直播间的男主角，一边被奶奶安排95后妹子、一边在群里大聊两性话题——人设反差拉满。偶尔会突然煽情，但煽完立刻自嘲救场。',
        ['金句制造机', '反差萌', '理论派选手']),
    '齐齐大圣': ('齐齐大圣', 233,
        '群聊气氛组核心成员。不负责生产深度内容，但负责在最冷的时候把场子烘热——"割了剁了吧""你变了""猴子不理人""下午好大家吃屎了没有"。像是群聊的恒温器，不管话题走到哪，她都能找到自己的位置补一刀或发个表情。存在感拉满，信息密度另说。',
        ['气氛泵', '暖场手', '话题跟屁虫']),
    '丑东西': ('丑东西', 163,
        '群里的冷面笑匠——话不多但每句都在点上，擅长一针见血的短评和假装正经的钓鱼。"可以推一下吗，没别的，单纯想认识一下"堪称本周最佳演技。从河西烧烤问到前任八卦，丑东西的存在感来自于恰到好处的捧眼和偶尔假装天真的毒舌。',
        ['冷面笑匠', '精准补刀', '钓鱼大师']),
    'Mo': ('Mo', 141,
        '本周最执着的牌友。"能不能打牌""找不到人咋办"以一己之力撑起了群聊的麻将板块。虽然大家的响应度不高但他从未放弃。同时也是"一天五次"话题的积极参与者——"我也是01年的弟弟，一晚上五次我也可以的"——用自嘲化解了一切尴尬。',
        ['牌瘾少年', '气氛组', '自我推销艺术家']),
    '沐沐不找对象': ('沐沐不找对象', 95,
        '群内理智担当。当大家都在吃瓜起哄的时候，沐沐负责拉回地面——"都掉了一胎进医院了，这是用钱能弥补的？"犀利但不刻薄。偶尔诚实得可爱："我要是男的，身材真这么好，我是愿意消费的"——这种直球坦率在全是弯弯绕绕的群聊里反而是一股清流。',
        ['理性担当', '直球选手', '人间清醒']),
    '脑壳炸（脑壳昏天字号小弟）': ('脑壳炸', 97,
        '简单粗暴的表达风格——"休了吧"三个字就能引发一场讨论。擅长简短有力的断言式发言，复读能力与掘炭仔不分伯仲。虽然是天字号小弟但发言风格毫无小弟的卑微感，反而像个躲在屏幕后面随时输出暴论的世外高人。',
        ['暴论输出机', '简单粗暴', '复读协奏者']),
    '樱桃小丸犊子🍒👧': ('樱桃小丸', 88,
        '本周的"话题引信"。一张好友申请截图引发了群内长达半天的大讨论。平时发言不算高频，但只要她一开口就会带出一个完整的故事线。"卧槽"两字开头、图片佐证、群体推理收尾——这是典型的樱桃小丸犊子式聊天模式。',
        ['话题引信', '故事开头王', '推波助澜']),
    '娄底抵押车二手车买卖': ('娄底抵押车', 85,
        '前任话题的黄金配角。用亲身经历为拉金子的猴子的故事会提供了一手佐证——从弯道差点撞人到分手的琐碎日常，为深夜的emo氛围添砖加瓦。白天聊的是正经的二手车生意，晚上参与的是不正经的前任吐槽大会。',
        ['前任故事王', '跨界选手', '深夜emo']),
    '笃定': ('笃定', 81,
        '本周后半段才登场但存在感不低。一上来就展现了精准的社交嗅觉——问地域找组织、约鱼生局、参与两性话题讨论。典型的"社牛型新人"：先抛出几个钩子看看哪个话题能接住，很快就和拉金子的猴子敲定了鱼生+生腌之约。',
        ['社交雷达', '约饭达人', '新人王']),
    '峰哥-长沙卖房人': ('峰哥', 51,
        '群聊的定海神针——发言不多但每次都踩在点上。无论是从生理学角度合理化姐弟恋、对低俗照片的精准审美点评、还是在句号出现时秒变"报告顶美"的情商秀，峰哥的发言质量堪称VIP水准。明明是卖房的中介，却活成了群里的意见领袖。',
        ['情商在线', '高质量发言', '意见领袖']),
    'W': ('W', 29,
        '佛系但锋利。平时不怎么出现，一出现就问关键问题——"说瓜的人呢""心情差的时候你老公呼吸都是错吗"。像群聊里的刺客，平时潜行、关键时候补一刀立刻消失。话少是因为不需要多说，一句顶十句。',
        ['沉默刺客', '灵魂拷问', '一击脱离']),
    '小辣椒': ('小辣椒', 26,
        '惜字如金型选手。主要参与了两性话题的讨论——从"一天五次的可行性"到"女性的生理极限"，虽然发言不多但话题参与度很高。像那种在课堂上不爱举手但被点名时总能答出标准答案的好学生。',
        ['潜水选手', '话题参与者']),
    '小苏爱吃糖': ('小苏爱吃糖', 26,
        '群里的精美捧场员。日常分享窗外风景、精准复读金句、偶尔加入两性话题讨论。和超级丹互动频繁——"老公天天想要咋办"这句复读堪称本周最佳接梗。性格温和不挑事，但存在感并不弱。',
        ['温柔捧场', '复读艺术家', '超级丹闺蜜']),
    '月下数青钱🌙': ('月下数青', 25,
        '神秘潜水型群友。发言频率低但每次都在深夜出现，有种"白天要上班、晚上才有空看看群在聊啥"的打工气息。发言内容偏配合型，不主导话题但也从不冷场。',
        ['深夜幽灵', '潜水围观']),
    '摄影师-逸轩': ('摄影师逸轩', 12,
        '存在感不高但关键时刻在线。在每天的八卦讨论中都有参与但发言量偏低，属于默默围观偶尔冒泡型。"谢谢帅哥"和"然后呢"这两句话精准概括了他的群聊定位——礼貌又好奇。',
        ['礼貌围观', '安静吃瓜']),
    '反正要走': ('反正要走', 12,
        '深夜话题专属发言人。每次出现都在凌晨时段，对姐弟恋话题有自己的一套见解——"就怕没完没了""这姐姐应该情感经验比较丰富吧"。典型的深夜哲学家模式，白天大概在补觉。',
        ['深夜哲学家', '姐弟恋观察员']),
    '不黏人的猫～': ('不黏人的猫', 10,
        '压线进入活跃榜的潜水选手。10条发言可能都是一天之内完成的，平时大概率是默默划屏的看客。虽然有资格上活跃榜但实际存在感不高，属于"我知道这个人在群里但想不起来他说过什么"的类型。',
        ['保级选手', '边缘OB']),
}

active_stars_html = ""
active_stars_data = []

for i, (name, count) in enumerate(stars_raw, 1):
    profile = star_profiles.get(name, (name, count, '存在感稳定，时不时冒泡参与话题讨论。', ['群聊参与者']))
    display_name = profile[0]
    comment = profile[2]
    tags = profile[3]
    tag_html = ' '.join(f'<span class="tag">{t}</span>' for t in tags)

    active_stars_html += f"""
<li>
  <div class="rank-item">
    <span class="rank-main"><span style="color:var(--muted);margin-right:8px;">#{i}</span>{display_name}</span>
    <span style="color:var(--cyan);font-weight:700;">{count}条</span>
  </div>
  <span class="star-note">{comment}</span>
  <div class="tag-row">{tag_html}</div>
</li>"""

    # Truncate name for data
    short = display_name[:8] if len(display_name) > 8 else display_name
    active_stars_data.append([short, count])

stars_data_json = json.dumps(active_stars_data, ensure_ascii=False)

# ============================================================
# Topic Forest Data
# ============================================================
forest_data = {
    "center": {
        "title": "两性与社交",
        "note": "群聊核心围绕两性关系、生活社交和即时娱乐展开——从姐弟恋实战到前任经济学，长沙青年的夜聊文化一览无余。"
    },
    "branches": [
        {
            "title": "两性话题",
            "icon": "\U0001f495",
            "color": "#e056fd",
            "topics": ["姐弟恋实战", "一天五次挑战", "性致心情论", "韭菜食疗研究"]
        },
        {
            "title": "前任经济学",
            "icon": "\U0001f4b0",
            "color": "#ffa94d",
            "topics": ["九百克黄金", "42万奥迪", "出轨与小三", "门当户对论"]
        },
        {
            "title": "吃喝玩乐",
            "icon": "\U0001f35c",
            "color": "#3bf0c3",
            "topics": ["榴莲外交", "鱼生生腌局", "河西烧烤", "排骨战争"]
        },
        {
            "title": "群聊社交",
            "icon": "\U0001f3ad",
            "color": "#5b8cff",
            "topics": ["麻将焦虑", "相亲直播", "溯溪活动", "好友申请鉴定"]
        },
        {
            "title": "生活日常",
            "icon": "\U0001f3e0",
            "color": "#7bed9f",
            "topics": ["厨房直播", "窗边风景", "结婚喜糖", "摸鱼上班"]
        }
    ]
}
forest_json = json.dumps(forest_data, ensure_ascii=False)

# ============================================================
# Relationship Data
# ============================================================
rel_data = {
    "note": "星城神仙小分队以超级丹和拉金子的猴子为双中心——一位负责抛话题、一位负责讲故事，其余群友围绕话题随缘加入。整体呈放射状互动结构，无明显小团体。",
    "nodes": [
        {"id": "拉金子的猴子", "weight": 48, "color": "#e056fd", "role": "故事大王"},
        {"id": "超级丹💗", "weight": 42, "color": "#ff6b98", "role": "话题女王"},
        {"id": "九思", "weight": 36, "color": "#5b8cff", "role": "金句制造者"},
        {"id": "掘炭仔", "weight": 34, "color": "#4de2ff", "role": "捧哏王"},
        {"id": "齐齐大圣", "weight": 32, "color": "#3bf0c3", "role": "气氛担当"},
        {"id": "丑东西", "weight": 28, "color": "#ffd93d", "role": "冷面笑匠"},
        {"id": "沐沐不找对象", "weight": 26, "color": "#a29bfe", "role": "理性担当"},
        {"id": "脑壳炸", "weight": 24, "color": "#ff6b6b", "role": "暴论输出"},
        {"id": "峰哥-长沙卖房人", "weight": 22, "color": "#7bed9f", "role": "意见领袖"},
        {"id": "笃定", "weight": 20, "color": "#74b9ff", "role": "社交达人"}
    ],
    "links": [
        {"source": "超级丹💗", "target": "拉金子的猴子", "type": "捧哏与逗哏", "strength": 9},
        {"source": "超级丹💗", "target": "九思", "type": "捧哏与逗哏", "strength": 7},
        {"source": "拉金子的猴子", "target": "沐沐不找对象", "type": "姐妹淘", "strength": 6},
        {"source": "九思", "target": "掘炭仔", "type": "基友", "strength": 8},
        {"source": "掘炭仔", "target": "丑东西", "type": "欢喜冤家", "strength": 5},
        {"source": "齐齐大圣", "target": "拉金子的猴子", "type": "搭子", "strength": 6},
        {"source": "超级丹💗", "target": "峰哥-长沙卖房人", "type": "商业互吹", "strength": 5},
        {"source": "九思", "target": "齐齐大圣", "type": "捧哏与逗哏", "strength": 6},
        {"source": "脑壳炸", "target": "掘炭仔", "type": "基友", "strength": 7},
        {"source": "超级丹💗", "target": "丑东西", "type": "欢喜冤家", "strength": 5},
        {"source": "拉金子的猴子", "target": "九思", "type": "搭子", "strength": 5},
        {"source": "笃定", "target": "拉金子的猴子", "type": "搭子", "strength": 4}
    ]
}
rel_json = json.dumps(rel_data, ensure_ascii=False)

# ============================================================
# Word Cloud Data
# ============================================================
word_cloud = [
    ["姐弟恋", 85], ["前任", 75], ["出轨", 60], ["榴莲", 55],
    ["相亲", 50], ["打牌", 48], ["排骨", 45], ["韭菜", 40],
    ["八卦", 38], ["男朋友", 36], ["女朋友", 34], ["黄金", 32],
    ["老公", 30], ["聊天", 28], ["结婚", 26], ["美食", 25],
    ["鱼生", 24], ["麻将", 22], ["溯溪", 20], ["烧烤", 18],
    ["上班", 17], ["厨房", 16], ["唱歌", 15], ["台球", 14],
    ["旅行", 13]
]
wc_json = json.dumps(word_cloud, ensure_ascii=False)

# ============================================================
# Read template and fill
# ============================================================
template_path = os.path.join(skill_dir, "assets", "report-template.html")
with open(template_path, 'r') as f:
    html = f.read()

# Summary blurb
summary_blurb = "4115条消息烧穿一周夜话，从姐弟恋实战到前任的九百克黄金，星城神仙小分队用两性话题和深夜故事会撑起了本周期最活跃的群聊生态。"

# Full summary section
full_summary_cards = summary_cards

replacements = {
    '{{GROUP_NAME}}': '星城神仙小分队',
    '{{REPORT_TYPE}}': '周报',
    '{{DATE_RANGE}}': '2026-07-22 ~ 2026-07-29',
    '{{SUMMARY_BLURB}}': summary_blurb,
    '{{SUMMARY_CARDS}}': full_summary_cards,
    '{{TREND_DATA}}': json.dumps(trend_data, ensure_ascii=False),
    '{{TREND_CARD}}': trend_card,
    '{{SUMMARY_LINE}}': summary_line,
    '{{HOT_TOPICS}}': hot_topics,
    '{{ACTIVE_STARS}}': active_stars_html,
    '{{ACTIVE_STARS_DATA}}': stars_data_json,
    '{{TOPIC_FOREST_DATA}}': forest_json,
    '{{WORD_CLOUD_DATA}}': wc_json,
    '{{GROUP_RELATIONSHIPS}}': rel_json,
    '{{SUPPORT_QR_IMAGE}}': qr_data,
}

for key, val in replacements.items():
    html = html.replace(key, val)

# Verify no placeholders remain
placeholders = re.findall(r'\{\{.*?\}\}', html)
if placeholders:
    print(f"WARNING: Unfilled placeholders: {placeholders}")
else:
    print("All placeholders filled successfully!")

# ============================================================
# Save
# ============================================================
output_path = "/Users/jiangtao/ai/wx周报/report/星城神仙小分队/星城神仙小分队_20260729.html"
with open(output_path, 'w') as f:
    f.write(html)

file_size = os.path.getsize(output_path)
print(f"Report saved to: {output_path}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
