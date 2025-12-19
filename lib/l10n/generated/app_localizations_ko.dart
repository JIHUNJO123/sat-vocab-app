// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Korean (`ko`).
class AppLocalizationsKo extends AppLocalizations {
  AppLocalizationsKo([String locale = 'ko']) : super(locale);

  @override
  String get appTitle => 'JLPT Step N5–N3';

  @override
  String get todayWord => '오늘의 단어';

  @override
  String get learning => '학습';

  @override
  String get levelLearning => '난이도별 학습';

  @override
  String get allWords => '전체 단어';

  @override
  String get viewAllWords => '모든 어휘 보기';

  @override
  String get favorites => '즐겨찾기';

  @override
  String get savedWords => '저장된 단어';

  @override
  String get flashcard => '플래시카드';

  @override
  String get cardLearning => '카드 학습';

  @override
  String get quiz => '퀴즈';

  @override
  String get testYourself => '실력 테스트';

  @override
  String get settings => '설정';

  @override
  String get language => '언어';

  @override
  String get displayLanguage => '표시 언어';

  @override
  String get selectLanguage => '언어 선택';

  @override
  String get display => '화면';

  @override
  String get darkMode => '다크 모드';

  @override
  String get fontSize => '글꼴 크기';

  @override
  String get notifications => '알림';

  @override
  String get dailyReminder => '매일 알림';

  @override
  String get dailyReminderDesc => '매일 학습 알림 받기';

  @override
  String get removeAds => '광고 제거';

  @override
  String get adsRemoved => '광고 제거됨';

  @override
  String get thankYou => '응원해 주셔서 감사합니다!';

  @override
  String get buy => '구매';

  @override
  String get restorePurchase => '구매 복원';

  @override
  String get restoring => '복원 중...';

  @override
  String get purchaseSuccess => '구매 완료!';

  @override
  String get loading => '로딩 중...';

  @override
  String get notAvailable => '사용 불가';

  @override
  String get info => '정보';

  @override
  String get version => '버전';

  @override
  String get disclaimer => '면책 조항';

  @override
  String get disclaimerText => '이 앱은 독립적인 JLPT 준비 도구이며 일본국제교류기금 또는 일본국제교육협회와 제휴, 보증 또는 승인 관계가 없습니다.';

  @override
  String get privacyPolicy => '개인정보 처리방침';

  @override
  String get cannotLoadWords => '단어를 불러올 수 없습니다';

  @override
  String get noFavoritesYet => '즐겨찾기가 없습니다';

  @override
  String get tapHeartToSave => '하트 아이콘을 눌러 단어를 저장하세요';

  @override
  String get addedToFavorites => '즐겨찾기에 추가됨';

  @override
  String get removedFromFavorites => '즐겨찾기에서 제거됨';

  @override
  String get wordDetail => '단어 상세';

  @override
  String get definition => '정의';

  @override
  String get example => '예문';

  @override
  String levelWords(String level) {
    return '$level 단어';
  }

  @override
  String get n5 => 'N5';

  @override
  String get n5Desc => '초급 - 500단어';

  @override
  String get n4 => 'N4';

  @override
  String get n4Desc => '초중급 - 1,000단어';

  @override
  String get n3 => 'N3';

  @override
  String get n3Desc => '중급 - 800단어';

  @override
  String get n2 => 'N2';

  @override
  String get n2Desc => '중상급 - 1,200단어';

  @override
  String get n1 => 'N1';

  @override
  String get n1Desc => '고급 - 1,500단어';

  @override
  String get alphabetical => '알파벳순';

  @override
  String get random => '무작위';

  @override
  String get tapToFlip => '탭하여 뒤집기';

  @override
  String get previous => '이전';

  @override
  String get next => '다음';

  @override
  String get question => '문제';

  @override
  String get score => '점수';

  @override
  String get quizComplete => '퀴즈 완료!';

  @override
  String get finish => '완료';

  @override
  String get tryAgain => '다시 시도';

  @override
  String get showResult => '결과 보기';

  @override
  String get wordToMeaning => '단어  뜻';

  @override
  String get meaningToWord => '뜻  단어';

  @override
  String get excellent => '훌륭해요! 만점!';

  @override
  String get great => '잘했어요! 계속 화이팅!';

  @override
  String get good => '좋아요! 계속 연습하세요!';

  @override
  String get keepPracticing => '계속 연습하세요! 실력이 늘 거예요!';

  @override
  String get levelA1 => '입문';

  @override
  String get levelA2 => '초급';

  @override
  String get levelB1 => '중급';

  @override
  String get levelB2 => '중상급';

  @override
  String get levelC1 => '고급';

  @override
  String get privacyPolicyContent => '이 앱은 개인정보를 수집, 저장 또는 공유하지 않습니다. 학습 진행 상황과 즐겨찾기는 기기에만 저장됩니다.';

  @override
  String get restorePurchaseDesc => '다른 기기에서 광고 제거를 구매했거나 앱을 재설치한 경우 여기를 눌러 구매를 복원하세요.';

  @override
  String get restoreComplete => '복원 완료';

  @override
  String get noPurchaseFound => '이전 구매 내역이 없습니다';

  @override
  String get furiganaDisplayMode => '읽기 표시 방식';

  @override
  String get parenthesesMode => '괄호 병기';

  @override
  String get furiganaMode => '후리가나';

  @override
  String get parenthesesExample => '예: 食べ物 (たべもの)';

  @override
  String get furiganaExample => '예: 食べ物 [たべもの]';
}
