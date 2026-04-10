#!/usr/bin/env python3
"""
SBTI 人格测试 - Python 实现
基于 B站@蛆肉儿串儿 的 SBTI 测试
"""

import json
import sys
from dataclasses import dataclass
from typing import Optional

# ============ 维度元数据 ============
DIMENSION_META = {
    "S1": {"name": "S1 自尊自信", "model": "自我模型"},
    "S2": {"name": "S2 自我清晰度", "model": "自我模型"},
    "S3": {"name": "S3 核心价值", "model": "自我模型"},
    "E1": {"name": "E1 依恋安全感", "model": "情感模型"},
    "E2": {"name": "E2 情感投入度", "model": "情感模型"},
    "E3": {"name": "E3 边界与依赖", "model": "情感模型"},
    "A1": {"name": "A1 世界观倾向", "model": "态度模型"},
    "A2": {"name": "A2 规则与灵活度", "model": "态度模型"},
    "A3": {"name": "A3 人生意义感", "model": "态度模型"},
    "Ac1": {"name": "Ac1 动机导向", "model": "行动驱力模型"},
    "Ac2": {"name": "Ac2 决策风格", "model": "行动驱力模型"},
    "Ac3": {"name": "Ac3 执行模式", "model": "行动驱力模型"},
    "So1": {"name": "So1 社交主动性", "model": "社交模型"},
    "So2": {"name": "So2 人际边界感", "model": "社交模型"},
    "So3": {"name": "So3 表达与真实度", "model": "社交模型"},
}

DIMENSION_ORDER = ["S1","S2","S3","E1","E2","E3","A1","A2","A3","Ac1","Ac2","Ac3","So1","So2","So3"]

# ============ 题库 ============
QUESTIONS = [
    {"id": "q1", "dim": "S1", "text": "我不够好，周围的人都比我优秀", "options": [{"label": "确实", "value": 1}, {"label": "有时", "value": 2}, {"label": "不是", "value": 3}]},
    {"id": "q2", "dim": "S1", "text": "我不仅是屌丝，我还是joker...（省略表述）", "options": [{"label": "我哭了。。", "value": 1}, {"label": "这是什么。。", "value": 2}, {"label": "这不是我！", "value": 3}]},
    {"id": "q3", "dim": "S2", "text": "我很清楚真正的自己是什么样的", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q4", "dim": "S2", "text": "我内心有真正追求的东西", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q5", "dim": "S3", "text": "我一定要不断往上爬、变得更厉害", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q6", "dim": "S3", "text": "外人的评价对我来说无所吊谓。", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q7", "dim": "E1", "text": "对象超过5小时没回消息，说自己窜稀了，你会怎么想？", "options": [{"label": "拉稀不可能5小时，也许ta隐瞒了我。", "value": 1}, {"label": "在信任和怀疑之间摇摆。", "value": 2}, {"label": "也许今天ta真的不太舒服。", "value": 3}]},
    {"id": "q8", "dim": "E1", "text": "我在感情里经常担心被对方抛弃", "options": [{"label": "是的", "value": 1}, {"label": "偶尔", "value": 2}, {"label": "不是", "value": 3}]},
    {"id": "q9", "dim": "E2", "text": "我对天发誓，我对待每一份感情都是认真的！", "options": [{"label": "并没有", "value": 1}, {"label": "也许？", "value": 2}, {"label": "是的！（问心无愧骄傲脸）", "value": 3}]},
    {"id": "q10", "dim": "E2", "text": "你的恋爱对象是一个完美的人，此时你会？", "options": [{"label": "就算ta再优秀我也不会陷入太深。", "value": 1}, {"label": "会介于A和C之间。", "value": 2}, {"label": "会非常珍惜ta，也许会变成恋爱脑。", "value": 3}]},
    {"id": "q11", "dim": "E3", "text": "恋爱后，对象非常黏人，你作何感想？", "options": [{"label": "那很爽了", "value": 1}, {"label": "都行无所谓", "value": 2}, {"label": "我更喜欢保留独立空间", "value": 3}]},
    {"id": "q12", "dim": "E3", "text": "我在任何关系里都很重视个人空间", "options": [{"label": "我更喜欢依赖与被依赖", "value": 1}, {"label": "看情况", "value": 2}, {"label": "是的！（斩钉截铁地说道）", "value": 3}]},
    {"id": "q13", "dim": "A1", "text": "大多数人是善良的", "options": [{"label": "其实邪恶的人心比世界上的痔疮更多。", "value": 1}, {"label": "也许吧。", "value": 2}, {"label": "是的，我愿相信好人更多。", "value": 3}]},
    {"id": "q14", "dim": "A1", "text": "你走在街上，一位萌萌的小女孩递给你一根棒棒糖，此时你作何感想？", "options": [{"label": "呜呜她真好真可爱！", "value": 3}, {"label": "一脸懵逼，作挠头状", "value": 2}, {"label": "这也许是一种新型诈骗？", "value": 1}]},
    {"id": "q15", "dim": "A2", "text": "快考试了，学校规定必须上晚自习，但今晚你约了女/男神一起玩游戏，你怎么办？", "options": [{"label": "翘了！反正就一次！", "value": 1}, {"label": "干脆请个假吧。", "value": 2}, {"label": "都快考试了还去啥。", "value": 3}]},
    {"id": "q16", "dim": "A2", "text": "我喜欢打破常规，不喜欢被束缚", "options": [{"label": "认同", "value": 1}, {"label": "保持中立", "value": 2}, {"label": "不认同", "value": 3}]},
    {"id": "q17", "dim": "A3", "text": "我做事通常有目标。", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q18", "dim": "A3", "text": "突然某一天，我意识到人生哪有什么他妈的狗屁意义...", "options": [{"label": "是这样的。", "value": 1}, {"label": "也许是，也许不是。", "value": 2}, {"label": "这简直是胡扯", "value": 3}]},
    {"id": "q19", "dim": "Ac1", "text": "我做事主要为了取得成果和进步，而不是避免麻烦和风险。", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q20", "dim": "Ac1", "text": "你因便秘坐在马桶上（已长达30分钟），拉不出很难受。此时你更像", "options": [{"label": "再坐三十分钟看看。", "value": 1}, {"label": "用力拍打自己的屁股并说：死屁股，快拉啊！", "value": 2}, {"label": "使用开塞露。", "value": 3}]},
    {"id": "q21", "dim": "Ac2", "text": "我做决定比较果断，不喜欢犹豫", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
    {"id": "q22", "dim": "Ac2", "text": "此题没有题目，请盲选", "options": [{"label": "反复思考后感觉应该选A？", "value": 1}, {"label": "啊，要不选B？", "value": 2}, {"label": "不会就选C？", "value": 3}]},
    {"id": "q23", "dim": "Ac3", "text": "别人说你\"执行力强\"，你内心更接近哪句？", "options": [{"label": "我被逼到最后确实执行力超强。。。", "value": 1}, {"label": "啊，有时候吧。", "value": 2}, {"label": "是的，事情本来就该被推进", "value": 3}]},
    {"id": "q24", "dim": "Ac3", "text": "我做事常常有计划，____", "options": [{"label": "然而计划不如变化快。", "value": 1}, {"label": "有时能完成，有时不能。", "value": 2}, {"label": "我讨厌被打破计划。", "value": 3}]},
    {"id": "q25", "dim": "So1", "text": "你因玩游戏结识许多网友，并被邀请线下见面，你的想法是？", "options": [{"label": "网上口嗨下就算了，真见面还是有点忐忑。", "value": 1}, {"label": "见网友也挺好。", "value": 2}, {"label": "我会热情聊天，万一呢？", "value": 3}]},
    {"id": "q26", "dim": "So1", "text": "朋友带了ta的朋友一起来玩，你最可能的状态是", "options": [{"label": "对\"朋友的朋友\"天然有点距离感", "value": 1}, {"label": "看对方，能玩就玩。", "value": 2}, {"label": "朋友的朋友应该也算我的朋友！", "value": 3}]},
    {"id": "q27", "dim": "So2", "text": "我和人相处主打一个电子围栏，靠太近会自动报警。", "options": [{"label": "认同", "value": 3}, {"label": "中立", "value": 2}, {"label": "不认同", "value": 1}]},
    {"id": "q28", "dim": "So2", "text": "我渴望和我信任的人关系密切，熟得像失散多年的亲戚。", "options": [{"label": "认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "不认同", "value": 3}]},
    {"id": "q29", "dim": "So3", "text": "有时候你明明对一件事有不同的、负面的看法，但最后没说出来。多数情况下原因是：", "options": [{"label": "这种情况较少。", "value": 1}, {"label": "可能碍于情面或者关系。", "value": 2}, {"label": "不想让别人知道自己是个阴暗的人。", "value": 3}]},
    {"id": "q30", "dim": "So3", "text": "我在不同人面前会表现出不一样的自己", "options": [{"label": "不认同", "value": 1}, {"label": "中立", "value": 2}, {"label": "认同", "value": 3}]},
]

SPECIAL_QUESTIONS = [
    {"id": "drink_gate_q1", "special": True, "kind": "drink_gate", "text": "您平时有什么爱好？", "options": [{"label": "吃喝拉撒", "value": 1}, {"label": "艺术爱好", "value": 2}, {"label": "饮酒", "value": 3}, {"label": "健身", "value": 4}]},
    {"id": "drink_gate_q2", "special": True, "kind": "drink_trigger", "text": "您对饮酒的态度是？", "options": [{"label": "小酌怡情，喝不了太多。", "value": 1}, {"label": "我习惯将白酒灌在保温杯，当白开水喝。", "value": 2}]},
]

# ============ 人格类型库 ============
TYPE_LIBRARY = {
    "CTRL": {"code": "CTRL", "cn": "拿捏者", "intro": "怎么样，被我拿捏了吧？", "desc": "您是宇宙熵增定律的天然反抗者！CTRL人格，是行走的人形自走任务管理器。"},
    "ATM-er": {"code": "ATM-er", "cn": "送钱者", "intro": "你以为我很有钱吗？", "desc": "您或将成为金融界的未解之谜——支付时间、支付精力、支付耐心、支付一个本该安宁的夜晚。"},
    "Dior-s": {"code": "Dior-s", "cn": "屌丝", "intro": "等着我屌丝逆袭。", "desc": "Dior-s人格，是对当代消费主义陷阱和成功学PUA最彻底的蔑视。"},
    "BOSS": {"code": "BOSS", "cn": "领导者", "intro": "方向盘给我，我来开。", "desc": "BOSS是一个手里永远拿着方向盘的人。效率是他们的信仰，秩序是他们的呼吸。"},
    "THAN-K": {"code": "THAN-K", "cn": "感恩者", "intro": "我感谢苍天！我感谢大地！", "desc": "THAN-K拥有温润如玉的性格和海纳百川的胸怀。"},
    "OH-NO": {"code": "OH-NO", "cn": "哦不人", "intro": "哦不！我怎么会是这个人格？！", "desc": "当普通人看到一个杯子放在桌沿，哦不人看到的是一场灾难史诗。"},
    "GOGO": {"code": "GOGO", "cn": "行者", "intro": "gogogo~出发咯", "desc": "GOGO活在一个极致的\"所见即所得\"世界里。"},
    "SEXY": {"code": "SEXY", "cn": "尤物", "intro": "您就是天生的尤物！", "desc": "当您走进一个房间，照明系统会自动将您识别为天生的尤物。"},
    "LOVE-R": {"code": "LOVE-R", "cn": "多情者", "intro": "爱意太满，现实显得有点贫瘠。", "desc": "LOVE-R人格像远古神话时代幸存至今的珍稀物种。"},
    "MUM": {"code": "MUM", "cn": "妈妈", "intro": "或许...我可以叫你妈妈吗....?", "desc": "妈妈人格的底色是温柔，擅长感知情绪，具有超强共情力。"},
    "FAKE": {"code": "FAKE", "cn": "伪人", "intro": "已经，没有人类了。", "desc": "在社交场合，伪人是八面玲珑的存在，因为他们切换人格面具比切换手机输入法还快。"},
    "OJBK": {"code": "OJBK", "cn": "无所谓人", "intro": "我说随便，是真的随便。", "desc": "OJBK已经不是一种人格，而是一种统治哲学。"},
    "MALO": {"code": "MALO", "cn": "吗喽", "intro": "人生是个副本，而我只是一只吗喽。", "desc": "朋友，你不是\"童心未泯\"，你压根就没进化。"},
    "JOKE-R": {"code": "JOKE-R", "cn": "小丑", "intro": "原来我们都是小丑。", "desc": "JOKE-R人格不是一个\"人\"，更像一个把笑话穿在身上的小丑。"},
    "WOC!": {"code": "WOC!", "cn": "握草人", "intro": "卧槽，我怎么是这个人格？", "desc": "WOC!人拥有两种完全独立的操作系统。"},
    "THIN-K": {"code": "THIN-K", "cn": "思考者", "intro": "已深度思考100s。", "desc": "THIN-K人格的大脑长时间处于思考状态。"},
    "SHIT": {"code": "SHIT", "cn": "愤世者", "intro": "这个世界，构石一坨。", "desc": "SHIT的行为模式是一场惊天动地的悖论戏剧。"},
    "ZZZZ": {"code": "ZZZZ", "cn": "装死者", "intro": "我没死，我只是在睡觉。", "desc": "群里99+条消息您可以视而不见，但当最后通牒出现，您就真正爆发了。"},
    "POOR": {"code": "POOR", "cn": "贫困者", "intro": "我穷，但我很专。", "desc": "您不是资源少，你是把资源全部灌进了一个坑里。"},
    "MONK": {"code": "MONK", "cn": "僧人", "intro": "没有那种世俗的欲望。", "desc": "MONK已然看破红尘，不希望闲人来扰其清修。"},
    "IMSB": {"code": "IMSB", "cn": "傻者", "intro": "认真的么？我真的是傻逼么？", "desc": "IMSB人格的大脑里住着两个不死不休的究极战士。"},
    "SOLO": {"code": "SOLO", "cn": "孤儿", "intro": "我哭了，我怎么会是孤儿？", "desc": "孤儿的自我价值感偏低，因此有时主动疏远他人。"},
    "FUCK": {"code": "FUCK", "cn": "草者", "intro": "操！这是什么人格？", "desc": "人类文明城市里，出现了一株无法被任何除草剂杀死的人形野草。"},
    "DEAD": {"code": "DEAD", "cn": "死者", "intro": "我，还活着吗？", "desc": "死者已经看透了那些无意义的哲学思考。"},
    "IMFW": {"code": "IMFW", "cn": "废物", "intro": "我真的...是废物吗？", "desc": "废物的自尊通常有些脆弱，给废物一颗糖，他们会还你一个完全信任你的眼神。"},
    "HHHH": {"code": "HHHH", "cn": "傻乐者", "intro": "哈哈哈哈哈哈。", "desc": "由于您的思维回路过于清奇，标准人格库已全面崩溃。"},
    "DRUNK": {"code": "DRUNK", "cn": "酒鬼", "intro": "烈酒烧喉，不得不醉。", "desc": "您体内流淌的不是血液，是美味的五粮液！"},
}

# ============ 人格模式库 ============
NORMAL_TYPES = [
    {"code": "CTRL", "pattern": "HHH-HMH-MHH-HHH-MHM"},
    {"code": "ATM-er", "pattern": "HHH-HHM-HHH-HMH-MHL"},
    {"code": "Dior-s", "pattern": "MHM-MMH-MHM-HMH-LHL"},
    {"code": "BOSS", "pattern": "HHH-HMH-MMH-HHH-LHL"},
    {"code": "THAN-K", "pattern": "MHM-HMM-HHM-MMH-MHL"},
    {"code": "OH-NO", "pattern": "HHL-LMH-LHH-HHM-LHL"},
    {"code": "GOGO", "pattern": "HHM-HMH-MMH-HHH-MHM"},
    {"code": "SEXY", "pattern": "HMH-HHL-HMM-HMM-HLH"},
    {"code": "LOVE-R", "pattern": "MLH-LHL-HLH-MLM-MLH"},
    {"code": "MUM", "pattern": "MMH-MHL-HMM-LMM-HLL"},
    {"code": "FAKE", "pattern": "HLM-MML-MLM-MLM-HLH"},
    {"code": "OJBK", "pattern": "MMH-MMM-HML-LMM-MML"},
    {"code": "MALO", "pattern": "MLH-MHM-MLH-MLH-LMH"},
    {"code": "JOKE-R", "pattern": "LLH-LHL-LML-LLL-MLM"},
    {"code": "WOC!", "pattern": "HHL-HMH-MMH-HHM-LHH"},
    {"code": "THIN-K", "pattern": "HHL-HMH-MLH-MHM-LHH"},
    {"code": "SHIT", "pattern": "HHL-HLH-LMM-HHM-LHH"},
    {"code": "ZZZZ", "pattern": "MHL-MLH-LML-MML-LHM"},
    {"code": "POOR", "pattern": "HHL-MLH-LMH-HHH-LHL"},
    {"code": "MONK", "pattern": "HHL-LLH-LLM-MML-LHM"},
    {"code": "IMSB", "pattern": "LLM-LMM-LLL-LLL-MLM"},
    {"code": "SOLO", "pattern": "LML-LLH-LHL-LML-LHM"},
    {"code": "FUCK", "pattern": "MLL-LHL-LLM-MLL-HLH"},
    {"code": "DEAD", "pattern": "LLL-LLM-LML-LLL-LHM"},
    {"code": "IMFW", "pattern": "LLH-LHL-LML-LLL-MLL"},
]

# ============ 维度解读 ============
DIM_EXPLANATIONS = {
    "S1": {"L": "对自己下手比别人还狠，夸你两句你都想先验明真伪。", "M": "自信值随天气波动，顺风能飞，逆风先缩。", "H": "心里对自己大致有数，不太会被路人一句话打散。"},
    "S2": {"L": "内心频道雪花较多，常在\"我是谁\"里循环缓存。", "M": "平时还能认出自己，偶尔也会被情绪临时换号。", "H": "对自己的脾气、欲望和底线都算门儿清。"},
    "S3": {"L": "更在意舒服和安全，没必要天天给人生开冲刺模式。", "M": "想上进，也想躺会儿，价值排序经常内部开会。", "H": "很容易被目标、成长或某种重要信念推着往前。"},
    "E1": {"L": "感情里警报器灵敏，已读不回都能脑补到大结局。", "M": "一半信任，一半试探，感情里常在心里拉锯。", "H": "更愿意相信关系本身，不会被一点风吹草动吓散。"},
    "E2": {"L": "感情投入偏克制，心门不是没开，是门禁太严。", "M": "会投入，但会给自己留后手，不至于全盘梭哈。", "H": "一旦认定就容易认真，情绪和精力都给得很足。"},
    "E3": {"L": "容易黏人也容易被黏，关系里的温度感很重要。", "M": "亲密和独立都要一点，属于可调节型依赖。", "H": "空间感很重要，再爱也得留一块属于自己的地。"},
    "A1": {"L": "看世界自带防御滤镜，先怀疑，再靠近。", "M": "既不天真也不彻底阴谋论，观望是你的本能。", "H": "更愿意相信人性和善意，遇事不急着把世界判死刑。"},
    "A2": {"L": "规则能绕就绕，舒服和自由往往排在前面。", "M": "该守的时候守，该变通的时候也不死磕。", "H": "秩序感较强，能按流程来就不爱即兴炸场。"},
    "A3": {"L": "意义感偏低，容易觉得很多事都像在走过场。", "M": "偶尔有目标，偶尔也想摆烂，人生观处于半开机。", "H": "做事更有方向，知道自己大概要往哪边走。"},
    "Ac1": {"L": "做事先考虑别翻车，避险系统比野心更先启动。", "M": "有时想赢，有时只想别麻烦，动机比较混合。", "H": "更容易被成果、成长和推进感点燃。"},
    "Ac2": {"L": "做决定前容易多转几圈，脑内会议常常超时。", "M": "会想，但不至于想死机，属于正常犹豫。", "H": "拍板速度快，决定一下就不爱回头磨叽。"},
    "Ac3": {"L": "执行力和死线有深厚感情，越晚越像要觉醒。", "M": "能做，但状态看时机，偶尔稳偶尔摆。", "H": "推进欲比较强，事情不落地心里都像卡了根刺。"},
    "So1": {"L": "社交启动慢热，主动出击这事通常得攒半天气。", "M": "有人来就接，没人来也不硬凑，社交弹性一般。", "H": "更愿意主动打开场子，在人群里不太怕露头。"},
    "So2": {"L": "关系里更想亲近和融合，熟了就容易把人划进内圈。", "M": "既想亲近又想留缝，边界感看对象调节。", "H": "边界感偏强，靠太近会先本能性后退半步。"},
    "So3": {"L": "表达更直接，心里有啥基本不爱绕。", "M": "会看气氛说话，真实和体面通常各留一点。", "H": "对不同场景的自我切换更熟练，真实感会分层发放。"},
}

DRUNK_TRIGGER_QUESTION_ID = "drink_gate_q2"


def sum_to_level(score):
    """将维度得分转换为等级"""
    if score <= 3:
        return "L"
    if score == 4:
        return "M"
    return "H"


def level_num(level):
    """将等级转换为数值"""
    return {"L": 1, "M": 2, "H": 3}[level]


def parse_pattern(pattern):
    """解析模式字符串"""
    return list(pattern.replace("-", ""))


def compute_result(answers):
    """
    根据用户答案计算人格结果

    Args:
        answers: dict，键为问题ID，值为选择的值

    Returns:
        dict，包含计算结果
    """
    # 计算每个维度的原始分数
    raw_scores = {dim: 0 for dim in DIMENSION_META}

    for q in QUESTIONS:
        q_id = q["id"]
        dim = q["dim"]
        if q_id in answers:
            raw_scores[dim] += answers[q_id]

    # 转换为等级
    levels = {dim: sum_to_level(score) for dim, score in raw_scores.items()}

    # 构建用户向量
    user_vector = [level_num(levels[dim]) for dim in DIMENSION_ORDER]

    # 计算与人格类型的匹配度
    ranked = []
    for type_info in NORMAL_TYPES:
        vector = parse_pattern(type_info["pattern"])
        vector = [level_num(v) for v in vector]

        distance = 0
        exact = 0
        for i in range(len(vector)):
            diff = abs(user_vector[i] - vector[i])
            distance += diff
            if diff == 0:
                exact += 1

        similarity = max(0, round((1 - distance / 30) * 100))

        type_data = TYPE_LIBRARY[type_info["code"]]
        ranked.append({
            "code": type_info["code"],
            "cn": type_data["cn"],
            "distance": distance,
            "exact": exact,
            "similarity": similarity,
        })

    # 按距离升序、相似度降序排序
    ranked.sort(key=lambda x: (x["distance"], -x["similarity"]))

    best_normal = ranked[0]

    # 检查饮酒触发
    drunk_triggered = answers.get(DRUNK_TRIGGER_QUESTION_ID) == 2

    # 确定最终人格
    if drunk_triggered:
        final_type = TYPE_LIBRARY["DRUNK"]
        mode_kicker = "隐藏人格已激活"
        badge = "匹配度 100% · 酒精异常因子已接管"
        sub = "乙醇亲和性过强，系统已直接跳过常规人格审判。"
        special = True
        secondary_type = best_normal
    elif best_normal["similarity"] < 60:
        final_type = TYPE_LIBRARY["HHHH"]
        mode_kicker = "系统强制兜底"
        badge = f"标准人格库最高匹配仅 {best_normal['similarity']}%"
        sub = "标准人格库对你的脑回路集体罢工了。"
        special = True
        secondary_type = None
    else:
        final_type = TYPE_LIBRARY[best_normal["code"]]
        mode_kicker = "你的主类型"
        badge = f"匹配度 {best_normal['similarity']}% · 精准命中 {best_normal['exact']}/15 维"
        sub = "维度命中度较高，当前结果可视为你的第一人格画像。"
        special = False
        secondary_type = None

    # 构建结果
    result = {
        "final_type": {
            "code": final_type["code"],
            "cn": final_type["cn"],
            "intro": final_type["intro"],
            "desc": final_type["desc"],
        },
        "mode_kicker": mode_kicker,
        "badge": badge,
        "sub": sub,
        "special": special,
        "levels": levels,
        "raw_scores": raw_scores,
        "best_normal": best_normal if not drunk_triggered else None,
        "secondary_type": secondary_type,
        "image_path": f"./image/{final_type['code']}.png" if final_type["code"] not in ["Dior-s", "JOKE-R"] else f"./image/{final_type['code']}.jpg",
    }

    return result


def get_questions():
    """返回所有问题（用于对话式问答）"""
    return {
        "regular_questions": QUESTIONS,
        "special_questions": SPECIAL_QUESTIONS,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: sbti.py <command> [args]")
        print("Commands: questions, calc")
        sys.exit(1)

    command = sys.argv[1]

    if command == "questions":
        # 输出所有问题
        result = get_questions()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "calc":
        # 从 stdin 读取答案并计算结果
        input_data = sys.stdin.read()
        if input_data.strip():
            answers = json.loads(input_data)
            result = compute_result(answers)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("Error: No answers provided", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
