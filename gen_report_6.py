# -*- coding: utf-8 -*-
import json, base64, os, re
from collections import Counter

# ============================================================
# Load data
# ============================================================
msgs = []
with open('/Users/jiangtao/.wechat-insight/data/长沙长沙（返湘1群）.jsonl') as f:
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
  <div class="trend-note">消息量在 07/27-07/28 达到峰值（1700+条），围绕股市行情和婚恋话题掀起两轮高潮，周末相对平淡。</div>
</div>
"""

# Summary line
summary_line = """
<div class="summary-line">
  <span class="summary-line-label">高频情绪：</span>📈 股市焦虑 🔥 婚恋八卦 💰 生活成本吐槽 🤔 返湘迷茫 😂 集体吐槽湖南
</div>
"""

# ============================================================
# Hot Topics
# ============================================================
hot_topics = """
<li>
  <span class="topic-title">📈 长鑫上市与半导体血崩：群友在线盯盘的一天</span>
  <span class="topic-act">第一幕：开盘即巅峰</span>
  <span class="topic-step">长鑫存储本周一上市，开盘冲高后迅速回落，群友从"79.8还真有希望"一路看到跌近十个点</span>
  <span class="topic-step">上海亚牌照明中签500股，开盘后卖出键变灰一度无法交易，最终在群友"抓紧卖"的催促下45块走人，小赚2W</span>
  <span class="topic-step">全场恭喜声刷屏——返湘小助手自动接龙祝福，群友排队"感谢老板早餐支持"</span>
  <span class="topic-act">第二幕：全球芯片风暴</span>
  <span class="topic-step">美股半导体暴跌：英伟达跌4.99%、闪迪跌11%、SK海力士跌7.47%、AMD跌5.17%、阿斯麦跌5.8%</span>
  <span class="topic-step">打螺丝-💗写意 全文播报美股芯片跌幅，Kerwin庆幸"昨天清仓了，今天看戏"</span>
  <span class="topic-step">吾生有涯哀叹"泱泱大国炒个股还要看棒子脸色"——群友集体共鸣"窝囊到家了"</span>
  <span class="topic-act">第三幕：科技信仰崩塌</span>
  <span class="topic-step">吾生有涯总结"这轮科技周期已经彻底烂了，空仓等下一轮"</span>
  <span class="topic-step">Kerwin表示"周末这么多利好周一开盘还是止不住，确实到了预期悲观的阶段"</span>
  <span class="topic-step">麦哥2025分享朋友通化金马被套惨状——女朋友都要分手了，彩礼都给不起</span>
  <span class="topic-step">打螺丝-💗写意灵魂追问"彩礼算不算闲钱"——全场沉默后爆笑</span>
  <div class="highlight-quote">
    <span class="highlight-text">"尼玛我泱泱大国炒个股，还得看人家棒子脸色"</span>
    <span class="highlight-author">— 吾生有涯</span>
  </div>
  <span class="ai-note">💬 AI 锐评：长鑫上市是全周期最高光时刻——上海亚牌照明靠500股赚了2万块跑了，群友的恭喜声比他自己还激动。可惜好景不长，美股一场芯片暴跌把大家都拉回了现实。从"79.8有希望"到"空仓等下一轮"，只用了三天时间就完成了牛市→熊市的心态切换，效率惊人。</span>
  <span class="topic-participants">主要参与者：上海亚牌照明、吾生有涯、Kerwin、打螺丝-💗写意、麦哥2025、乐儿💕</span>
</li>

<li>
  <span class="topic-title">💔 🐽的爱情急诊室：26岁妹妹和34岁无业男友该不该跑</span>
  <span class="topic-act">第一幕：困境全曝光</span>
  <span class="topic-step">🐽 在群友"不婚不育"话题中突然切入自己的困惑：23岁和大8岁男友在一起，第一年就见了父母说要结婚</span>
  <span class="topic-step">在一起一年后发现男友外面欠债十几万，父母帮忙还清后男友觉得"愧对父母"</span>
  <span class="topic-step">男友已失业一年无存款无房，父母催婚越来越猛——但五金钱4万被男友花掉了，父母不愿再出</span>
  <span class="topic-act">第二幕：群友集体问诊</span>
  <span class="topic-step">长沙群-雨上以过来人身份连环追问"催婚以后马上催生""你有没有跟父母相处过""婚前答应的事婚后全变"</span>
  <span class="topic-step">姚钱树3.0戳中要害"三十多了还没存款很危险""没钱才是最小的问题"</span>
  <span class="topic-step">淡写～～、重返人间北京银行、小卒三位"前任过来人"异口同声"趁没结婚赶紧跑"</span>
  <span class="topic-step">吾生有涯反向拉偏架"别误导小姑娘，人家情侣关系好着呢"——但立刻被群友用事实压回去</span>
  <span class="topic-act">第三幕：犹豫与拉扯</span>
  <span class="topic-step">🐽 坦言自己23岁就在一起，处了三年多放不下</span>
  <span class="topic-step">但男友父母有慢性病、未来大概率同住、自己26岁还要不要继续等——每个问题都在加重她的焦虑</span>
  <span class="topic-step">阿瑞一句话总结"35的老登还没意识！"全场点赞</span>
  <span class="topic-step">最后🐽留下"我也觉得不可能"的动摇表态——群友的建议没白给</span>
  <div class="highlight-quote">
    <span class="highlight-text">"他父母知道后就不愿意再出这个钱了，他现在也没存款"</span>
    <span class="highlight-author">— 🐽</span>
  </div>
  <span class="ai-note">💬 AI 锐评：🐽的投稿揭开了本周期最沉重的一个话题。从23岁到26岁，三年感情绑在一个负债、失业、34岁还没存款的男人身上——群友集体扮演了一回理智闺蜜团，从经济、家庭、人生节奏三个维度劝退。长沙群-雨上的"婚前承诺婚后全废"血泪发言比任何大V的情感建议都有说服力。反观吾生有涯的"人家感情好着呢"，大概就是为什么这年头情感咨询生意这么好做。</span>
  <span class="topic-participants">主要参与者：🐽、长沙群-雨上、淡写～～、姚钱树3.0、重返人间北京银行、吾生有涯、阿瑞</span>
</li>

<li>
  <span class="topic-title">🎯 Tina脱单行动：帮94年的妹妹在群里找对象</span>
  <span class="topic-act">第一幕：公开征集</span>
  <span class="topic-step">Tina 直接在群里发问"有没有定居长沙的单身男士，找结婚对象的"——有个94年的妹妹急需结婚对象</span>
  <span class="topic-step">上海-IT-刃心火速推荐小舅子"93年，高中学历，人老实"，并附上照片</span>
  <span class="topic-step">群友对颜值给予肯定反馈后，Tina大方表态"真长得挺好的，什么时候回长沙约着见见"</span>
  <span class="topic-act">第二幕：婚恋观念大碰撞</span>
  <span class="topic-step">话题从相亲滑向更深的婚恋讨论：草坪头推荐"找个弟弟不香吗"，重返人间北京银行主张"高门槛不行就换"</span>
  <span class="topic-step">打螺丝-💗写意分享"群主之前搞过相亲，可以搞个AI相亲"引发群友热议</span>
  <span class="topic-step">重返人间北京银行提出"AI分身先跟潜在对象聊，聊好再真人见面"的科幻级相亲方案</span>
  <span class="topic-step">吾生有涯金句"剩男剩女的心冷得像大润发杀了二十年鱼的那把刀"把气氛推向高潮</span>
  <span class="topic-act">第三幕：群主下场</span>
  <span class="topic-step">长沙-金融-森岚（群主）透露去年做了4场相亲沙龙，今年精力跟不上没搞</span>
  <span class="topic-step">打螺丝-💗写意建议"搞徒步读书会更好"，淡写～～补充"借兴趣自然结识比硬相亲效果好"</span>
  <span class="topic-step">终局：Tina加了上海-IT-刃心私聊，群友集体拿到了一个相亲直播间的入场券</span>
  <div class="highlight-quote">
    <span class="highlight-text">"剩男剩女们的心冷得像大润发杀了二十年鱼的那把刀"</span>
    <span class="highlight-author">— 吾生有涯</span>
  </div>
  <span class="ai-note">💬 AI 锐评：Tina用一个公开征婚把群聊从股市焦虑中拉了回来。上海-IT-刃心的"小舅子推荐"堪称群内中介业的顶级操作——不仅带着照片来，还附带了完整的简历式介绍。从AI相亲到AI分身再到杀鱼刀比喻，这一波话题在"找对象"这个传统命题上开出了不少新花样。至于群主去年的沙龙为什么不搞了——大概是被"剩男剩女们零下二十度的热情"冻住了。</span>
  <span class="topic-participants">主要参与者：Tina、上海-IT-刃心、重返人间北京银行、打螺丝-💗写意、吾生有涯、长沙-金融-森岚</span>
</li>

<li>
  <span class="topic-title">💰 彩礼经济学：永州20万起步 vs 长株潭12万"良心价"</span>
  <span class="topic-act">第一幕：真实报价</span>
  <span class="topic-step">长沙~一味 发来一线情报：粉店老板说永州彩礼20几万起步，快要追上江西了</span>
  <span class="topic-step">打螺丝-💗写意证实：老公表妹前两年就要20多万，虽然长得高漂亮，但直接标价有点太赤裸</span>
  <span class="topic-step">长沙群-雨上否认"瞎说，没有这么高，个别的吧"——但语气底气不太足</span>
  <span class="topic-act">第二幕：不嫁不娶新潮流</span>
  <span class="topic-step">长沙群-雨上透露老家流行"不嫁不娶"：不要彩礼也没有嫁妆，生两个娃一边姓一个</span>
  <span class="topic-step">打螺丝-💗写意指出父母完全接受不了这种模式</span>
  <span class="topic-step">长沙~一味 细算一笔账后承认"结婚起步80万，好像也没问题"——群友陷入沉默</span>
  <span class="topic-act">第三幕：婚姻经济学</span>
  <span class="topic-step">话题延伸到多兄弟家庭的问题：长沙群-雨上透露谈过一个两兄弟的，被母亲坚决反对</span>
  <span class="topic-step">但她也苦笑找了个独生子还是一地鸡毛——婆婆同住带娃、公公水火不容</span>
  <span class="topic-step">群友最终结论：有没有钱都是问题，关键看心态</span>
  <div class="highlight-quote">
    <span class="highlight-text">"一说结婚就说起步80w——我刚想反驳，他就跟我算了一笔账，好像也没问题"</span>
    <span class="highlight-author">— 长沙~一味</span>
  </div>
  <span class="ai-note">💬 AI 锐评：一场从"永州彩礼20万"开始的田野调查，最终以"结婚起步80万"的账单暴击收场。长沙群-雨上的"不嫁不娶"方案听起来很平等，但执行难度堪比上市公司合并重组。而两兄弟 vs 独生子的对比实验证明了一件事：你以为的坑和你实际掉进去的坑，永远是不同的坑。</span>
  <span class="topic-participants">主要参与者：长沙~一味、打螺丝-💗写意、长沙群-雨上、吾生有涯、🐽</span>
</li>

<li>
  <span class="topic-title">🏙️ 返湘生存指南：长沙真的回得去吗？</span>
  <span class="topic-act">第一幕：回不去的长沙</span>
  <span class="topic-step">进化论。。。！加入群聊后吐露心声："20年被逼离开奋斗8年的长沙来广东，现在平稳了想回去，但觉得回不去了"</span>
  <span class="topic-step">打螺丝-💗写意透露曾动员老板把厂搬回长沙——老板说"你别开玩笑了"</span>
  <span class="topic-step">现在前老板的厂越搬越偏，都快到河源了——制造业外流趋势肉眼可见</span>
  <span class="topic-act">第二幕：湖南的槽点大会</span>
  <span class="topic-step">上海-IT-刃心甩出知乎链接"好多吐槽咱们湖南的"，引发群友集体自黑</span>
  <span class="topic-step">风禾-半导体PCB精准补刀"来了8年，坑坑洼洼永远修不好的二环线"</span>
  <span class="topic-step">吾生有涯透露认识的老板宁愿去江西贵州投资，一听说湖南直摇头——名声搞臭了几十年恢复不过来</span>
  <span class="topic-step">打螺丝-💗写意爆料"湖南都还有黑社会"，长沙~一味接话"知道衡阳火车站为什么需要武警执勤吗"</span>
  <span class="topic-act">第三幕：长株潭还能打吗</span>
  <span class="topic-step">已返长-运营-ken搬运深度分析：萍乡反而比岳阳常德更能享受长株潭溢出效应</span>
  <span class="topic-step">19年是长沙巅峰，如今的发展势头不如从前</span>
  <span class="topic-step">群友在"想回去"和"回不去"之间反复横跳——这也是返湘群永恒的母题</span>
  <div class="highlight-quote">
    <span class="highlight-text">"我上海认识的老板都宁愿去江西、贵州投资，一听说去湖南投都直摇头"</span>
    <span class="highlight-author">— 吾生有涯</span>
  </div>
  <span class="ai-note">💬 AI 锐评：返湘群的核心矛盾在本周集中爆发——人在外省想回、回了发现槽点比想象中多、不回又心有不甘。从衡阳火车站的武警到修了8年的二环线，湖南被群友自己人吐槽得体无完肤。但"名声搞臭了几十年恢复不过来"这句话，恐怕是本周最有分量的一句黑色幽默——毕竟说这话的人自己也在想方设法回来。</span>
  <span class="topic-participants">主要参与者：进化论。。。！、打螺丝-💗写意、上海-IT-刃心、吾生有涯、风禾-半导体PCB、已返长-运营-ken</span>
</li>

<li>
  <span class="topic-title">🏠 海景房泡沫：11万70平的山东乳山 vs 惠州的百元海景</span>
  <span class="topic-act">第一幕：天道酬勤的海景房直播</span>
  <span class="topic-step">天道酬勤在荣成海景房现场直播：11万70平、开盘6500现在1300</span>
  <span class="topic-step">上海亚牌照明提起"乳山几万块一套"的传说，20岁了还没吃过麦当劳立刻接话"帮我带一套"</span>
  <span class="topic-step">但配套只有一个老太太早上卖包子，剩下的全是海鸥</span>
  <span class="topic-act">第二幕：海景房性价比之战</span>
  <span class="topic-step">广州-晓燕～和打螺丝-💗写意分享惠州海景：工作日200不到的海景房，周末不可能</span>
  <span class="topic-step">天道酬勤补刀"纯海景房，鸟不拉屎"，Leo给title"面朝大海春暖花开——但没吃的没喝的"</span>
  <span class="topic-step">乐儿💕惊讶"11万70平"，深圳-IT表示"很多内陆投资客全砸手里了"</span>
  <div class="highlight-quote">
    <span class="highlight-text">"唯一的配套是早晨有个老太太卖包子，其他就没了"</span>
    <span class="highlight-author">— 天道酬勤</span>
  </div>
  <span class="ai-note">💬 AI 锐评：天道酬勤以一己之力完成了海景房的全方位祛魅——11万一套听起来像是捡漏，配上"老太太卖包子"的配套信息之后，听起来就像买了块海边的荒地。群友从"帮我带一套"到"只剩鸟拉屎了"只用了两轮对话，堪称房地产泡沫的微观崩塌现场。</span>
  <span class="topic-participants">主要参与者：天道酬勤、上海亚牌照明、打螺丝-💗写意、乐儿💕、20岁了还没吃过麦当劳</span>
</li>

<li>
  <span class="topic-title">👥 深圳合租血泪史：从抢厕所到程序员不解风情</span>
  <span class="topic-act">第一幕：合租回忆杀</span>
  <span class="topic-step">从租房价格讨论自然滑向合租经历分享——打螺丝-💗写意回忆刚来深圳时跟网友合租的青春岁月</span>
  <span class="topic-step">吾生有涯贡献了一串离谱室友：霸占卫生间一小时的、姨妈斤乱飞的、半夜带人回来啊啊啊的</span>
  <span class="topic-step">而遇到的最靠谱室友是个程序员——房间自带厕所、平时隐身、公区卫生保持完美</span>
  <span class="topic-act">第二幕：程序员の不解风情</span>
  <span class="topic-step">吾生有涯断断续续讲出一个都市故事：隔壁妹子对程序员有意思，故意喝他冰箱里的啤酒然后v他</span>
  <span class="topic-step">结果程序员让她直接发群里——妹子被硬生生劝退</span>
  <span class="topic-step">有天晚上程序员还带了应召女郎回来——群友集体震住</span>
  <span class="topic-step">打螺丝-💗写意盖章"程序员基本上没有生活痕迹"——Tina补刀"还没有对象"</span>
  <div class="highlight-quote">
    <span class="highlight-text">"那个妹子会故意喝程序员放在冰箱里的啤酒，然后v给他，想加他微信，结果程序员让她直接v群里"</span>
    <span class="highlight-author">— 吾生有涯</span>
  </div>
  <span class="ai-note">💬 AI 锐评：一段合租史硬是被吾生有涯讲成了都市轻喜剧。从凌晨两点的噪音大战到程序员的"心里只有bug"，每一个离谱室友背后都站着一个被生活毒打过的租房人。而程序员不解风情的段子——妹子故意v他想加微信，他让人家直接发群里——可能是本周最能代表"钢铁直男"的高光时刻了。</span>
  <span class="topic-participants">主要参与者：吾生有涯、打螺丝-💗写意、Tina、长沙~一味、Kerwin</span>
</li>

<li>
  <span class="topic-title">🛠️ 麦哥的程序员朋友：裁员60万补偿、广州两套房、300万现金、一辆老轩逸</span>
  <span class="topic-act">第一幕：人生赢家模板</span>
  <span class="topic-step">麦哥2025分享朋友故事：三本毕业程序员，去年裁员拿了60万补偿</span>
  <span class="topic-step">狂投简历2个月后放弃，现在兼职炒股+接送娃</span>
  <span class="topic-step">广州两套房自住+出租，身边3-400万现金，房贷几乎没有</span>
  <span class="topic-act">第二幕：全民找茬</span>
  <span class="topic-step">但画风急转直下——麦哥补刀"车还是个7/8年老轩逸""老婆也不漂亮"</span>
  <span class="topic-step">三生石反驳"3-400万现金老婆就一定漂亮？"引发讨论</span>
  <span class="topic-step">Tina好奇"能忍住不换电车确实牛"，麦哥总结"所以他可以存到钱，8年我换了4-5个车，他还在原地踏步"</span>
  <div class="highlight-quote">
    <span class="highlight-text">"8年时间我都已经换了4/5个车了，他还在原地踏步"</span>
    <span class="highlight-author">— 麦哥2025</span>
  </div>
  <span class="ai-note">💬 AI 锐评：麦哥用一段"看似炫耀实则吐槽"的朋友故事，展示了什么叫真正的财务自由——不是开什么车，是不用上班也能活。而全群最扎心的瞬间是麦哥一句轻描淡写的"老婆也不漂亮"——你都有300万现金了还嫌弃老婆不好看，群友纷纷表示这就是为什么你换车不如人家频繁。</span>
  <span class="topic-participants">主要参与者：麦哥2025、三生石、Tina、吾生有涯、Kerwin</span>
</li>
"""

# ============================================================
# Active Stars HTML
# ============================================================
star_profiles = {
    '打螺丝-💗写意': ('打螺丝-💗写意', 418,
        '本周当之无愧的话量女王——400多条发言几乎覆盖每一个话题。从早上抱怨台风天上班到晚上聊合租八卦，螺丝姐是群聊的稳定输出器。特点是"我有话说就一定要说"，而且每条都掷地有声——讲职场、骂老板、聊婚姻、分享人生经验，是全群的定海神针和气氛发动机。唯一的缺点是语速太快，群友还没接上她已经发了第三条。',
        ['话题女王', '话量担当', '人生经验包']),
    'Kerwin': ('Kerwin', 238,
        '群里的理智型选手。周三清仓躲过半导体暴跌后，全天的发言基调从"run吧"切换到"今天看戏了"，情绪管理堪称大师级。平时话不算最多，但每次行情有变时必定出现——像股市晴雨表一样准时。合租话题里也不忘补刀"碰到抽烟的顶不住"，生活品质感刻在骨子里。',
        ['股市晴雨表', '理智撤退者', '品质控']),
    '吾生有涯': ('吾生有涯', 220,
        '群里的金句批发商。本周贡献了两条名言级输出：关于股市的"窝囊他妈给窝囊开门"，和关于婚恋的"剩男剩女的心冷得像杀了二十年鱼的刀"。自带上海观察员视角——从静安寺的比基尼老外写到华政鉴定中心的考证狂人，叙事节奏感一流。缺点是总在情感话题里扮演"理中客"角色，被群友怼回去的时候也颇有喜感。',
        ['金句制造机', '段子手', '气氛调节器']),
    '长沙群-雨上': ('长沙群-雨上', 188,
        '婚恋话题的核心军师。以过来人姿态，用亲身经历为🐽等迷茫青年提供一线婚恋咨询：从"不嫁不娶"的新风俗到"婚前承诺婚后全废"的血泪教训，句句带刀。经典发言"我妈说我性格不好不愿意吃亏不利于家庭和谐——我说傻子才愿意吃亏"堪称人间清醒三观。同时爆料老家流行"两个娃一边姓一个"，刷新了群友对湖南婚俗的认知。',
        ['婚恋军师', '人间清醒', '吐槽担当']),
    '🐽': ('🐽', 164,
        '本周群聊的"女主角"。带着26岁的婚恋困惑闯入群聊后，意外开启了一场全群参与的集体问诊。坦诚、真实、不矫饰——从男友负债史到父母催婚到五金钱被花掉，每一条发言都踩在当代年轻人最敏感的婚恋神经上。虽然被群友"赶紧跑"的建议包围，但她最后那句"我也觉得不可能"说明她已经有了答案，只是需要被确认。',
        ['勇敢追问者', '群聊女主角', '年轻人的样本']),
    '乐儿💕': ('乐儿💕', 135,
        '股市专线话务员。主要出现在股票讨论时段，对成交额、指数点位和市场情绪有专业级敏感度。"今天到现在居然才2万亿""4000元都能赚2万"——发言精炼但对群聊话题的推进作用很大。同时偶尔展现柔情一面——对深圳-IT的"爱妻论"给予了正面肯定，证明了她不是只会看K线。',
        ['股市雷达', '温柔点评员', '情绪观察者']),
    '小卒': ('小卒', 113,
        '擅长一语道破的锋利型选手。话不多但切入点精准：合租被偷吃冰箱的尴尬、海景房捡漏的坑、婚姻中的现实问题——每次开口都带着"我一个朋友"的叙事外壳，但谁都看得出来说的都是自己的观察。那句"不是人比海鲜多"对海景房讨论一锤定音。',
        ['一针见血', '经验输出者', '务实派']),
    '上海亚牌照明': ('上海亚牌照明', 89,
        '本周最大赢家——中签长鑫500股，45块卖出小赚2万，被群友集体恭喜了一整天。从"不让卖"的买家焦虑到卖完后的"反弹了就是洗盘"，全流程直播新股操作的刺激感。平时喜欢在讨论中扮演老江湖——"陆家嘴是骗子聚集地""大宁已经是富人区了"，看问题角度清奇，自带行业内部视角。',
        ['新股达人', '沪上观察者', '隐形凡尔赛']),
    '淡写～～': ('淡写～～', 83,
        '群里的"过来人"担当。在🐽求助帖中以淡定的"别问我为啥知道"姿态分享过往前车之鉴，建议简单粗暴"赶紧跑路"。时不时插播户外经历——徒步圈年轻人的约炮文化、炒冰摊的美食测评——让群聊在沉重话题间得到喘息。节奏把控精准，从不抢话但每次出现都有效。',
        ['清醒旁观者', '生活分享家', '建议输出者']),
    '天道酬勤': ('天道酬勤', 71,
        '荣成海景房现场直播员。以"11万70平+老太太卖包子"的荒诞组合拳完美解构了海景房投资神话。从海鸥数量到开盘价比当前价，数据详实、描述生动，像是一位驻扎海边的特派记者。偶尔出现在股市讨论里——但存在感主要靠"一套房只要11万"这个信息锚点撑起来的。',
        ['海景房特派员', '直播达人', '人间真实']),
    'Tina': ('Tina', 66,
        '公开征婚行动的发起人。用一条"有没有定居长沙的单身男士"的直球提问，把全群从股市拉回了婚恋赛道。对上海-IT-刃心推荐的小舅子颜值给予了正面评价并果断进入私聊环节，执行力满分。虽然来群里的主要目的是帮妹妹找对象，但自己的故事分享——一年认识、一年结婚——本身就证明了她有资格当这个媒人。',
        ['媒人担当', '执行派', '话题引导者']),
    'Leo': ('Leo', 60,
        '安静的观察型选手。发言不太频繁但每次都点到关键处——"面朝大海春暖花开——但没吃的没喝的""上海竟然不挤，城市规划得好"。对湖南经济的"湖南被安徽挤出前十"一句引发全群讨论。像群里的弹幕员，不动声色地给每个话题配一条精准的观察性评论。',
        ['安静观察者', '一针见血', '数据控']),
    '上海-IT-刃心': ('上海-IT-刃心', 53,
        '群里的"人脉王"。Tina征婚他第一个推荐小舅子，不仅附照片还配完整背景介绍。喜欢抛话题引子——知乎上吐槽湖南的帖子、小红书的开曼群岛注册信息——每次都能带动一轮高质量讨论。虽然总在抱怨工作（"校招生全是985211"），但说话风格自带IT行业特有的冷幽默。',
        ['人脉枢纽', '话题点火人', 'IT行业观察者']),
    '重返人间 北京 银行': ('重返人间 北京 银行', 50,
        'AI相亲的提出者。"AI分身先聊再真人见面"的想法让全群眼前一亮。个人感情经历方面也不藏着掖着——"和前任死磕一年也分了"，并分享"前期多认识多撒网"的心得。在🐽的求助帖中通过类比"像极了我上一段恋情"提供了共情式建议，是有故事的人。',
        ['AI相亲推广大使', '经验输出者', '理性派']),
    '草坪头': ('草坪头', 50,
        '精准的短评运动员。发言很少超过10个字，但每次都命中要害——"还得是建模""生理性喜欢""找个弟弟不香吗""没混出样子的校庆都不会请你"。在群聊里扮演捧哏角色：别人抛梗他接，别人吐槽他补刀，存在感全靠精准打击而非刷屏。',
        ['短评王', '捧哏高手', '精准打击']),
    '麦哥2025': ('麦哥2025', 48,
        '群里的"别人的故事"收藏家。本周贡献了两个经典故事：通化金马被套到彩礼都给不起的程序员朋友、裁员60万补偿+广州两套房的另一种程序员朋友。一边嘲笑人家"老婆也不漂亮、车还是老轩逸"，一边又承认"所以人家可以存到钱不用上班了"——这种矛盾心理大概就是中年人的真实写照。',
        ['故事大王', '凡尔赛观察者', '人间真实']),
    '姚钱树3.0': ('姚钱树3.0', 39,
        '婚恋经济学派的代表人物。在🐽的求助中用一句话就戳穿了本质"他有钱不知道存钱不知道规划那不更恐怖吗"。紧接着分享同事案例"老公创业赔了一次又一次，她一次次拿钱"，让群友看到下一个五年可能发生什么。言语犀利但逻辑缜密，是群里的风险提示牌。',
        ['风险提示员', '现实主义', '逻辑派']),
    '已返长-运营-ken': ('已返长-运营-ken', 36,
        '长株潭发展研究专员。从萍乡承接产业溢出的深度分析到19年长沙巅峰时刻的回顾，贡献了本周质量最高的区域经济讨论。用数据说话，不带情绪，风格在一众吐槽里显得格外冷静。应该是那种话不多但一开口就有货的人。',
        ['区域经济观察员', '数据型选手', '返湘样本']),
    '欲买桂花同载酒': ('欲买桂花同载酒', 34,
        '群内的闷声发大财型潜水员。发言不多但每次都在关键节点上——"2元就可以买价值8亿元股权"这种冷知识型提问让人怀疑她知道些什么内幕。参与话题范围广但不深入，是那种群聊里的"我知道她在但想不起来说了啥"的稳定存在。',
        ['冷知识提供者', '低调围观', '话题参与者']),
    '广州-晓燕～': ('广州-晓燕～', 32,
        '广深生活对比的发言代表。在海景房讨论中贡献了惠州现场经验——工作日200的海景房、杨梅坑的海也很好看。在婚恋话题中偶尔插话"我身边很多80后单身女性自己过的很好""可以找小男朋友谈恋爱"，为群聊增加了独立的女性视角。',
        ['女性视角代表', '广深生活家', '人间清醒']),
    '深圳-IT': ('深圳-IT', 25,
        '本周最动人的故事讲述者。以自传体长文分享了自己从一个又黑又矮的大专生到深圳程序员的逆袭——"我以为自己会孤独终老"到"老婆孩子照片做头像"的转变让乐儿💕都忍不住感叹"字里行间都能感觉你对老婆的爱"。他的故事证明了"命运算卦>选择>努力"这个被群友反复引用的公式。',
        ['故事王', '人生逆袭代表', '爱妻典范']),
    '天心搁主': ('天心搁主', 28,
        '合租生活的和平主义者。"我一直合租的，遇到的都挺好的"——在一群合租血泪史中宛如一股清流。但随后又补了一句"有些也是相互嫌弃吧，嘴上说"，说明他也并非没遇到过问题只是心态好。在长鑫上市赚2万后第一时间排队祝贺，说明在群里属于"与人为善"型选手。',
        ['合租乐观派', '与人为善', '和平爱好者']),
    '风禾-半导体PCB': ('风禾-半导体PCB', 17,
        '专程吐槽长沙基础设施的精准炮手。"来了8年坑坑洼洼永远修不好的二环线"一句话就让全湖南人无法反驳。岗位是半导体PCB，属于本群"返湘专业人士"阵营的典型代表——在深圳做着高层次的工作，但对家乡的槽点比谁都清楚。',
        ['长沙吐槽王', '专业人士', '返湘观察员']),
    '樱桃圆子': ('樱桃圆子', 16,
        '本周的暴论冠军。"剖腹产的钱都没有，生二胎？""有点同情这个二胎孩子"——在Leo讲述姐姐的故事时以两句暴击式发言完成了本周最犀利的现场评论。话不多但足够狠，让人过目不忘。',
        ['暴论输出者', '一针见血', '犀利姐姐']),
    '三生石': ('三生石', 20,
        '湘潭白菜价房子的关注者。"我在等它降到10万以下"——群友的房地产悲观预期在他这里得到了具象化表达。对麦哥炫耀朋友财富时反击"3-400万现金老婆就一定漂亮？""3-4万的黄毛也可以有很漂亮的老婆"，三观极正。',
        ['人间清醒', '三观输出', '围观群众']),
    '马斯洛': ('马斯洛', 17,
        '社交媒体时代的哲学爱好者。"群里搞不起来""30+的单身都难伺候""不干涉别人的因果"——每句话都像帖子标题，简短有力但总带着"我已看透一切"的疲惫感。在相亲话题中一句"广撒网"被本群专业捧场王精准复读，形成了本周最小的一个子话题。',
        ['哲学爱好者', '金句输出', '人间观察者']),
    '本群专业捧场王': ('本群专业捧场王', 20,
        '人如其名——群里的复读机担当。把别人的话复制粘贴一遍就是他对该话题最大的支持。"去过大小梅沙也算是在深圳看过海了吧""找对象还是得广撒网"——当你迷茫的时候，他帮你把群友的建议再重复一遍。看似在划水，实则在用一种很低成本的方式维持话题热度。',
        ['专业捧场', '复读机', '气氛维持者']),
    '如是我闻': ('如是我闻', 12,
        '存在感不高但每次出现都有话说的稳健型群友。发言集中在群聊的日常时段，内容偏附和型——"居然错过了红包恭喜恭喜"——属于那种潜水为主、偶尔冒泡证明自己还在的群成员。',
        ['潜水选手', '礼貌捧场', '稳健派']),
    '20岁了还没吃过麦当劳-已打流2年': ('还没吃麦当劳', 12,
        '本周最会接梗的新人之一。海景房讨论中一句"帮我带一套"把全场逗笑，复读"没混出样子的校庆都不会请你"也恰到好处。名称本身就是个梗，发言风格也继承了这种不正经但好笑的群聊基因。',
        ['接梗小能手', '群聊气氛组', '新人王']),
    '40岁了还没有喝过香飘飘': ('没喝过香飘飘', 15,
        '专攻IT行业往事的怀旧选手。"我有个朋友上大专培训半年就在深圳做IT了，以前搞IT真是碰上好时候了"——短暂地让群聊进入了"如果早生十年"的幻想时间。存在感不高但每次出现都带着"当年"的故事，像是群里的年代记忆开关。',
        ['怀旧选手', 'IT考古学家', '偶尔冒泡']),
    '机智平': ('机智平', 13,
        '专攻经济民生话题。从海景房讨论中的"人比海鲜多"到车位事件"这次的停车场事情"，再到衡阳发展话题"上指标了"——每次发言都像在给一个话题盖个戳，证明这个方向有讨论价值。话不多但定位清晰。',
        ['话题鉴定师', '经济观察者', '精准定位']),
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
        "title": "返湘者的生活与焦虑",
        "note": "群聊围绕经济生存与家庭关系两大主线展开——从股市套利到婚恋迷局，从海景房泡沫到长沙槽点，折射出在外打拼的湖南人对「回去」这件事的复杂情绪。"
    },
    "branches": [
        {
            "title": "股市投资",
            "icon": "📈",
            "color": "#e056fd",
            "topics": ["长鑫上市博弈", "半导体暴跌", "科技周期见顶", "新股中签实操"]
        },
        {
            "title": "婚恋战场",
            "icon": "💔",
            "color": "#ff6b98",
            "topics": ["彩礼经济学", "不嫁不娶新潮", "低成本相亲", "婆媳同住难题"]
        },
        {
            "title": "返湘焦虑",
            "icon": "🏙️",
            "color": "#5b8cff",
            "topics": ["长沙营商环境", "二环线永不修好", "衡阳火车站威慑", "产业外流观察"]
        },
        {
            "title": "生活成本",
            "icon": "💰",
            "color": "#ffa94d",
            "topics": ["海景房泡沫", "深圳合租往事", "房租降了吗", "沪币区物价"]
        },
        {
            "title": "职场人生",
            "icon": "💼",
            "color": "#3bf0c3",
            "topics": ["裁员补偿60万", "工厂劝退实录", "985211纯牛马", "IT行业红利"]
        }
    ]
}
forest_json = json.dumps(forest_data, ensure_ascii=False)

# ============================================================
# Relationship Data
# ============================================================
rel_data = {
    "note": "长沙返湘群以打螺丝-💗写意和吾生有涯为两大叙述中心——前者负责话量覆盖和人生经验，后者负责金句输出和上海视角。群内互动呈自由放射状，无明显小团体，新人进群后也能很快参与热门话题。",
    "nodes": [
        {"id": "打螺丝-💗写意", "weight": 48, "color": "#e056fd", "role": "话题女王"},
        {"id": "吾生有涯", "weight": 42, "color": "#5b8cff", "role": "金句制造机"},
        {"id": "Kerwin", "weight": 36, "color": "#3bf0c3", "role": "理智撤退者"},
        {"id": "长沙群-雨上", "weight": 34, "color": "#ffd93d", "role": "婚恋军师"},
        {"id": "🐽", "weight": 32, "color": "#ff6b98", "role": "话题女主角"},
        {"id": "乐儿💕", "weight": 28, "color": "#7bed9f", "role": "股市雷达"},
        {"id": "Tina", "weight": 24, "color": "#ffa94d", "role": "相亲发起人"},
        {"id": "小卒", "weight": 22, "color": "#a29bfe", "role": "一针见血"},
        {"id": "上海亚牌照明", "weight": 20, "color": "#74b9ff", "role": "新股达人"},
        {"id": "淡写～～", "weight": 18, "color": "#fd79a8", "role": "清醒旁观者"},
        {"id": "麦哥2025", "weight": 16, "color": "#fdcb6e", "role": "故事收藏家"},
        {"id": "上海-IT-刃心", "weight": 14, "color": "#6c5ce7", "role": "人脉枢纽"}
    ],
    "links": [
        {"source": "打螺丝-💗写意", "target": "吾生有涯", "type": "捧哏与逗哏", "strength": 8},
        {"source": "打螺丝-💗写意", "target": "Kerwin", "type": "股市搭子", "strength": 6},
        {"source": "Tina", "target": "上海-IT-刃心", "type": "相亲中介", "strength": 7},
        {"source": "长沙群-雨上", "target": "🐽", "type": "姐妹淘", "strength": 8},
        {"source": "🐽", "target": "淡写～～", "type": "过来人", "strength": 6},
        {"source": "吾生有涯", "target": "Kerwin", "type": "基友", "strength": 7},
        {"source": "乐儿💕", "target": "Kerwin", "type": "股市搭子", "strength": 5},
        {"source": "麦哥2025", "target": "打螺丝-💗写意", "type": "故事互投", "strength": 5},
        {"source": "小卒", "target": "吾生有涯", "type": "捧哏与逗哏", "strength": 4},
        {"source": "长沙群-雨上", "target": "打螺丝-💗写意", "type": "欢喜冤家", "strength": 5},
        {"source": "上海亚牌照明", "target": "吾生有涯", "type": "基友", "strength": 6},
        {"source": "Tina", "target": "打螺丝-💗写意", "type": "姐妹淘", "strength": 5}
    ]
}
rel_json = json.dumps(rel_data, ensure_ascii=False)

# ============================================================
# Word Cloud Data
# ============================================================
word_cloud = [
    ["结婚", 82], ["彩礼", 72], ["股市", 68], ["深圳", 65],
    ["长沙", 62], ["房价", 55], ["合租", 52], ["半导体", 48],
    ["长鑫", 45], ["裁员", 42], ["买房", 40], ["科技", 38],
    ["返湘", 36], ["相亲", 34], ["程序员", 32], ["养娃", 30],
    ["行情", 28], ["海景房", 26], ["租客", 24], ["老板", 22],
    ["失业", 20], ["职场", 18], ["婆媳", 16], ["IT", 15],
    ["医疗", 14]
]
wc_json = json.dumps(word_cloud, ensure_ascii=False)

# ============================================================
# Read template and fill
# ============================================================
template_path = os.path.join(skill_dir, "assets", "report-template.html")
with open(template_path, 'r') as f:
    html = f.read()

# Summary blurb
summary_blurb = "3741条消息烧穿本周期，从长鑫上市赚2万到26岁女孩的婚恋急诊室，从海景房11万70平的泡沫到衡阳火车站的武警执勤——长沙返湘群用股市焦虑和婚恋困惑撑起了本周最硬核的群聊生态。"

# Full summary section
full_summary_cards = summary_cards

replacements = {
    '{{GROUP_NAME}}': '长沙长沙（返湘1群）',
    '{{REPORT_TYPE}}': '周报',
    '{{DATE_RANGE}}': '2026-07-23 ~ 2026-07-30',
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
output_path = "/Users/jiangtao/ai/wx周报/report/长沙长沙（返湘1群）/长沙长沙（返湘1群）_20260730.html"
with open(output_path, 'w') as f:
    f.write(html)

file_size = os.path.getsize(output_path)
print(f"Report saved to: {output_path}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
