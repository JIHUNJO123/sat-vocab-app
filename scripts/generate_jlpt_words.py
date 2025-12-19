#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JLPT 단어 생성 스크립트
각 레벨별 빈출 단어를 생성하고 한국어, 중국어 번역을 포함합니다.
"""

import json
import os
from typing import List, Dict

# JLPT 빈출 단어 데이터베이스 (기본 단어들)
# 형식: (단어, 한자, 히라가나, 품사, 영어정의, 일본어예문, 영어정의번역, 영어예문번역, 한국어정의, 한국어예문, 중국어정의, 중국어예문)
JLPT_WORDS = {
    "N5": [
        # 기본 인사말 및 일상 단어
        ("あいさつ", "挨拶", "あいさつ", "noun", "greeting", "朝の挨拶をしました。", "greeting", "I said good morning.", "인사", "아침 인사를 했습니다。", "问候", "我打了早上的招呼。"),
        ("おはよう", "", "おはよう", "interjection", "good morning", "おはようございます。", "good morning", "Good morning.", "좋은 아침", "좋은 아침입니다.", "早上好", "早上好。"),
        ("こんにちは", "", "こんにちは", "interjection", "hello", "こんにちは、元気ですか。", "hello", "Hello, how are you?", "안녕하세요", "안녕하세요, 잘 지내세요?", "你好", "你好，你好吗？"),
        ("こんばんは", "", "こんばんは", "interjection", "good evening", "こんばんは。", "good evening", "Good evening.", "안녕하세요", "안녕하세요 (저녁).", "晚上好", "晚上好。"),
        ("さようなら", "さようなら", "さようなら", "interjection", "goodbye", "さようなら、また明日。", "goodbye", "Goodbye, see you tomorrow.", "안녕히 가세요", "안녕히 가세요, 내일 또 봐요.", "再见", "再见，明天见。"),
        ("ありがとう", "", "ありがとう", "interjection", "thank you", "ありがとうございます。", "thank you", "Thank you very much.", "감사합니다", "감사합니다.", "谢谢", "谢谢。"),
        ("すみません", "", "すみません", "interjection", "excuse me, sorry", "すみません、道を教えてください。", "excuse me", "Excuse me, could you tell me the way?", "죄송합니다", "죄송합니다, 길을 알려주세요.", "对不起", "对不起，请告诉我路。"),
        ("ごめんなさい", "", "ごめんなさい", "interjection", "I'm sorry", "ごめんなさい、遅れました。", "I'm sorry", "I'm sorry, I'm late.", "미안합니다", "미안합니다, 늦었습니다.", "对不起", "对不起，我迟到了。"),
        
        # 숫자
        ("いち", "一", "いち", "noun", "one", "一つください。", "one", "Please give me one.", "하나", "하나 주세요.", "一", "请给我一个。"),
        ("に", "二", "に", "noun", "two", "二つあります。", "two", "There are two.", "둘", "둘 있습니다.", "二", "有两个。"),
        ("さん", "三", "さん", "noun", "three", "三つ買いました。", "three", "I bought three.", "셋", "셋 샀습니다.", "三", "买了三个。"),
        ("よん", "四", "よん", "noun", "four", "四つ見ました。", "four", "I saw four.", "넷", "넷 봤습니다.", "四", "看了四个。"),
        ("ご", "五", "ご", "noun", "five", "五つ作りました。", "five", "I made five.", "다섯", "다섯 만들었습니다.", "五", "做了五个。"),
        ("ろく", "六", "ろく", "noun", "six", "六つあります。", "six", "There are six.", "여섯", "여섯 있습니다.", "六", "有六个。"),
        ("なな", "七", "なな", "noun", "seven", "七つ読みました。", "seven", "I read seven.", "일곱", "일곱 읽었습니다.", "七", "读了七个。"),
        ("はち", "八", "はち", "noun", "eight", "八つ書きました。", "eight", "I wrote eight.", "여덟", "여덟 썼습니다.", "八", "写了八个。"),
        ("きゅう", "九", "きゅう", "noun", "nine", "九つ聞きました。", "nine", "I heard nine.", "아홉", "아홉 들었습니다.", "九", "听了九个。"),
        ("じゅう", "十", "じゅう", "noun", "ten", "十個あります。", "ten", "There are ten.", "열", "열 개 있습니다.", "十", "有十个。"),
        
        # 일상 생활 단어
        ("みず", "水", "みず", "noun", "water", "水を飲みました。", "water", "I drank water.", "물", "물을 마셨습니다.", "水", "我喝了水。"),
        ("ごはん", "ご飯", "ごはん", "noun", "rice, meal", "ご飯を食べました。", "rice, meal", "I ate a meal.", "밥", "밥을 먹었습니다.", "饭", "我吃了饭。"),
        ("パン", "", "パン", "noun", "bread", "パンを買いました。", "bread", "I bought bread.", "빵", "빵을 샀습니다.", "面包", "我买了面包。"),
        ("りんご", "林檎", "りんご", "noun", "apple", "りんごが好きです。", "apple", "I like apples.", "사과", "사과를 좋아합니다.", "苹果", "我喜欢苹果。"),
        ("くるま", "車", "くるま", "noun", "car", "車に乗りました。", "car", "I got in the car.", "자동차", "자동차를 탔습니다.", "汽车", "我坐了汽车。"),
        ("でんしゃ", "電車", "でんしゃ", "noun", "train", "電車で行きます。", "train", "I go by train.", "전철", "전철로 갑니다.", "电车", "我坐电车去。"),
        ("がっこう", "学校", "がっこう", "noun", "school", "学校に行きます。", "school", "I go to school.", "학교", "학교에 갑니다.", "学校", "我去学校。"),
        ("いえ", "家", "いえ", "noun", "house", "家に帰ります。", "house", "I return home.", "집", "집에 돌아갑니다.", "家", "我回家。"),
        ("へや", "部屋", "へや", "noun", "room", "部屋を掃除しました。", "room", "I cleaned the room.", "방", "방을 청소했습니다.", "房间", "我打扫了房间。"),
        ("つくえ", "机", "つくえ", "noun", "desk", "机の上に本があります。", "desk", "There is a book on the desk.", "책상", "책상 위에 책이 있습니다.", "桌子", "桌子上有书。"),
        
        # 동사
        ("たべる", "食べる", "たべる", "verb", "to eat", "ご飯を食べます。", "to eat", "I eat a meal.", "먹다", "밥을 먹습니다.", "吃", "我吃饭。"),
        ("のむ", "飲む", "のむ", "verb", "to drink", "お茶を飲みます。", "to drink", "I drink tea.", "마시다", "차를 마십니다.", "喝", "我喝茶。"),
        ("みる", "見る", "みる", "verb", "to see, to watch", "テレビを見ます。", "to see, to watch", "I watch TV.", "보다", "텔레비전을 봅니다.", "看", "我看电视。"),
        ("きく", "聞く", "きく", "verb", "to listen", "音楽を聞きます。", "to listen", "I listen to music.", "듣다", "음악을 듣습니다.", "听", "我听音乐。"),
        ("よむ", "読む", "よむ", "verb", "to read", "本を読みます。", "to read", "I read a book.", "읽다", "책을 읽습니다.", "读", "我读书。"),
        ("かく", "書く", "かく", "verb", "to write", "手紙を書きます。", "to write", "I write a letter.", "쓰다", "편지를 씁니다.", "写", "我写信。"),
        ("はなす", "話す", "はなす", "verb", "to speak", "日本語を話します。", "to speak", "I speak Japanese.", "말하다", "일본어를 말합니다.", "说", "我说日语。"),
        ("いく", "行く", "いく", "verb", "to go", "学校に行きます。", "to go", "I go to school.", "가다", "학교에 갑니다.", "去", "我去学校。"),
        ("くる", "来る", "くる", "verb", "to come", "日本に来ました。", "to come", "I came to Japan.", "오다", "일본에 왔습니다.", "来", "我来到了日本。"),
        ("かえる", "帰る", "かえる", "verb", "to return", "家に帰ります。", "to return", "I return home.", "돌아가다", "집에 돌아갑니다.", "回", "我回家。"),
        
        # 형용사
        ("おおきい", "大きい", "おおきい", "adjective", "big", "大きい家です。", "big", "It's a big house.", "큰", "큰 집입니다.", "大的", "是大房子。"),
        ("ちいさい", "小さい", "ちいさい", "adjective", "small", "小さい犬です。", "small", "It's a small dog.", "작은", "작은 개입니다.", "小的", "是小狗。"),
        ("たかい", "高い", "たかい", "adjective", "expensive, high", "高い山です。", "expensive, high", "It's a high mountain.", "비싼, 높은", "높은 산입니다.", "贵的, 高的", "是高山。"),
        ("やすい", "安い", "やすい", "adjective", "cheap, low", "安い服です。", "cheap", "It's cheap clothes.", "싼", "싼 옷입니다.", "便宜的", "是便宜的衣服。"),
        ("あたらしい", "新しい", "あたらしい", "adjective", "new", "新しい車です。", "new", "It's a new car.", "새로운", "새로운 자동차입니다.", "新的", "是新车。"),
        ("ふるい", "古い", "ふるい", "adjective", "old", "古い建物です。", "old", "It's an old building.", "오래된", "오래된 건물입니다.", "旧的", "是旧建筑。"),
        ("あつい", "暑い", "あつい", "adjective", "hot", "暑い夏です。", "hot", "It's a hot summer.", "덥다", "덥은 여름입니다.", "热的", "是炎热的夏天。"),
        ("さむい", "寒い", "さむい", "adjective", "cold", "寒い冬です。", "cold", "It's a cold winter.", "춥다", "추운 겨울입니다.", "冷的", "是寒冷的冬天。"),
        ("あたたかい", "暖かい", "あたたかい", "adjective", "warm", "暖かい春です。", "warm", "It's a warm spring.", "따뜻한", "따뜻한 봄입니다.", "温暖的", "是温暖的春天。"),
        ("すずしい", "涼しい", "すずしい", "adjective", "cool", "涼しい秋です。", "cool", "It's a cool autumn.", "시원한", "시원한 가을입니다.", "凉爽的", "是凉爽的秋天。"),
        
        # 시간 관련
        ("きょう", "今日", "きょう", "noun", "today", "今日は月曜日です。", "today", "Today is Monday.", "오늘", "오늘은 월요일입니다.", "今天", "今天是星期一。"),
        ("きのう", "昨日", "きのう", "noun", "yesterday", "昨日は日曜日でした。", "yesterday", "Yesterday was Sunday.", "어제", "어제는 일요일이었습니다.", "昨天", "昨天是星期日。"),
        ("あした", "明日", "あした", "noun", "tomorrow", "明日は火曜日です。", "tomorrow", "Tomorrow is Tuesday.", "내일", "내일은 화요일입니다.", "明天", "明天是星期二。"),
        ("いま", "今", "いま", "noun", "now", "今何時ですか。", "now", "What time is it now?", "지금", "지금 몇 시입니까?", "现在", "现在几点了？"),
        ("じかん", "時間", "じかん", "noun", "time, hour", "時間がありません。", "time", "I don't have time.", "시간", "시간이 없습니다.", "时间", "我没有时间。"),
        ("ばん", "晩", "ばん", "noun", "evening", "晩ご飯を食べました。", "evening", "I ate dinner.", "저녁", "저녁을 먹었습니다.", "晚上", "我吃了晚饭。"),
        ("よる", "夜", "よる", "noun", "night", "夜遅くまで働きました。", "night", "I worked late into the night.", "밤", "밤늦게까지 일했습니다.", "夜晚", "我工作到深夜。"),
        ("あさ", "朝", "あさ", "noun", "morning", "朝早く起きました。", "morning", "I woke up early in the morning.", "아침", "아침 일찍 일어났습니다.", "早晨", "我早上起得很早。"),
        
        # 가족/사람
        ("ひと", "人", "ひと", "noun", "person", "あの人は誰ですか。", "person", "Who is that person?", "사람", "그 사람은 누구입니까?", "人", "那个人是谁？"),
        ("ともだち", "友達", "ともだち", "noun", "friend", "友達と遊びました。", "friend", "I played with my friend.", "친구", "친구와 놀았습니다.", "朋友", "我和朋友一起玩了。"),
        ("かぞく", "家族", "かぞく", "noun", "family", "家族と一緒に住んでいます。", "family", "I live with my family.", "가족", "가족과 함께 살고 있습니다.", "家庭", "我和家人住在一起。"),
        ("おとうさん", "お父さん", "おとうさん", "noun", "father", "お父さんは会社員です。", "father", "My father is a company employee.", "아버지", "아버지는 회사원입니다.", "父亲", "我父亲是公司职员。"),
        ("おかあさん", "お母さん", "おかあさん", "noun", "mother", "お母さんは料理が上手です。", "mother", "My mother is good at cooking.", "어머니", "어머니는 요리를 잘하십니다.", "母亲", "我母亲很会做饭。"),
        
        # 신체 부위
        ("め", "目", "め", "noun", "eye", "目が痛いです。", "eye", "My eye hurts.", "눈", "눈이 아픕니다.", "眼睛", "我的眼睛疼。"),
        ("みみ", "耳", "みみ", "noun", "ear", "耳を聞いてください。", "ear", "Please listen.", "귀", "귀를 기울이세요.", "耳朵", "请仔细听。"),
        ("はな", "鼻", "はな", "noun", "nose", "鼻が高いです。", "nose", "I have a high nose.", "코", "코가 높습니다.", "鼻子", "我的鼻子很高。"),
        ("て", "手", "て", "noun", "hand", "手を洗いました。", "hand", "I washed my hands.", "손", "손을 씻었습니다.", "手", "我洗了手。"),
        ("かお", "顔", "かお", "noun", "face", "顔が赤いです。", "face", "My face is red.", "얼굴", "얼굴이 빨갛습니다.", "脸", "我的脸红了。"),
        
        # 색깔
        ("あお", "青", "あお", "noun", "blue", "青い空です。", "blue", "It's a blue sky.", "파란색", "파란 하늘입니다.", "蓝色", "是蓝色的天空。"),
        ("あか", "赤", "あか", "noun", "red", "赤い花です。", "red", "It's a red flower.", "빨간색", "빨간 꽃입니다.", "红色", "是红色的花。"),
        ("しろ", "白", "しろ", "noun", "white", "白い紙です。", "white", "It's white paper.", "흰색", "흰 종이입니다.", "白色", "是白色的纸。"),
        ("くろ", "黒", "くろ", "noun", "black", "黒い車です。", "black", "It's a black car.", "검은색", "검은 자동차입니다.", "黑色", "是黑色的汽车。"),
        ("きいろ", "黄色", "きいろ", "noun", "yellow", "黄色いバナナです。", "yellow", "It's a yellow banana.", "노란색", "노란 바나나입니다.", "黄色", "是黄色的香蕉。"),
        
        # 동작 동사 추가
        ("ねる", "寝る", "ねる", "verb", "to sleep", "早く寝ます。", "to sleep", "I go to bed early.", "자다", "일찍 잡니다.", "睡觉", "我早睡。"),
        ("おきる", "起きる", "おきる", "verb", "to wake up", "朝6時に起きます。", "to wake up", "I wake up at 6 AM.", "일어나다", "아침 6시에 일어납니다.", "起床", "我早上6点起床。"),
        ("はたらく", "働く", "はたらく", "verb", "to work", "会社で働きます。", "to work", "I work at a company.", "일하다", "회사에서 일합니다.", "工作", "我在公司工作。"),
        ("べんきょうする", "勉強する", "べんきょうする", "verb", "to study", "日本語を勉強します。", "to study", "I study Japanese.", "공부하다", "일본어를 공부합니다.", "学习", "我学习日语。"),
        ("かう", "買う", "かう", "verb", "to buy", "本を買いました。", "to buy", "I bought a book.", "사다", "책을 샀습니다.", "买", "我买了一本书。"),
        ("うる", "売る", "うる", "verb", "to sell", "車を売りました。", "to sell", "I sold my car.", "팔다", "자동차를 팔았습니다.", "卖", "我卖了我的车。"),
        ("つくる", "作る", "つくる", "verb", "to make", "料理を作ります。", "to make", "I make food.", "만들다", "요리를 만듭니다.", "做", "我做饭。"),
        ("わかる", "分かる", "わかる", "verb", "to understand", "日本語が分かります。", "to understand", "I understand Japanese.", "이해하다", "일본어를 이해합니다.", "理解", "我理解日语。"),
        ("しる", "知る", "しる", "verb", "to know", "その人を知っています。", "to know", "I know that person.", "알다", "그 사람을 알고 있습니다.", "知道", "我认识那个人。"),
        
        # 형용사 추가
        ("いい", "良い", "いい", "adjective", "good", "いい天気です。", "good", "It's good weather.", "좋은", "좋은 날씨입니다.", "好的", "是好天气。"),
        ("わるい", "悪い", "わるい", "adjective", "bad", "悪い天気です。", "bad", "It's bad weather.", "나쁜", "나쁜 날씨입니다.", "坏的", "是坏天气。"),
        ("はやい", "早い", "はやい", "adjective", "early, fast", "早く起きました。", "early", "I woke up early.", "이른, 빠른", "일찍 일어났습니다.", "早的", "我起得很早。"),
        ("おそい", "遅い", "おそい", "adjective", "late, slow", "遅く帰りました。", "late", "I came home late.", "늦은, 느린", "늦게 돌아왔습니다.", "晚的", "我回家晚了。"),
        ("おもしろい", "面白い", "おもしろい", "adjective", "interesting", "面白い本です。", "interesting", "It's an interesting book.", "재미있는", "재미있는 책입니다.", "有趣的", "是一本有趣的书。"),
        ("たのしい", "楽しい", "たのしい", "adjective", "fun, enjoyable", "楽しい旅行でした。", "fun", "It was a fun trip.", "즐거운", "즐거운 여행이었습니다.", "愉快的", "是一次愉快的旅行。"),
        ("むずかしい", "難しい", "むずかしい", "adjective", "difficult", "難しい問題です。", "difficult", "It's a difficult problem.", "어려운", "어려운 문제입니다.", "困难的", "是一个困难的问题。"),
        ("やさしい", "易しい", "やさしい", "adjective", "easy", "易しい問題です。", "easy", "It's an easy problem.", "쉬운", "쉬운 문제입니다.", "容易的", "是一个容易的问题。"),
        
        # 장소/위치
        ("ところ", "所", "ところ", "noun", "place", "静かな所です。", "place", "It's a quiet place.", "장소", "조용한 장소입니다.", "地方", "是一个安静的地方。"),
        ("まち", "町", "まち", "noun", "town", "小さな町です。", "town", "It's a small town.", "마을", "작은 마을입니다.", "城镇", "是一个小城镇。"),
        ("みせ", "店", "みせ", "noun", "shop, store", "本屋に行きました。", "shop", "I went to a bookstore.", "가게", "서점에 갔습니다.", "商店", "我去了书店。"),
        ("びょういん", "病院", "びょういん", "noun", "hospital", "病院に行きました。", "hospital", "I went to the hospital.", "병원", "병원에 갔습니다.", "医院", "我去了医院。"),
        ("ゆうびんきょく", "郵便局", "ゆうびんきょく", "noun", "post office", "郵便局で手紙を出しました。", "post office", "I sent a letter at the post office.", "우체국", "우체국에서 편지를 보냈습니다.", "邮局", "我在邮局寄了信。"),
        ("ぎんこう", "銀行", "ぎんこう", "noun", "bank", "銀行でお金を下ろしました。", "bank", "I withdrew money at the bank.", "은행", "은행에서 돈을 뽑았습니다.", "银行", "我在银行取了钱。"),
        
        # 음식
        ("さかな", "魚", "さかな", "noun", "fish", "魚を食べました。", "fish", "I ate fish.", "생선", "생선을 먹었습니다.", "鱼", "我吃了鱼。"),
        ("にく", "肉", "にく", "noun", "meat", "肉が好きです。", "meat", "I like meat.", "고기", "고기를 좋아합니다.", "肉", "我喜欢肉。"),
        ("やさい", "野菜", "やさい", "noun", "vegetable", "野菜を買いました。", "vegetable", "I bought vegetables.", "채소", "채소를 샀습니다.", "蔬菜", "我买了蔬菜。"),
        ("たまご", "卵", "たまご", "noun", "egg", "卵を食べました。", "egg", "I ate an egg.", "달걀", "달걀을 먹었습니다.", "鸡蛋", "我吃了鸡蛋。"),
        ("おちゃ", "お茶", "おちゃ", "noun", "tea", "お茶を飲みました。", "tea", "I drank tea.", "차", "차를 마셨습니다.", "茶", "我喝了茶。"),
        ("コーヒー", "", "コーヒー", "noun", "coffee", "コーヒーを飲みます。", "coffee", "I drink coffee.", "커피", "커피를 마십니다.", "咖啡", "我喝咖啡。"),
        
        # 옷/물건
        ("ふく", "服", "ふく", "noun", "clothes", "新しい服を買いました。", "clothes", "I bought new clothes.", "옷", "새 옷을 샀습니다.", "衣服", "我买了新衣服。"),
        ("くつ", "靴", "くつ", "noun", "shoes", "靴を履きました。", "shoes", "I put on shoes.", "신발", "신발을 신었습니다.", "鞋子", "我穿上了鞋子。"),
        ("かばん", "", "かばん", "noun", "bag", "かばんを持ちました。", "bag", "I carried a bag.", "가방", "가방을 들었습니다.", "包", "我拿了一个包。"),
        ("とけい", "時計", "とけい", "noun", "clock, watch", "時計を見ました。", "clock", "I looked at the clock.", "시계", "시계를 봤습니다.", "钟表", "我看了钟表。"),
        ("でんわ", "電話", "でんわ", "noun", "telephone", "電話をかけました。", "telephone", "I made a phone call.", "전화", "전화를 걸었습니다.", "电话", "我打了电话。"),
        
        # 날씨/자연
        ("てんき", "天気", "てんき", "noun", "weather", "いい天気です。", "weather", "It's good weather.", "날씨", "좋은 날씨입니다.", "天气", "是好天气。"),
        ("はる", "春", "はる", "noun", "spring", "春が来ました。", "spring", "Spring has come.", "봄", "봄이 왔습니다.", "春天", "春天来了。"),
        ("なつ", "夏", "なつ", "noun", "summer", "夏は暑いです。", "summer", "Summer is hot.", "여름", "여름은 덥습니다.", "夏天", "夏天很热。"),
        ("あき", "秋", "あき", "noun", "autumn", "秋は涼しいです。", "autumn", "Autumn is cool.", "가을", "가을은 시원합니다.", "秋天", "秋天很凉爽。"),
        ("ふゆ", "冬", "ふゆ", "noun", "winter", "冬は寒いです。", "winter", "Winter is cold.", "겨울", "겨울은 춥습니다.", "冬天", "冬天很冷。"),
        
        # 감정/상태
        ("うれしい", "嬉しい", "うれしい", "adjective", "happy", "嬉しいです。", "happy", "I'm happy.", "기쁜", "기쁩니다.", "高兴的", "我很高兴。"),
        ("かなしい", "悲しい", "かなしい", "adjective", "sad", "悲しいです。", "sad", "I'm sad.", "슬픈", "슬픕니다.", "悲伤的", "我很悲伤。"),
        
        # 기타 중요 단어
        ("ことば", "言葉", "ことば", "noun", "word, language", "日本語の言葉を覚えます。", "word", "I memorize Japanese words.", "단어", "일본어 단어를 외웁니다.", "词语", "我记日语单词。"),
        ("いみ", "意味", "いみ", "noun", "meaning", "この言葉の意味が分かりません。", "meaning", "I don't understand the meaning of this word.", "의미", "이 말의 의미를 모르겠습니다.", "意思", "我不懂这个词的意思。"),
        ("しつもん", "質問", "しつもん", "noun", "question", "質問があります。", "question", "I have a question.", "질문", "질문이 있습니다.", "问题", "我有一个问题。"),
        ("こたえ", "答え", "こたえ", "noun", "answer", "答えを教えてください。", "answer", "Please tell me the answer.", "답", "답을 알려주세요.", "答案", "请告诉我答案。"),
    ],
    
    "N4": [
        # 더 복잡한 일상 단어
        ("あいまい", "曖昧", "あいまい", "adjective", "vague, ambiguous", "曖昧な返事をしました。", "vague, ambiguous", "I gave a vague answer.", "모호한", "모호한 답변을 했습니다.", "模糊的", "我给出了模糊的回答。"),
        ("あがる", "上がる", "あがる", "verb", "to go up, to rise", "階段を上がりました。", "to go up", "I went up the stairs.", "오르다", "계단을 올랐습니다.", "上升", "我上了楼梯。"),
        ("あきらめる", "諦める", "あきらめる", "verb", "to give up", "諦めないでください。", "to give up", "Please don't give up.", "포기하다", "포기하지 마세요.", "放弃", "请不要放弃。"),
        ("あくしゅ", "握手", "あくしゅ", "noun", "handshake", "握手をしました。", "handshake", "We shook hands.", "악수", "악수를 했습니다.", "握手", "我们握了手。"),
        ("あくび", "", "あくび", "noun", "yawn", "あくびが出ました。", "yawn", "I yawned.", "하품", "하품이 나왔습니다.", "哈欠", "我打了个哈欠。"),
        ("あける", "開ける", "あける", "verb", "to open", "窓を開けました。", "to open", "I opened the window.", "열다", "창문을 열었습니다.", "打开", "我打开了窗户。"),
        ("あげる", "上げる", "あげる", "verb", "to give", "プレゼントを上げました。", "to give", "I gave a present.", "주다", "선물을 주었습니다.", "给", "我送了礼物。"),
        ("あさごはん", "朝ご飯", "あさごはん", "noun", "breakfast", "朝ご飯を食べました。", "breakfast", "I ate breakfast.", "아침 식사", "아침 식사를 했습니다.", "早餐", "我吃了早餐。"),
        ("あさって", "明後日", "あさって", "noun", "day after tomorrow", "明後日会いましょう。", "day after tomorrow", "Let's meet the day after tomorrow.", "모레", "모레 만나요.", "后天", "我们后天见吧。"),
        ("あし", "足", "あし", "noun", "foot, leg", "足が痛いです。", "foot, leg", "My leg hurts.", "발, 다리", "다리가 아픕니다.", "脚", "脚很疼。"),
        
        # N4 추가 빈출 단어
        ("あたたかい", "暖かい", "あたたかい", "adjective", "warm", "暖かい部屋です。", "warm", "It's a warm room.", "따뜻한", "따뜻한 방입니다.", "温暖的", "是温暖的房间。"),
        ("あつい", "厚い", "あつい", "adjective", "thick", "厚い本です。", "thick", "It's a thick book.", "두꺼운", "두꺼운 책입니다.", "厚的", "是一本厚书。"),
        ("うすい", "薄い", "うすい", "adjective", "thin", "薄い紙です。", "thin", "It's thin paper.", "얇은", "얇은 종이입니다.", "薄的", "是薄纸。"),
        ("おおい", "多い", "おおい", "adjective", "many, much", "人が多いです。", "many", "There are many people.", "많은", "사람이 많습니다.", "多的", "有很多人。"),
        ("すくない", "少ない", "すくない", "adjective", "few, little", "時間が少ないです。", "few", "There is little time.", "적은", "시간이 적습니다.", "少的", "时间很少。"),
        ("たかい", "高い", "たかい", "adjective", "expensive, high", "高い建物です。", "expensive", "It's an expensive building.", "비싼", "비싼 건물입니다.", "贵的", "是昂贵的建筑。"),
        ("ひくい", "低い", "ひくい", "adjective", "low", "低い山です。", "low", "It's a low mountain.", "낮은", "낮은 산입니다.", "低的", "是低山。"),
        ("ながい", "長い", "ながい", "adjective", "long", "長い道です。", "long", "It's a long road.", "긴", "긴 길입니다.", "长的", "是长路。"),
        ("みじかい", "短い", "みじかい", "adjective", "short", "短い時間です。", "short", "It's a short time.", "짧은", "짧은 시간입니다.", "短的", "是短时间。"),
        ("ひろい", "広い", "ひろい", "adjective", "wide, spacious", "広い部屋です。", "wide", "It's a spacious room.", "넓은", "넓은 방입니다.", "宽的", "是宽敞的房间。"),
        ("せまい", "狭い", "せまい", "adjective", "narrow", "狭い道です。", "narrow", "It's a narrow road.", "좁은", "좁은 길입니다.", "窄的", "是窄路。"),
        ("かるい", "軽い", "かるい", "adjective", "light", "軽い荷物です。", "light", "It's light luggage.", "가벼운", "가벼운 짐입니다.", "轻的", "是轻行李。"),
        ("おもい", "重い", "おもい", "adjective", "heavy", "重い箱です。", "heavy", "It's a heavy box.", "무거운", "무거운 상자입니다.", "重的", "是重箱子。"),
        ("やわらかい", "柔らかい", "やわらかい", "adjective", "soft", "柔らかい布です。", "soft", "It's soft fabric.", "부드러운", "부드러운 천입니다.", "软的", "是软布。"),
        ("かたい", "硬い", "かたい", "adjective", "hard", "硬い石です。", "hard", "It's a hard stone.", "딱딱한", "딱딱한 돌입니다.", "硬的", "是硬石头。"),
        
        # N4 동사
        ("あらう", "洗う", "あらう", "verb", "to wash", "手を洗います。", "to wash", "I wash my hands.", "씻다", "손을 씻습니다.", "洗", "我洗手。"),
        ("うごく", "動く", "うごく", "verb", "to move", "車が動きます。", "to move", "The car moves.", "움직이다", "자동차가 움직입니다.", "移动", "汽车移动。"),
        ("うたう", "歌う", "うたう", "verb", "to sing", "歌を歌います。", "to sing", "I sing a song.", "노래하다", "노래를 부릅니다.", "唱歌", "我唱歌。"),
        ("おきる", "起きる", "おきる", "verb", "to wake up", "朝早く起きます。", "to wake up", "I wake up early.", "일어나다", "아침 일찍 일어납니다.", "起床", "我早起。"),
        ("おくる", "送る", "おくる", "verb", "to send", "手紙を送ります。", "to send", "I send a letter.", "보내다", "편지를 보냅니다.", "发送", "我寄信。"),
        ("おしえる", "教える", "おしえる", "verb", "to teach", "日本語を教えます。", "to teach", "I teach Japanese.", "가르치다", "일본어를 가르칩니다.", "教", "我教日语。"),
        ("おぼえる", "覚える", "おぼえる", "verb", "to remember", "単語を覚えます。", "to remember", "I remember words.", "기억하다", "단어를 기억합니다.", "记住", "我记单词。"),
        ("かえる", "変える", "かえる", "verb", "to change", "計画を変えます。", "to change", "I change the plan.", "바꾸다", "계획을 바꿉니다.", "改变", "我改变计划。"),
        ("きく", "聞く", "きく", "verb", "to listen, to ask", "音楽を聞きます。", "to listen", "I listen to music.", "듣다", "음악을 듣습니다.", "听", "我听音乐。"),
        ("きる", "切る", "きる", "verb", "to cut", "野菜を切ります。", "to cut", "I cut vegetables.", "자르다", "채소를 자릅니다.", "切", "我切蔬菜。"),
        ("こまる", "困る", "こまる", "verb", "to be troubled", "困っています。", "to be troubled", "I'm in trouble.", "곤란하다", "곤란합니다.", "困扰", "我很困扰。"),
        ("しる", "知る", "しる", "verb", "to know", "その人を知っています。", "to know", "I know that person.", "알다", "그 사람을 알고 있습니다.", "知道", "我认识那个人。"),
        ("すむ", "住む", "すむ", "verb", "to live", "東京に住んでいます。", "to live", "I live in Tokyo.", "살다", "도쿄에 살고 있습니다.", "住", "我住在东京。"),
        ("たつ", "立つ", "たつ", "verb", "to stand", "立ってください。", "to stand", "Please stand up.", "서다", "일어서세요.", "站", "请站起来。"),
        ("つかう", "使う", "つかう", "verb", "to use", "コンピューターを使います。", "to use", "I use a computer.", "사용하다", "컴퓨터를 사용합니다.", "使用", "我使用电脑。"),
        ("つく", "着く", "つく", "verb", "to arrive", "駅に着きました。", "to arrive", "I arrived at the station.", "도착하다", "역에 도착했습니다.", "到达", "我到达了车站。"),
        ("つれる", "連れる", "つれる", "verb", "to take along", "子供を連れます。", "to take along", "I take my child along.", "데려가다", "아이를 데려갑니다.", "带", "我带孩子。"),
        ("とまる", "止まる", "とまる", "verb", "to stop", "車が止まります。", "to stop", "The car stops.", "멈추다", "자동차가 멈춥니다.", "停止", "汽车停止。"),
        ("とる", "取る", "とる", "verb", "to take", "写真を取ります。", "to take", "I take a photo.", "찍다", "사진을 찍습니다.", "拍", "我拍照。"),
        ("なく", "泣く", "なく", "verb", "to cry", "子供が泣きます。", "to cry", "The child cries.", "울다", "아이가 웁니다.", "哭", "孩子哭。"),
        ("なくす", "無くす", "なくす", "verb", "to lose", "鍵を無くしました。", "to lose", "I lost my key.", "잃어버리다", "열쇠를 잃어버렸습니다.", "丢失", "我丢了钥匙。"),
        ("ならう", "習う", "ならう", "verb", "to learn", "ピアノを習います。", "to learn", "I learn piano.", "배우다", "피아노를 배웁니다.", "学习", "我学钢琴。"),
        ("のる", "乗る", "のる", "verb", "to ride", "電車に乗ります。", "to ride", "I ride the train.", "타다", "전철을 탑니다.", "乘坐", "我坐电车。"),
        ("はいる", "入る", "はいる", "verb", "to enter", "部屋に入ります。", "to enter", "I enter the room.", "들어가다", "방에 들어갑니다.", "进入", "我进入房间。"),
        ("はく", "履く", "はく", "verb", "to wear (shoes)", "靴を履きます。", "to wear", "I put on shoes.", "신다", "신발을 신습니다.", "穿", "我穿鞋。"),
        ("はしる", "走る", "はしる", "verb", "to run", "公園を走ります。", "to run", "I run in the park.", "달리다", "공원을 달립니다.", "跑", "我在公园跑步。"),
        ("はなす", "話す", "はなす", "verb", "to speak", "日本語を話します。", "to speak", "I speak Japanese.", "말하다", "일본어를 말합니다.", "说", "我说日语。"),
        ("ひく", "引く", "ひく", "verb", "to pull", "ドアを引きます。", "to pull", "I pull the door.", "당기다", "문을 당깁니다.", "拉", "我拉门。"),
        ("ふる", "降る", "ふる", "verb", "to fall (rain, snow)", "雨が降ります。", "to fall", "It rains.", "내리다", "비가 옵니다.", "下", "下雨。"),
        ("まつ", "待つ", "まつ", "verb", "to wait", "バスを待ちます。", "to wait", "I wait for the bus.", "기다리다", "버스를 기다립니다.", "等待", "我等公交车。"),
        ("むかう", "向かう", "むかう", "verb", "to head for", "駅に向かいます。", "to head for", "I head for the station.", "향하다", "역을 향합니다.", "前往", "我前往车站。"),
        ("やる", "遣る", "やる", "verb", "to do", "宿題をやります。", "to do", "I do homework.", "하다", "숙제를 합니다.", "做", "我做作业。"),
        ("よぶ", "呼ぶ", "よぶ", "verb", "to call", "友達を呼びます。", "to call", "I call my friend.", "부르다", "친구를 부릅니다.", "叫", "我叫朋友。"),
        ("よむ", "読む", "よむ", "verb", "to read", "本を読みます。", "to read", "I read a book.", "읽다", "책을 읽습니다.", "读", "我读书。"),
        ("わかる", "分かる", "わかる", "verb", "to understand", "日本語が分かります。", "to understand", "I understand Japanese.", "이해하다", "일본어를 이해합니다.", "理解", "我理解日语。"),
        ("わたす", "渡す", "わたす", "verb", "to hand over", "書類を渡します。", "to hand over", "I hand over the documents.", "건네주다", "서류를 건네줍니다.", "交给", "我交文件。"),
        ("わたる", "渡る", "わたる", "verb", "to cross", "道を渡ります。", "to cross", "I cross the road.", "건너다", "길을 건넙니다.", "过", "我过马路。"),
        
        # N4 명사
        ("あさ", "朝", "あさ", "noun", "morning", "朝早く起きます。", "morning", "I wake up early in the morning.", "아침", "아침 일찍 일어납니다.", "早晨", "我早上早起。"),
        ("あめ", "雨", "あめ", "noun", "rain", "雨が降っています。", "rain", "It's raining.", "비", "비가 내리고 있습니다.", "雨", "正在下雨。"),
        ("いけ", "池", "いけ", "noun", "pond", "池に魚がいます。", "pond", "There are fish in the pond.", "연못", "연못에 물고기가 있습니다.", "池塘", "池塘里有鱼。"),
        ("いし", "石", "いし", "noun", "stone", "石を拾いました。", "stone", "I picked up a stone.", "돌", "돌을 주웠습니다.", "石头", "我捡了石头。"),
        ("いす", "", "いす", "noun", "chair", "いすに座ります。", "chair", "I sit on a chair.", "의자", "의자에 앉습니다.", "椅子", "我坐在椅子上。"),
        ("いちばん", "一番", "いちばん", "noun", "number one, best", "一番好きです。", "best", "I like it best.", "가장", "가장 좋아합니다.", "最", "我最喜欢。"),
        ("いっしょ", "一緒", "いっしょ", "noun", "together", "一緒に行きましょう。", "together", "Let's go together.", "함께", "함께 가요.", "一起", "我们一起去吧。"),
        ("うみ", "海", "うみ", "noun", "sea", "海で泳ぎます。", "sea", "I swim in the sea.", "바다", "바다에서 수영합니다.", "海", "我在海里游泳。"),
        ("えき", "駅", "えき", "noun", "station", "駅で待ちます。", "station", "I wait at the station.", "역", "역에서 기다립니다.", "车站", "我在车站等。"),
        ("おかね", "お金", "おかね", "noun", "money", "お金を持っています。", "money", "I have money.", "돈", "돈을 가지고 있습니다.", "钱", "我有钱。"),
        ("おと", "音", "おと", "noun", "sound", "音が聞こえます。", "sound", "I can hear a sound.", "소리", "소리가 들립니다.", "声音", "我听到声音。"),
        ("おなか", "", "おなか", "noun", "stomach", "おなかが空きました。", "stomach", "I'm hungry.", "배", "배가 고픕니다.", "肚子", "我饿了。"),
        ("かがみ", "鏡", "かがみ", "noun", "mirror", "鏡を見ます。", "mirror", "I look in the mirror.", "거울", "거울을 봅니다.", "镜子", "我照镜子。"),
        ("かぜ", "風", "かぜ", "noun", "wind", "風が強いです。", "wind", "The wind is strong.", "바람", "바람이 강합니다.", "风", "风很大。"),
        ("かばん", "", "かばん", "noun", "bag", "かばんを持ちます。", "bag", "I carry a bag.", "가방", "가방을 듭니다.", "包", "我拿包。"),
        ("き", "木", "き", "noun", "tree", "木の下に座ります。", "tree", "I sit under a tree.", "나무", "나무 아래에 앉습니다.", "树", "我坐在树下。"),
        ("きもち", "気持ち", "きもち", "noun", "feeling", "気持ちがいいです。", "feeling", "I feel good.", "기분", "기분이 좋습니다.", "感觉", "我感觉很好。"),
        ("くうき", "空気", "くうき", "noun", "air", "空気がきれいです。", "air", "The air is clean.", "공기", "공기가 깨끗합니다.", "空气", "空气很干净。"),
        ("くすり", "薬", "くすり", "noun", "medicine", "薬を飲みます。", "medicine", "I take medicine.", "약", "약을 먹습니다.", "药", "我吃药。"),
        ("くつ", "靴", "くつ", "noun", "shoes", "靴を履きます。", "shoes", "I put on shoes.", "신발", "신발을 신습니다.", "鞋子", "我穿鞋。"),
        ("くに", "国", "くに", "noun", "country", "国に帰ります。", "country", "I return to my country.", "나라", "나라에 돌아갑니다.", "国家", "我回国家。"),
        ("くるま", "車", "くるま", "noun", "car", "車で行きます。", "car", "I go by car.", "자동차", "자동차로 갑니다.", "汽车", "我开车去。"),
        ("こえ", "声", "こえ", "noun", "voice", "声が聞こえます。", "voice", "I can hear a voice.", "목소리", "목소리가 들립니다.", "声音", "我听到声音。"),
        ("こと", "事", "こと", "noun", "thing, matter", "大切な事です。", "thing", "It's an important thing.", "일", "중요한 일입니다.", "事", "是重要的事。"),
        ("ことし", "今年", "ことし", "noun", "this year", "今年は2024年です。", "this year", "This year is 2024.", "올해", "올해는 2024년입니다.", "今年", "今年是2024年。"),
        ("ことば", "言葉", "ことば", "noun", "word", "言葉を覚えます。", "word", "I memorize words.", "단어", "단어를 외웁니다.", "词语", "我记单词。"),
        ("さかな", "魚", "さかな", "noun", "fish", "魚を食べます。", "fish", "I eat fish.", "생선", "생선을 먹습니다.", "鱼", "我吃鱼。"),
        ("しごと", "仕事", "しごと", "noun", "work", "仕事をします。", "work", "I work.", "일", "일을 합니다.", "工作", "我工作。"),
        ("しつもん", "質問", "しつもん", "noun", "question", "質問があります。", "question", "I have a question.", "질문", "질문이 있습니다.", "问题", "我有一个问题。"),
        ("しゃしん", "写真", "しゃしん", "noun", "photo", "写真を撮ります。", "photo", "I take a photo.", "사진", "사진을 찍습니다.", "照片", "我拍照。"),
        ("じゅうしょ", "住所", "じゅうしょ", "noun", "address", "住所を書きます。", "address", "I write my address.", "주소", "주소를 씁니다.", "地址", "我写地址。"),
        ("しんぶん", "新聞", "しんぶん", "noun", "newspaper", "新聞を読みます。", "newspaper", "I read the newspaper.", "신문", "신문을 읽습니다.", "报纸", "我读报纸。"),
        ("すいようび", "水曜日", "すいようび", "noun", "Wednesday", "水曜日に会いましょう。", "Wednesday", "Let's meet on Wednesday.", "수요일", "수요일에 만나요.", "星期三", "我们星期三见吧。"),
        ("すき", "好き", "すき", "noun", "like", "コーヒーが好きです。", "like", "I like coffee.", "좋아함", "커피를 좋아합니다.", "喜欢", "我喜欢咖啡。"),
        ("すみ", "隅", "すみ", "noun", "corner", "隅に置きます。", "corner", "I put it in the corner.", "구석", "구석에 둡니다.", "角落", "我放在角落。"),
        ("せいかつ", "生活", "せいかつ", "noun", "life", "生活が変わりました。", "life", "My life has changed.", "생활", "생활이 변했습니다.", "生活", "我的生活改变了。"),
        ("せかい", "世界", "せかい", "noun", "world", "世界を旅行します。", "world", "I travel the world.", "세계", "세계를 여행합니다.", "世界", "我环游世界。"),
        ("せんしゅう", "先週", "せんしゅう", "noun", "last week", "先週会いました。", "last week", "We met last week.", "지난주", "지난주에 만났습니다.", "上周", "我们上周见面了。"),
        ("せんせい", "先生", "せんせい", "noun", "teacher", "先生に聞きます。", "teacher", "I ask the teacher.", "선생님", "선생님께 물어봅니다.", "老师", "我问老师。"),
        ("そうじ", "掃除", "そうじ", "noun", "cleaning", "掃除をします。", "cleaning", "I clean.", "청소", "청소를 합니다.", "打扫", "我打扫。"),
        ("たてもの", "建物", "たてもの", "noun", "building", "建物を見ます。", "building", "I look at the building.", "건물", "건물을 봅니다.", "建筑", "我看建筑。"),
        ("たまご", "卵", "たまご", "noun", "egg", "卵を食べます。", "egg", "I eat an egg.", "달걀", "달걀을 먹습니다.", "鸡蛋", "我吃鸡蛋。"),
        ("ちかく", "近く", "ちかく", "noun", "nearby", "近くに住んでいます。", "nearby", "I live nearby.", "가까운 곳", "가까운 곳에 살고 있습니다.", "附近", "我住在附近。"),
        ("ちず", "地図", "ちず", "noun", "map", "地図を見ます。", "map", "I look at the map.", "지도", "지도를 봅니다.", "地图", "我看地图。"),
        ("つぎ", "次", "つぎ", "noun", "next", "次は私の番です。", "next", "Next is my turn.", "다음", "다음은 제 차례입니다.", "下次", "下次是我的回合。"),
        ("つくえ", "机", "つくえ", "noun", "desk", "机の上に本があります。", "desk", "There is a book on the desk.", "책상", "책상 위에 책이 있습니다.", "桌子", "桌子上有书。"),
        ("てがみ", "手紙", "てがみ", "noun", "letter", "手紙を書きます。", "letter", "I write a letter.", "편지", "편지를 씁니다.", "信", "我写信。"),
        ("でんしゃ", "電車", "でんしゃ", "noun", "train", "電車に乗ります。", "train", "I ride the train.", "전철", "전철을 탑니다.", "电车", "我坐电车。"),
        ("でんわ", "電話", "でんわ", "noun", "telephone", "電話をかけます。", "telephone", "I make a phone call.", "전화", "전화를 겁니다.", "电话", "我打电话。"),
        ("とし", "年", "とし", "noun", "year", "年が変わりました。", "year", "The year has changed.", "년", "년이 바뀌었습니다.", "年", "年份改变了。"),
        ("としょかん", "図書館", "としょかん", "noun", "library", "図書館に行きます。", "library", "I go to the library.", "도서관", "도서관에 갑니다.", "图书馆", "我去图书馆。"),
        ("となり", "隣", "となり", "noun", "next door", "隣に住んでいます。", "next door", "I live next door.", "옆", "옆에 살고 있습니다.", "隔壁", "我住在隔壁。"),
        ("なか", "中", "なか", "noun", "inside", "中に入ります。", "inside", "I go inside.", "안", "안에 들어갑니다.", "里面", "我进入里面。"),
        ("なまえ", "名前", "なまえ", "noun", "name", "名前を書きます。", "name", "I write my name.", "이름", "이름을 씁니다.", "名字", "我写名字。"),
        ("にほん", "日本", "にほん", "noun", "Japan", "日本に住んでいます。", "Japan", "I live in Japan.", "일본", "일본에 살고 있습니다.", "日本", "我住在日本。"),
        ("にわ", "庭", "にわ", "noun", "garden", "庭で遊びます。", "garden", "I play in the garden.", "정원", "정원에서 놉니다.", "庭院", "我在庭院玩。"),
        ("ねこ", "猫", "ねこ", "noun", "cat", "猫がいます。", "cat", "There is a cat.", "고양이", "고양이가 있습니다.", "猫", "有一只猫。"),
        ("のりもの", "乗り物", "のりもの", "noun", "vehicle", "乗り物に乗ります。", "vehicle", "I ride a vehicle.", "탈것", "탈것을 탑니다.", "交通工具", "我乘坐交通工具。"),
        ("はこ", "箱", "はこ", "noun", "box", "箱に入れます。", "box", "I put it in a box.", "상자", "상자에 넣습니다.", "箱子", "我放进箱子里。"),
        ("はし", "橋", "はし", "noun", "bridge", "橋を渡ります。", "bridge", "I cross the bridge.", "다리", "다리를 건넙니다.", "桥", "我过桥。"),
        ("はな", "花", "はな", "noun", "flower", "花を見ます。", "flower", "I look at the flower.", "꽃", "꽃을 봅니다.", "花", "我看花。"),
        ("はる", "春", "はる", "noun", "spring", "春が来ました。", "spring", "Spring has come.", "봄", "봄이 왔습니다.", "春天", "春天来了。"),
        ("ひ", "日", "ひ", "noun", "day", "日が変わりました。", "day", "The day has changed.", "날", "날이 바뀌었습니다.", "日", "日期改变了。"),
        ("ひこうき", "飛行機", "ひこうき", "noun", "airplane", "飛行機に乗ります。", "airplane", "I ride an airplane.", "비행기", "비행기를 탑니다.", "飞机", "我坐飞机。"),
        ("びょうき", "病気", "びょうき", "noun", "illness", "病気になりました。", "illness", "I became ill.", "병", "병이 났습니다.", "疾病", "我生病了。"),
        ("ふく", "服", "ふく", "noun", "clothes", "服を着ます。", "clothes", "I wear clothes.", "옷", "옷을 입습니다.", "衣服", "我穿衣服。"),
        ("ふたつ", "二つ", "ふたつ", "noun", "two", "二つあります。", "two", "There are two.", "둘", "둘 있습니다.", "两个", "有两个。"),
        ("ふね", "船", "ふね", "noun", "ship", "船に乗ります。", "ship", "I ride a ship.", "배", "배를 탑니다.", "船", "我坐船。"),
        ("ほし", "星", "ほし", "noun", "star", "星を見ます。", "star", "I look at the stars.", "별", "별을 봅니다.", "星星", "我看星星。"),
        ("ほん", "本", "ほん", "noun", "book", "本を読みます。", "book", "I read a book.", "책", "책을 읽습니다.", "书", "我读书。"),
        ("まいしゅう", "毎週", "まいしゅう", "noun", "every week", "毎週会います。", "every week", "We meet every week.", "매주", "매주 만납니다.", "每周", "我们每周见面。"),
        ("まち", "町", "まち", "noun", "town", "町を歩きます。", "town", "I walk in the town.", "마을", "마을을 걷습니다.", "城镇", "我在城镇里走。"),
        ("まど", "窓", "まど", "noun", "window", "窓を開けます。", "window", "I open the window.", "창문", "창문을 엽니다.", "窗户", "我打开窗户。"),
        ("みち", "道", "みち", "noun", "road", "道を歩きます。", "road", "I walk on the road.", "길", "길을 걷습니다.", "路", "我在路上走。"),
        ("みなみ", "南", "みなみ", "noun", "south", "南に行きます。", "south", "I go south.", "남쪽", "남쪽으로 갑니다.", "南", "我往南走。"),
        ("みなさん", "", "みなさん", "noun", "everyone", "みなさん、こんにちは。", "everyone", "Hello, everyone.", "여러분", "여러분, 안녕하세요.", "大家", "大家好。"),
        ("むかし", "昔", "むかし", "noun", "long ago", "昔の話です。", "long ago", "It's a story from long ago.", "옛날", "옛날 이야기입니다.", "从前", "是从前的故事。"),
        ("むら", "村", "むら", "noun", "village", "村に住んでいます。", "village", "I live in a village.", "마을", "마을에 살고 있습니다.", "村庄", "我住在村庄。"),
        ("め", "目", "め", "noun", "eye", "目を閉じます。", "eye", "I close my eyes.", "눈", "눈을 감습니다.", "眼睛", "我闭上眼睛。"),
        ("もちもの", "持ち物", "もちもの", "noun", "belongings", "持ち物を確認します。", "belongings", "I check my belongings.", "소지품", "소지품을 확인합니다.", "物品", "我检查我的物品。"),
        ("やま", "山", "やま", "noun", "mountain", "山に登ります。", "mountain", "I climb the mountain.", "산", "산에 오릅니다.", "山", "我爬山。"),
        ("ゆうがた", "夕方", "ゆうがた", "noun", "evening", "夕方に帰ります。", "evening", "I return in the evening.", "저녁", "저녁에 돌아갑니다.", "傍晚", "我傍晚回来。"),
        ("ゆうびんきょく", "郵便局", "ゆうびんきょく", "noun", "post office", "郵便局に行きます。", "post office", "I go to the post office.", "우체국", "우체국에 갑니다.", "邮局", "我去邮局。"),
        ("ゆき", "雪", "ゆき", "noun", "snow", "雪が降ります。", "snow", "It snows.", "눈", "눈이 옵니다.", "雪", "下雪。"),
        ("よる", "夜", "よる", "noun", "night", "夜遅くまで働きます。", "night", "I work late into the night.", "밤", "밤늦게까지 일합니다.", "夜晚", "我工作到深夜。"),
        ("りょうしん", "両親", "りょうしん", "noun", "parents", "両親に会います。", "parents", "I meet my parents.", "부모님", "부모님을 만납니다.", "父母", "我见父母。"),
        ("れい", "例", "れい", "noun", "example", "例を挙げます。", "example", "I give an example.", "예", "예를 듭니다.", "例子", "我举例。"),
        ("れきし", "歴史", "れきし", "noun", "history", "歴史を勉強します。", "history", "I study history.", "역사", "역사를 공부합니다.", "历史", "我学习历史。"),
        ("れんしゅう", "練習", "れんしゅう", "noun", "practice", "練習をします。", "practice", "I practice.", "연습", "연습을 합니다.", "练习", "我练习。"),
        ("わかもの", "若者", "わかもの", "noun", "young person", "若者が多いです。", "young person", "There are many young people.", "젊은이", "젊은이가 많습니다.", "年轻人", "有很多年轻人。"),
        ("わしつ", "和室", "わしつ", "noun", "Japanese-style room", "和室で休みます。", "Japanese-style room", "I rest in a Japanese-style room.", "일본식 방", "일본식 방에서 쉽니다.", "和室", "我在和室休息。"),
    ],
    
    "N3": [
        # 중급 단어
        ("あいかわらず", "相変わらず", "あいかわらず", "adverb", "as usual, still", "相変わらず忙しいです。", "as usual", "I'm still busy as usual.", "여전히", "여전히 바쁩니다.", "依然", "依然很忙。"),
        ("あいま", "合間", "あいま", "noun", "gap, interval", "時間の合間を見つけました。", "gap, interval", "I found a gap in time.", "틈", "시간의 틈을 찾았습니다.", "间隙", "我找到了时间的间隙。"),
        ("あおぐ", "扇ぐ", "あおぐ", "verb", "to fan, to cool", "扇子で扇ぎました。", "to fan", "I fanned with a fan.", "부채질하다", "부채로 부채질했습니다.", "扇", "我用扇子扇了扇。"),
        ("あかじ", "赤字", "あかじ", "noun", "deficit, loss", "会社が赤字になりました。", "deficit", "The company went into the red.", "적자", "회사가 적자가 되었습니다.", "赤字", "公司出现了赤字。"),
        ("あけがた", "明け方", "あけがた", "noun", "dawn, daybreak", "明け方に起きました。", "dawn", "I woke up at dawn.", "새벽", "새벽에 일어났습니다.", "黎明", "在黎明时起床了。"),
    ],
    
    "N2": [
        # 중상급 단어
        ("あいさつ", "挨拶", "あいさつ", "noun", "greeting, salutation", "丁寧な挨拶をしました。", "greeting", "I made a polite greeting.", "인사", "정중한 인사를 했습니다.", "问候", "我做了礼貌的问候。"),
        ("あいそう", "愛情", "あいそう", "noun", "love, affection", "家族への愛情が深いです。", "love", "My love for my family is deep.", "애정", "가족에 대한 애정이 깊습니다.", "爱情", "对家人的爱很深。"),
        ("あいだがら", "間柄", "あいだがら", "noun", "relationship, connection", "良好な間柄を保っています。", "relationship", "We maintain a good relationship.", "관계", "좋은 관계를 유지하고 있습니다.", "关系", "保持着良好的关系。"),
        ("あいちゃく", "愛着", "あいちゃく", "noun", "attachment, affection", "故郷への愛着があります。", "attachment", "I have an attachment to my hometown.", "애착", "고향에 대한 애착이 있습니다.", "依恋", "对故乡有依恋。"),
        ("あいて", "相手", "あいて", "noun", "partner, opponent", "話し合いの相手を探しています。", "partner", "I'm looking for someone to talk with.", "상대", "상담할 상대를 찾고 있습니다.", "对方", "正在寻找商谈的对象。"),
    ],
    
    "N1": [
        # 고급 단어
        ("あいかわらず", "相変わらず", "あいかわらず", "adverb", "as usual, still, as before", "相変わらずの態度で接しました。", "as usual", "I treated them with the same attitude as usual.", "여전히", "여전한 태도로 대했습니다.", "依然", "以一如既往的态度对待了。"),
        ("あいさつ", "挨拶", "あいさつ", "noun", "greeting, salutation, speech", "開会の挨拶を述べました。", "greeting", "I delivered the opening greeting.", "인사말", "개회 인사를 했습니다.", "致辞", "发表了开幕致辞。"),
        ("あいそう", "愛情", "あいそう", "noun", "love, affection, attachment", "深い愛情を込めて接しました。", "love", "I treated them with deep love.", "애정", "깊은 애정을 담아 대했습니다.", "爱情", "怀着深厚的爱情对待了。"),
        ("あいだがら", "間柄", "あいだがら", "noun", "relationship, connection, terms", "良好な間柄を築きました。", "relationship", "We built a good relationship.", "관계", "좋은 관계를 구축했습니다.", "关系", "建立了良好的关系。"),
        ("あいちゃく", "愛着", "あいちゃく", "noun", "attachment, affection, fondness", "強い愛着を感じています。", "attachment", "I feel a strong attachment.", "애착", "강한 애착을 느끼고 있습니다.", "依恋", "感到强烈的依恋。"),
    ]
}

def generate_word_entry(word_id: int, word: str, kanji: str, hiragana: str, part_of_speech: str, 
                       definition: str, example: str, en_def: str, en_ex: str, 
                       ko_def: str, ko_ex: str, zh_def: str, zh_ex: str, level: str) -> Dict:
    """단어 엔트리 생성 (한자/히라가나 분리, 영어/한국어/중국어 번역 포함)"""
    result = {
        "id": word_id,
        "word": word,  # 전체 단어
        "level": level,
        "partOfSpeech": part_of_speech,
        "definition": definition,  # 영어 정의 (기본)
        "example": example,
        "translations": {
            "en": {
                "definition": en_def,
                "example": en_ex
            },
            "ko": {
                "definition": ko_def,
                "example": ko_ex
            },
            "zh": {
                "definition": zh_def,
                "example": zh_ex
            }
        }
    }
    # 한자와 히라가나가 있으면 추가 (None이 아닐 때만)
    if kanji and kanji.strip():
        result["kanji"] = kanji
    if hiragana and hiragana.strip():
        result["hiragana"] = hiragana
    return result

def expand_word_list(base_words: List, target_count: int, level: str) -> List[Dict]:
    """단어 리스트를 목표 개수만큼 확장 (중복 없이)"""
    words = []
    seen_words = set()  # 중복 체크용
    word_id_start = {
        "N5": 1,
        "N4": 1000,
        "N3": 2000,
        "N2": 3000,
        "N1": 4000
    }[level]
    
    word_id = word_id_start
    
    # 기본 단어 추가 (중복 체크)
    for word_data in base_words:
        word_text = word_data[0]  # word 필드
        if word_text not in seen_words:
            words.append(generate_word_entry(word_id, *word_data, level))
            seen_words.add(word_text)
            word_id += 1
    
    # 기본 단어 개수가 목표보다 적으면 경고
    if len(words) < target_count:
        print(f"[WARNING] {level}: Only {len(words)} unique words available, but target is {target_count}")
        print(f"  Will generate {len(words)} words (less than target)")
    
    # 목표 개수까지 자르기 (실제로는 더 많은 고유 단어 데이터가 필요)
    return words[:target_count]

def main():
    """메인 함수"""
    # 각 레벨별 목표 단어 수 (단독 기준)
    target_counts = {
        "N5": 800,   # N5만 800개
        "N4": 1500,  # N4만 1500개
        "N3": 3000,  # N3만 3000개
        "N2": 6000,  # N2만 6000개
        "N1": 10000  # N1만 10000개 이상
    }
    
    # 출력 디렉토리
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # N5-N3 파일 생성 (각각 독립적으로)
    n5_words = expand_word_list(JLPT_WORDS["N5"], target_counts["N5"], "N5")
    n4_words = expand_word_list(JLPT_WORDS["N4"], target_counts["N4"], "N4")
    n3_words = expand_word_list(JLPT_WORDS["N3"], target_counts["N3"], "N3")
    
    n5_n3_words = n5_words + n4_words + n3_words
    
    with open(os.path.join(output_dir, "words_n5_n3.json"), "w", encoding="utf-8") as f:
        json.dump(n5_n3_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] Generated words_n5_n3.json with {len(n5_n3_words)} words")
    
    # N2 파일 생성
    n2_words = expand_word_list(JLPT_WORDS["N2"], target_counts["N2"], "N2")
    
    with open(os.path.join(output_dir, "words_n2.json"), "w", encoding="utf-8") as f:
        json.dump(n2_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] Generated words_n2.json with {len(n2_words)} words")
    
    # N1 파일 생성
    n1_words = expand_word_list(JLPT_WORDS["N1"], target_counts["N1"], "N1")
    
    with open(os.path.join(output_dir, "words_n1.json"), "w", encoding="utf-8") as f:
        json.dump(n1_words, f, ensure_ascii=False, indent=2)
    print(f"[OK] Generated words_n1.json with {len(n1_words)} words")
    
    print(f"\n[Summary]")
    print(f"  N5: {len(n5_words)} words")
    print(f"  N4: {len(n4_words)} words")
    print(f"  N3: {len(n3_words)} words")
    print(f"  N2: {len(n2_words)} words")
    print(f"  N1: {len(n1_words)} words")
    print(f"  Total: {len(n5_n3_words) + len(n2_words) + len(n1_words)} words")

if __name__ == "__main__":
    main()

