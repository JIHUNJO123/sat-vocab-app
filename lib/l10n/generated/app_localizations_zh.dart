// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Chinese (`zh`).
class AppLocalizationsZh extends AppLocalizations {
  AppLocalizationsZh([String locale = 'zh']) : super(locale);

  @override
  String get appTitle => 'JLPT Step N5–N3';

  @override
  String get todayWord => '今日单词';

  @override
  String get learning => '学习';

  @override
  String get levelLearning => '难度等级';

  @override
  String get allWords => '全部单词';

  @override
  String get viewAllWords => '查看所有词汇';

  @override
  String get favorites => '收藏夹';

  @override
  String get savedWords => '已保存的单词';

  @override
  String get flashcard => '闪卡';

  @override
  String get cardLearning => '卡片学习';

  @override
  String get quiz => '测验';

  @override
  String get testYourself => '测试自己';

  @override
  String get settings => '设置';

  @override
  String get language => '语言';

  @override
  String get displayLanguage => '显示语言';

  @override
  String get selectLanguage => '选择语言';

  @override
  String get display => '显示';

  @override
  String get darkMode => '深色模式';

  @override
  String get fontSize => '字体大小';

  @override
  String get notifications => '通知';

  @override
  String get dailyReminder => '每日提醒';

  @override
  String get dailyReminderDesc => '每天提醒您学习';

  @override
  String get removeAds => '移除广告';

  @override
  String get adsRemoved => '广告已移除';

  @override
  String get thankYou => '感谢您的支持！';

  @override
  String get buy => '购买';

  @override
  String get restorePurchase => '恢复购买';

  @override
  String get restoring => '恢复中...';

  @override
  String get purchaseSuccess => '购买成功！';

  @override
  String get loading => '加载中...';

  @override
  String get notAvailable => '不可用';

  @override
  String get info => '信息';

  @override
  String get version => '版本';

  @override
  String get disclaimer => '免责声明';

  @override
  String get disclaimerText => '本应用是独立的JLPT备考工具，与日本国际交流基金会或日本国际教育支援协会无任何关联、背书或认可关系。';

  @override
  String get privacyPolicy => '隐私政策';

  @override
  String get cannotLoadWords => '无法加载单词';

  @override
  String get noFavoritesYet => '暂无收藏';

  @override
  String get tapHeartToSave => '点击心形图标保存单词';

  @override
  String get addedToFavorites => '已添加到收藏';

  @override
  String get removedFromFavorites => '已从收藏中移除';

  @override
  String get wordDetail => '单词详情';

  @override
  String get definition => '定义';

  @override
  String get example => '例句';

  @override
  String levelWords(String level) {
    return '$level单词';
  }

  @override
  String get n5 => 'N5';

  @override
  String get n5Desc => '初级 - 500词';

  @override
  String get n4 => 'N4';

  @override
  String get n4Desc => '初中级 - 1,000词';

  @override
  String get n3 => 'N3';

  @override
  String get n3Desc => '中级 - 800词';

  @override
  String get n2 => 'N2';

  @override
  String get n2Desc => '中高级 - 1,200词';

  @override
  String get n1 => 'N1';

  @override
  String get n1Desc => '高级 - 1,500词';

  @override
  String get alphabetical => '字母顺序';

  @override
  String get random => '随机';

  @override
  String get tapToFlip => '点击翻转';

  @override
  String get previous => '上一个';

  @override
  String get next => '下一个';

  @override
  String get question => '问题';

  @override
  String get score => '分数';

  @override
  String get quizComplete => '测验完成！';

  @override
  String get finish => '完成';

  @override
  String get tryAgain => '再试一次';

  @override
  String get showResult => '显示结果';

  @override
  String get wordToMeaning => '单词释义';

  @override
  String get meaningToWord => '释义单词';

  @override
  String get excellent => '太棒了！满分！';

  @override
  String get great => '很好！继续加油！';

  @override
  String get good => '不错！继续练习！';

  @override
  String get keepPracticing => '继续练习！你会进步的！';

  @override
  String get levelA1 => '入门';

  @override
  String get levelA2 => '初级';

  @override
  String get levelB1 => '中级';

  @override
  String get levelB2 => '中高级';

  @override
  String get levelC1 => '高级';

  @override
  String get privacyPolicyContent => '本应用不收集、存储或共享任何个人信息。您的学习进度和收藏仅存储在您的设备上。';

  @override
  String get restorePurchaseDesc => '如果您之前在其他设备上购买了移除广告或重新安装了应用，请点击此处恢复购买。';

  @override
  String get restoreComplete => '恢复完成';

  @override
  String get noPurchaseFound => '未找到之前的购买记录';

  @override
  String get furiganaDisplayMode => '假名显示方式';

  @override
  String get parenthesesMode => '括号标注';

  @override
  String get furiganaMode => '假名标注';

  @override
  String get parenthesesExample => '例：食べ物 (たべもの)';

  @override
  String get furiganaExample => '例：食べ物 [たべもの]';
}
