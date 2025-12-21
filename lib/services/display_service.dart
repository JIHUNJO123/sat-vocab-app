import 'package:shared_preferences/shared_preferences.dart';

/// ?¨ì–´ ?œì‹œ ë°©ì‹ ê´€ë¦??œë¹„??
class DisplayService {
  static final DisplayService instance = DisplayService._internal();
  factory DisplayService() => instance;
  DisplayService._internal();

  static const String _keyFuriganaDisplayMode = 'furiganaDisplayMode';
  String _displayMode = 'parentheses';

  /// ?œì‹œ ë°©ì‹ ì´ˆê¸°??
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _displayMode = prefs.getString(_keyFuriganaDisplayMode) ?? 'parentheses';
  }

  /// ?„ì¬ ?œì‹œ ë°©ì‹ ê°€?¸ì˜¤ê¸?
  String get displayMode => _displayMode;

  /// ?œì‹œ ë°©ì‹ ?¤ì •
  Future<void> setDisplayMode(String mode) async {
    _displayMode = mode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyFuriganaDisplayMode, mode);
  }

  /// ê´„í˜¸ ë³‘ê¸° ë°©ì‹?¸ì? ?•ì¸
  bool get isParenthesesMode => _displayMode == 'parentheses';

  /// ?„ë¦¬ê°€??ë°©ì‹?¸ì? ?•ì¸
  bool get isFuriganaMode => _displayMode == 'furigana';
}

