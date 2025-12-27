import 'package:flutter/material.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/ad_service.dart';
import '../services/translation_service.dart';

class WordDetailScreen extends StatefulWidget {
  final Word word;
  final List<Word>? wordList;
  final int? currentIndex;

  const WordDetailScreen({
    super.key,
    required this.word,
    this.wordList,
    this.currentIndex,
  });

  @override
  State<WordDetailScreen> createState() => _WordDetailScreenState();
}

class _WordDetailScreenState extends State<WordDetailScreen> {
  late Word _word;
  late int _currentIndex;
  String? _translatedDefinition;
  String? _translatedExample;

  @override
  void initState() {
    super.initState();
    _word = widget.word;
    _currentIndex = widget.currentIndex ?? 0;
    _loadTranslations();
  }

  bool get _hasNavigation =>
      widget.wordList != null && widget.wordList!.length > 1;
  bool get _canGoPrevious => _hasNavigation && _currentIndex > 0;
  bool get _canGoNext =>
      _hasNavigation && _currentIndex < widget.wordList!.length - 1;

  // 잠긴 단어인지 확인 (짝수 인덱스 = 2, 4, 6...)
  bool _isWordLocked(int index) {
    if (index % 2 == 0) return false;
    return !AdService.instance.isUnlocked;
  }

  void _goToPrevious() {
    if (_canGoPrevious) {
      int newIndex = _currentIndex - 1;
      while (newIndex > 0 && _isWordLocked(newIndex)) {
        newIndex--;
      }
      if (_isWordLocked(newIndex)) return;

      setState(() {
        _currentIndex = newIndex;
        _word = widget.wordList![_currentIndex];
        _translatedDefinition = null;
        _translatedExample = null;
      });
      _loadTranslations();
    }
  }

  void _goToNext() {
    if (_canGoNext) {
      int newIndex = _currentIndex + 1;
      while (newIndex < widget.wordList!.length - 1 &&
          _isWordLocked(newIndex)) {
        newIndex++;
      }
      if (_isWordLocked(newIndex)) return;

      setState(() {
        _currentIndex = newIndex;
        _word = widget.wordList![_currentIndex];
        _translatedDefinition = null;
        _translatedExample = null;
      });
      _loadTranslations();
    }
  }

  Future<void> _loadTranslations() async {
    final translationService = TranslationService.instance;
    await translationService.init();

    if (!translationService.needsTranslation) return;

    // ?�장 번역�??�용 (API ?�출 ?�음)
    final langCode = translationService.currentLanguage;
    final embeddedDef = _word.getEmbeddedTranslation(langCode, 'definition');
    final embeddedEx = _word.getEmbeddedTranslation(langCode, 'example');

    if (mounted) {
      setState(() {
        _translatedDefinition = embeddedDef;
        _translatedExample = embeddedEx;
      });
    }
  }

  Future<void> _toggleFavorite() async {
    await DatabaseHelper.instance.toggleFavorite(_word.id, !_word.isFavorite);
    setState(() {
      _word = _word.copyWith(isFavorite: !_word.isFavorite);
    });

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            _word.isFavorite
                ? AppLocalizations.of(context)!.addedToFavorites
                : AppLocalizations.of(context)!.removedFromFavorites,
          ),
          duration: const Duration(seconds: 1),
        ),
      );
    }
  }

  Color _getLevelColor(String level) {
    switch (level) {
      case 'Band 5':
        return Colors.green;
      case 'Band 6':
        return Colors.lightGreen;
      case 'Band 7':
        return Colors.orange;
      case 'Band 8+':
        return Colors.red;
      default:
        return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final levelColor = _getLevelColor(_word.level);

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) {
        if (didPop) return;
        Navigator.of(context).pop(_currentIndex);
      },
      child: Scaffold(
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => Navigator.of(context).pop(_currentIndex),
          ),
          title: Text(
            _hasNavigation
                ? '${_currentIndex + 1} / ${widget.wordList!.length}'
                : l10n.wordDetail,
          ),
          actions: [
            IconButton(
              icon: Icon(
                _word.isFavorite ? Icons.favorite : Icons.favorite_border,
                color: _word.isFavorite ? Colors.red : null,
              ),
              onPressed: _toggleFavorite,
            ),
          ],
        ),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Card
              Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(24.0),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    gradient: LinearGradient(
                      colors: [
                        levelColor,
                        levelColor.withAlpha((0.7 * 255).toInt()),
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.white.withAlpha(
                                (0.2 * 255).toInt(),
                              ),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              _word.level,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),
                      Text(
                        _word.word,
                        style: const TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Definition Section - 번역 ??(??글??, ?�어 ?�래 (?�색)
              _buildDefinitionSection(
                title: l10n.definition,
                icon: Icons.book,
                content: _word.definition,
                translation: _translatedDefinition,
              ),
              const SizedBox(height: 16),

              // Example Section - ?�어 ??(검?�??, 번역 ?�래 (?�색)
              _buildExampleSection(
                title: l10n.example,
                icon: Icons.format_quote,
                content: _word.example,
                translation: _translatedExample,
              ),
              // Navigation buttons at bottom
              if (_hasNavigation) ...[
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    ElevatedButton.icon(
                      onPressed: _currentIndex > 0 ? _goToPrevious : null,
                      icon: const Icon(Icons.arrow_back),
                      label: Text(l10n.previous),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 12,
                        ),
                      ),
                    ),
                    ElevatedButton.icon(
                      onPressed:
                          _currentIndex < widget.wordList!.length - 1
                              ? _goToNext
                              : null,
                      icon: const Icon(Icons.arrow_forward),
                      label: Text(l10n.next),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 12,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  // ?�의?? 번역 먼�? (??글??, ?�어 ?�래 (?�색)
  Widget _buildDefinitionSection({
    required String title,
    required IconData icon,
    required String content,
    String? translation,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, size: 20, color: Theme.of(context).primaryColor),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            // 번역???�으�?번역 먼�? (??글??, ?�어 ?�래 (?�색)
            if (translation != null) ...[
              Text(
                translation,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w500,
                  height: 1.5,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                content,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[600],
                  height: 1.5,
                ),
              ),
            ] else
              Text(content, style: const TextStyle(fontSize: 16, height: 1.5)),
          ],
        ),
      ),
    );
  }

  // ?�문?? ?�어 먼�? (검?�??, 번역 ?�래 (?�색)
  Widget _buildExampleSection({
    required String title,
    required IconData icon,
    required String content,
    String? translation,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, size: 20, color: Theme.of(context).primaryColor),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            // ?�어 먼�? (검?�??, 번역 ?�래 (?�색)
            Text(
              content,
              style: const TextStyle(
                fontSize: 16,
                fontStyle: FontStyle.italic,
                height: 1.5,
              ),
            ),
            if (translation != null) ...[
              const SizedBox(height: 8),
              Text(
                translation,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[600],
                  height: 1.5,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
