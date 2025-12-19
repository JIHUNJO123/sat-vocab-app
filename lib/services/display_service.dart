import 'package:shared_preferences/shared_preferences.dart';

/// 단어 표시 방식 관리 서비스
class DisplayService {
  static final DisplayService instance = DisplayService._internal();
  factory DisplayService() => instance;
  DisplayService._internal();

  static const String _keyFuriganaDisplayMode = 'furiganaDisplayMode';
  String _displayMode = 'parentheses';

  /// 표시 방식 초기화
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _displayMode = prefs.getString(_keyFuriganaDisplayMode) ?? 'parentheses';
  }

  /// 현재 표시 방식 가져오기
  String get displayMode => _displayMode;

  /// 표시 방식 설정
  Future<void> setDisplayMode(String mode) async {
    _displayMode = mode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyFuriganaDisplayMode, mode);
  }

  /// 괄호 병기 방식인지 확인
  bool get isParenthesesMode => _displayMode == 'parentheses';

  /// 후리가나 방식인지 확인
  bool get isFuriganaMode => _displayMode == 'furigana';
}

