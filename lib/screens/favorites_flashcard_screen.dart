import 'package:flutter/material.dart';
import 'package:flip_card/flip_card.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../db/database_helper.dart';

class FavoritesFlashcardScreen extends StatefulWidget {
  final List<Word> favorites;

  const FavoritesFlashcardScreen({super.key, required this.favorites});

  @override
  State<FavoritesFlashcardScreen> createState() =>
      _FavoritesFlashcardScreenState();
}

class _FavoritesFlashcardScreenState extends State<FavoritesFlashcardScreen> {
  late List<Word> _favorites;
  late PageController _pageController;
  int _currentIndex = 0;
  Map<int, String> _translatedDefinitions = {};
  Map<int, String> _translatedExamples = {};
  bool _showNativeLanguage = true;

  @override
  void initState() {
    super.initState();
    _favorites = List.from(widget.favorites);
    _pageController = PageController();
    _loadTranslations();
  }

  Future<void> _loadTranslations() async {
    final translationService = TranslationService.instance;
    await translationService.init();

    if (translationService.needsTranslation) {
      final langCode = translationService.currentLanguage;
      for (var word in _favorites) {
        // ?¥Ïû• Î≤àÏó≠Îß??¨Ïö© (API ?∏Ï∂ú ?ÜÏùå)
        final embeddedDef = word.getEmbeddedTranslation(langCode, 'definition');
        final embeddedEx = word.getEmbeddedTranslation(langCode, 'example');

        if (mounted && embeddedDef != null && embeddedDef.isNotEmpty) {
          setState(() {
            _translatedDefinitions[word.id] = embeddedDef;
            if (embeddedEx != null && embeddedEx.isNotEmpty) {
              _translatedExamples[word.id] = embeddedEx;
            }
          });
        }
      }
    }
  }

  Future<void> _toggleFavorite(Word word) async {
    await DatabaseHelper.instance.toggleFavorite(word.id, !word.isFavorite);
    setState(() {
      word.isFavorite = !word.isFavorite;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          word.isFavorite
              ? AppLocalizations.of(context)!.addedToFavorites
              : AppLocalizations.of(context)!.removedFromFavorites,
        ),
        duration: const Duration(seconds: 1),
      ),
    );
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
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    if (_favorites.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.flashcard)),
        body: Center(child: Text(l10n.noFavoritesYet)),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.flashcard),
        actions: [
          if (TranslationService.instance.needsTranslation)
            IconButton(
              icon: Icon(
                _showNativeLanguage ? Icons.translate : Icons.language,
              ),
              onPressed: () {
                setState(() {
                  _showNativeLanguage = !_showNativeLanguage;
                });
              },
            ),
        ],
      ),
      body: Column(
        children: [
          // Progress indicator
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              '${_currentIndex + 1} / ${_favorites.length}',
              style: const TextStyle(fontSize: 16),
            ),
          ),
          // Flashcard
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              itemCount: _favorites.length,
              onPageChanged: (index) {
                setState(() {
                  _currentIndex = index;
                });
              },
              itemBuilder: (context, index) {
                final word = _favorites[index];
                final definition =
                    _showNativeLanguage &&
                            _translatedDefinitions.containsKey(word.id)
                        ? _translatedDefinitions[word.id]!
                        : word.definition;
                final example =
                    _showNativeLanguage &&
                            _translatedExamples.containsKey(word.id)
                        ? _translatedExamples[word.id]!
                        : word.example;

                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: FlipCard(
                    direction: FlipDirection.HORIZONTAL,
                    front: Card(
                      elevation: 4,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(20),
                          gradient: LinearGradient(
                            colors: [
                              _getLevelColor(word.level),
                              _getLevelColor(
                                word.level,
                              ).withAlpha((0.7 * 255).toInt()),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(24.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(
                                      horizontal: 12,
                                      vertical: 6,
                                    ),
                                    decoration: BoxDecoration(
                                      color: Colors.white.withAlpha(
                                        (0.2 * 255).toInt(),
                                      ),
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                    child: Text(
                                      word.partOfSpeech,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  IconButton(
                                    icon: Icon(
                                      word.isFavorite
                                          ? Icons.favorite
                                          : Icons.favorite_border,
                                      color:
                                          word.isFavorite
                                              ? Colors.red
                                              : Colors.white,
                                    ),
                                    onPressed: () => _toggleFavorite(word),
                                  ),
                                ],
                              ),
                              const Spacer(),
                              Text(
                                word.word,
                                style: const TextStyle(
                                  fontSize: 28,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 16),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 12,
                                  vertical: 6,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.white.withAlpha(
                                    (0.2 * 255).toInt(),
                                  ),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  word.level,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 14,
                                  ),
                                ),
                              ),
                              const Spacer(),
                              Text(
                                l10n.tapToFlip,
                                style: TextStyle(
                                  color: Colors.white.withAlpha(
                                    (0.8 * 255).toInt(),
                                  ),
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    back: Card(
                      elevation: 4,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(24.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.lightbulb_outline,
                              size: 40,
                              color: Theme.of(context).primaryColor,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              l10n.definition,
                              style: TextStyle(
                                fontSize: 14,
                                color: Theme.of(context).primaryColor,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              definition,
                              style: const TextStyle(fontSize: 18, height: 1.5),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 24),
                            Text(
                              l10n.example,
                              style: TextStyle(
                                fontSize: 14,
                                color: Theme.of(context).primaryColor,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              word.example, // Always show example in English
                              style: TextStyle(
                                fontSize: 16,
                                fontStyle: FontStyle.italic,
                                color: Colors.grey[700],
                                height: 1.5,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          // Navigation buttons
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed:
                      _currentIndex > 0
                          ? () {
                            _pageController.previousPage(
                              duration: const Duration(milliseconds: 300),
                              curve: Curves.easeInOut,
                            );
                          }
                          : null,
                  icon: const Icon(Icons.chevron_left),
                  label: Text(l10n.previous),
                ),
                ElevatedButton.icon(
                  onPressed:
                      _currentIndex < _favorites.length - 1
                          ? () {
                            _pageController.nextPage(
                              duration: const Duration(milliseconds: 300),
                              curve: Curves.easeInOut,
                            );
                          }
                          : null,
                  icon: const Icon(Icons.chevron_right),
                  label: Text(l10n.next),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
