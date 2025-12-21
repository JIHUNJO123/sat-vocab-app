import 'dart:convert';

/// ?¨ì–´ ëª¨ë¸ (GRE ?™ìŠµ??- ?¤êµ­??ì§€??
/// ?ì–´ ?ë³¸ ?°ì´??+ ?´ì¥ ë²ˆì—­ + ?™ì  ë²ˆì—­
class Word {
  final int id;
  final String word;
  final String
  level; // GRE Band ê¸°ì?: Band 4.5-5.5, Band 6.0-6.5, Band 7.0-7.5, Band 8.0+
  final String partOfSpeech;
  final String definition; // ?ì–´ ?•ì˜
  final String example; // ?ì–´ ?ˆë¬¸
  final String
  category; // ì¹´í…Œê³ ë¦¬: Academic, Environment, Technology, Health, Education ??
  bool isFavorite;

  // ?´ì¥ ë²ˆì—­ ?°ì´??(words.json?ì„œ ë¡œë“œ)
  final Map<String, Map<String, String>>? translations;

  // ë²ˆì—­???ìŠ¤??(?°í??„ì— ?¤ì •??
  String? translatedDefinition;
  String? translatedExample;

  Word({
    required this.id,
    required this.word,
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

  /// ?´ì¥ ë²ˆì—­ ê°€?¸ì˜¤ê¸?
  String? getEmbeddedTranslation(String langCode, String fieldType) {
    if (translations == null) return null;
    final langData = translations![langCode];
    if (langData == null) return null;
    return langData[fieldType];
  }

  /// JSON?ì„œ ?ì„± (?ì–´ ?ë³¸ + ?´ì¥ ë²ˆì—­)
  factory Word.fromJson(Map<String, dynamic> json) {
    // translations ?Œì‹± (??ê°€ì§€ ?•ì‹ ì§€??
    Map<String, Map<String, String>>? translations;

    // ?•ì‹ 1: translations ê°ì²´
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

    // ?•ì‹ 2: flat ?•ì‹ (definition_ja, example_ja ??
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
        // zh_cn -> zhë¡?ë§¤í•‘
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
      level: json['level'],
      partOfSpeech: json['partOfSpeech'],
      definition: json['definition'],
      example: json['example'],
      category: json['category'] ?? 'General',
      isFavorite: json['isFavorite'] == 1 || json['isFavorite'] == true,
      translations: translations,
    );
  }

  /// DB ë§µì—???ì„± (translations JSON ?Œì‹± ?¬í•¨)
  factory Word.fromDb(Map<String, dynamic> json) {
    // DB?ì„œ translations ?„ë“œ ?Œì‹±
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

  /// ë²ˆì—­???•ì˜ ê°€?¸ì˜¤ê¸?(ë²ˆì—­ ?†ìœ¼ë©??ì–´ ?ë³¸)
  String getDefinition(bool useTranslation) {
    if (useTranslation &&
        translatedDefinition != null &&
        translatedDefinition!.isNotEmpty) {
      return translatedDefinition!;
    }
    return definition;
  }

  /// ë²ˆì—­???ˆë¬¸ ê°€?¸ì˜¤ê¸?(ë²ˆì—­ ?†ìœ¼ë©??ì–´ ?ë³¸)
  String getExample(bool useTranslation) {
    if (useTranslation &&
        translatedExample != null &&
        translatedExample!.isNotEmpty) {
      return translatedExample!;
    }
    return example;
  }

  Word copyWith({
    int? id,
    String? word,
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
