import 'dart:ui' as ui;
import 'package:shared_preferences/shared_preferences.dart';

/// Supported language information
class SupportedLanguage {
  final String code;
  final String name;
  final String nativeName;

  const SupportedLanguage({
    required this.code,
    required this.name,
    required this.nativeName,
  });
}

/// Translation service (embedded translations only, no API calls)
class TranslationService {
  static final TranslationService instance = TranslationService._init();
  TranslationService._init();

  // Supported languages list - GRE major markets only
  // India (#1), China (#2), USA, South Korea
  static const List<SupportedLanguage> supportedLanguages = [
    SupportedLanguage(code: 'en', name: 'English', nativeName: 'English'),
    SupportedLanguage(code: 'hi', name: 'Hindi', nativeName: 'Hindi'),
    SupportedLanguage(code: 'zh', name: 'Chinese', nativeName: 'Chinese'),
    SupportedLanguage(code: 'ko', name: 'Korean', nativeName: 'Korean'),
  ];

  String _currentLanguage = 'en';

  String get currentLanguage => _currentLanguage;

  /// Get current language info
  SupportedLanguage get currentLanguageInfo {
    return supportedLanguages.firstWhere(
      (lang) => lang.code == _currentLanguage,
      orElse: () => supportedLanguages.first,
    );
  }

  /// Initialize language service
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final savedLanguage = prefs.getString('nativeLanguage');

    if (savedLanguage != null &&
        supportedLanguages.any((lang) => lang.code == savedLanguage)) {
      _currentLanguage = savedLanguage;
    } else {
      // Auto-detect device language if no saved value
      final deviceLocale = ui.PlatformDispatcher.instance.locale;
      final deviceLangCode = deviceLocale.languageCode;

      // Check if supported
      final isSupported = supportedLanguages.any(
        (lang) => lang.code == deviceLangCode,
      );
      _currentLanguage = isSupported ? deviceLangCode : 'en';

      await prefs.setString('nativeLanguage', _currentLanguage);
    }
  }

  /// Change language
  Future<void> setLanguage(String languageCode) async {
    if (supportedLanguages.any((lang) => lang.code == languageCode)) {
      _currentLanguage = languageCode;
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('nativeLanguage', languageCode);
    }
  }

  /// Check if translation is needed
  bool get needsTranslation => _currentLanguage != 'en';
}
