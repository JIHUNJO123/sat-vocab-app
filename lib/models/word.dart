import 'dart:convert';

/// ?�어 모델 (JLPT ?�습??- ?�본???�어??
/// ?�어 기본 ?�보 + ?�베??번역 + ?�적 번역
class Word {
  final int id;
  final String word; // ?�체 ?�어 (?�자+?�라가???�합)
  final String? kanji; // ?�자 부�?
  final String? hiragana; // ?�라가???�기
  final String
  level; // JLPT ?�벨: N5, N4, N3, N2, N1
  final String partOfSpeech;
  final String definition; // ?�어 ?�의
  final String example; // ?�어 ?�문
  final String
  category; // 카테고리: Academic, Environment, Technology, Health, Education ??
  bool isFavorite;

  // ?�장 번역 ?�이??(words.json?�서 로드)
  final Map<String, Map<String, String>>? translations;

  // 번역???�스??(?��??�에 ?�정??
  String? translatedDefinition;
  String? translatedExample;

  Word({
    required this.id,
    required this.word,
    this.kanji,
    this.hiragana,
    required this.level,
    required this.partOfSpeech,
    required this.definition,
    required this.example,
    this.category = 'General',
    this.isFavorite = false,
    this.translations,
    this.translatedDefinition,
    this.translatedExample,
  });

  /// ?�장 번역 가?�오�?
  String? getEmbeddedTranslation(String langCode, String fieldType) {
    if (translations == null) return null;
    final langData = translations![langCode];
    if (langData == null) return null;
    return langData[fieldType];
  }

  /// JSON?�서 ?�성 (?�어 ?�본 + ?�장 번역)
  factory Word.fromJson(Map<String, dynamic> json) {
    // translations ?�싱 (??가지 ?�식 지??
    Map<String, Map<String, String>>? translations;

    // ?�식 1: translations 객체
    if (json['translations'] != null) {
      translations = {};
      (json['translations'] as Map<String, dynamic>).forEach((langCode, data) {
        if (data is Map<String, dynamic>) {
          translations![langCode] = {
            'definition': data['definition']?.toString() ?? '',
            'example': data['example']?.toString() ?? '',
          };
        }
      });
    }

    // ?�식 2: flat ?�식 (definition_ja, example_ja ??
    final langCodes = [
      'ko',
      'ja',
      'zh',
      'zh_cn',
      'zh_tw',
      'es',
      'fr',
      'de',
      'pt',
      'vi',
      'ar',
      'th',
      'ru',
    ];
    for (final lang in langCodes) {
      final defKey = 'definition_$lang';
      final exKey = 'example_$lang';
      if (json[defKey] != null || json[exKey] != null) {
        translations ??= {};
        // zh_cn -> zh�?매핑
        final normalizedLang = lang == 'zh_cn' ? 'zh' : lang;
        translations[normalizedLang] = {
          'definition': json[defKey]?.toString() ?? '',
          'example': json[exKey]?.toString() ?? '',
        };
      }
    }

    return Word(
      id: json['id'],
      word: json['word'],
      kanji: json['kanji'],
      hiragana: json['hiragana'],
      level: json['level'],
      partOfSpeech: json['partOfSpeech'],
      definition: json['definition'],
      example: json['example'],
      category: json['category'] ?? 'General',
      isFavorite: json['isFavorite'] == 1 || json['isFavorite'] == true,
      translations: translations,
    );
  }

  /// DB 맵에???�성 (translations JSON ?�싱 ?�함)
  factory Word.fromDb(Map<String, dynamic> json) {
    // DB?�서 translations ?�드 ?�싱
    Map<String, Map<String, String>>? translations;
    if (json['translations'] != null && json['translations'] is String) {
      try {
        final decoded = jsonDecode(json['translations'] as String);
        if (decoded is Map<String, dynamic>) {
          translations = {};
          decoded.forEach((langCode, data) {
            if (data is Map<String, dynamic>) {
              translations![langCode] = {
                'definition': data['definition']?.toString() ?? '',
                'example': data['example']?.toString() ?? '',
              };
            }
          });
        }
      } catch (e) {
        print('Error parsing translations JSON: $e');
      }
    }

    return Word(
      id: json['id'] as int,
      word: json['word'] as String,
      kanji: json['kanji'] as String?,
      hiragana: json['hiragana'] as String?,
      level: json['level'] as String,
      partOfSpeech: json['partOfSpeech'] as String,
      definition: json['definition'] as String,
      example: json['example'] as String,
      category: json['category'] as String? ?? 'General',
      isFavorite: (json['isFavorite'] as int) == 1,
      translations: translations,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'word': word,
      'level': level,
      'partOfSpeech': partOfSpeech,
      'definition': definition,
      'example': example,
      'category': category,
      'isFavorite': isFavorite ? 1 : 0,
    };
  }

  /// 번역???�의 가?�오�?(번역 ?�으�??�어 ?�본)
  String getDefinition(bool useTranslation) {
    if (useTranslation &&
        translatedDefinition != null &&
        translatedDefinition!.isNotEmpty) {
      return translatedDefinition!;
    }
    return definition;
  }

  /// 번역???�문 가?�오�?(번역 ?�으�??�어 ?�본)
  String getExample(bool useTranslation) {
    if (useTranslation &&
        translatedExample != null &&
        translatedExample!.isNotEmpty) {
      return translatedExample!;
    }
    return example;
  }

  /// ?�자?� ?�라가?��? ?�께 ?�시 (?�시 방식???�라)
  /// [displayMode]: 'parentheses' (괄호 병기) ?�는 'furigana' (?�리가??
  String getDisplayWord({String displayMode = 'parentheses'}) {
    if (kanji != null && hiragana != null && kanji!.isNotEmpty && hiragana!.isNotEmpty) {
      if (displayMode == 'furigana') {
        // ?�리가??방식: 食べ??[?�べ?�の]
        return '$kanji [$hiragana]';
      } else {
        // 괄호 병기 방식: 食べ??(?�べ?�の)
        return '$kanji ($hiragana)';
      }
    }
    return word;
  }

  Word copyWith({
    int? id,
    String? word,
    String? kanji,
    String? hiragana,
    String? level,
    String? partOfSpeech,
    String? definition,
    String? example,
    String? category,
    bool? isFavorite,
    Map<String, Map<String, String>>? translations,
    String? translatedDefinition,
    String? translatedExample,
  }) {
    return Word(
      id: id ?? this.id,
      word: word ?? this.word,
      kanji: kanji ?? this.kanji,
      hiragana: hiragana ?? this.hiragana,
      level: level ?? this.level,
      partOfSpeech: partOfSpeech ?? this.partOfSpeech,
      definition: definition ?? this.definition,
      example: example ?? this.example,
      category: category ?? this.category,
      isFavorite: isFavorite ?? this.isFavorite,
      translations: translations ?? this.translations,
      translatedDefinition: translatedDefinition ?? this.translatedDefinition,
      translatedExample: translatedExample ?? this.translatedExample,
    );
  }
}
