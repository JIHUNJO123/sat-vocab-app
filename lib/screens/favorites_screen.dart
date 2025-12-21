import 'package:flutter/material.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../services/display_service.dart';
import 'word_detail_screen.dart';
import 'favorites_flashcard_screen.dart';

class FavoritesScreen extends StatefulWidget {
  const FavoritesScreen({super.key});

  @override
  State<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends State<FavoritesScreen> {
  List<Word> _favorites = [];
  List<Word> _allFavorites = []; // ?�본 즐겨찾기 목록
  bool _isLoading = true;
  Map<int, String> _translatedDefinitions = {};
  bool _showNativeLanguage = true;
  bool _showBandBadge = true; // Band 배�? ?�시 ?��?
  String? _selectedBandFilter; // Band ?�터

  @override
  void initState() {
    super.initState();
    _loadFavorites();
  }

  Future<void> _loadFavorites() async {
    final favorites = await DatabaseHelper.instance.getFavorites();

    final translationService = TranslationService.instance;
    await translationService.init();
    final langCode = translationService.currentLanguage;

    if (translationService.needsTranslation) {
      // JSON?�서 ?�장 번역 로드
      final jsonWords =
          await DatabaseHelper.instance.getWordsWithTranslations();

      for (var word in favorites) {
        // ?�장 번역�??�용 (API ?�출 ?�음)
        final jsonWord = jsonWords.firstWhere(
          (w) =>
              w.id == word.id ||
              w.word.toLowerCase() == word.word.toLowerCase(),
          orElse: () => word,
        );
        final embeddedTranslation = jsonWord.getEmbeddedTranslation(
          langCode,
          'definition',
        );

        if (embeddedTranslation != null && embeddedTranslation.isNotEmpty) {
          _translatedDefinitions[word.id] = embeddedTranslation;
        }
      }
    }

    if (mounted) {
      setState(() {
        _allFavorites = favorites;
        _favorites = favorites;
        _isLoading = false;
      });
    }
  }

  void _filterByBand(String? band) {
    setState(() {
      _selectedBandFilter = band;
      if (band == null) {
        _favorites = List.from(_allFavorites);
      } else {
        _favorites = _allFavorites.where((w) => w.level == band).toList();
      }
    });
  }

  void _showBandFilterDialog() {
    final l10n = AppLocalizations.of(context)!;
    final bands = [
      {'level': null, 'name': l10n.allWords, 'color': Colors.grey},
      {'level': 'N5', 'name': 'N5', 'color': Colors.green},
      {'level': 'N4', 'name': 'N4', 'color': Colors.blue},
      {'level': 'N3', 'name': 'N3', 'color': Colors.orange},
    ];

    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder:
          (context) => Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  l10n.levelLearning,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                ...bands.map(
                  (band) => ListTile(
                    leading: CircleAvatar(
                      backgroundColor: band['color'] as Color,
                      radius: 12,
                    ),
                    title: Text(band['name'] as String),
                    trailing:
                        _selectedBandFilter == band['level']
                            ? Icon(
                              Icons.check,
                              color: Theme.of(context).primaryColor,
                            )
                            : null,
                    onTap: () {
                      Navigator.pop(context);
                      _filterByBand(band['level'] as String?);
                    },
                  ),
                ),
                const SizedBox(height: 16),
              ],
            ),
          ),
    );
  }

  Future<void> _removeFavorite(Word word) async {
    await DatabaseHelper.instance.toggleFavorite(word.id, false);

    setState(() {
      _favorites.removeWhere((w) => w.id == word.id);
    });

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(AppLocalizations.of(context)!.removedFromFavorites),
          action: SnackBarAction(
            label: 'Undo',
            onPressed: () async {
              await DatabaseHelper.instance.toggleFavorite(word.id, true);
              _loadFavorites();
            },
          ),
        ),
      );
    }
  }

  Color _getLevelColor(String level) {
    switch (level) {
      case 'N5':
        return Colors.green;
      case 'N4':
        return Colors.blue;
      case 'N3':
        return Colors.orange;
      case 'N2':
        return Colors.purple;
      case 'N1':
        return Colors.red;
      default:
        return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          children: [
            Text(l10n.favorites),
            if (_selectedBandFilter != null)
              Text(
                _selectedBandFilter!,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.normal,
                ),
              ),
          ],
        ),
        centerTitle: true,
        actions: [
          // Band 배�? ?��?
          if (_allFavorites.isNotEmpty)
            IconButton(
              icon: Icon(
                _showBandBadge ? Icons.label : Icons.label_off,
                color: _showBandBadge ? Theme.of(context).primaryColor : null,
              ),
              tooltip: 'Toggle Band Badge',
              onPressed: () {
                setState(() {
                  _showBandBadge = !_showBandBadge;
                });
              },
            ),
          // Band ?�터
          if (_allFavorites.isNotEmpty)
            IconButton(
              icon: Icon(
                Icons.filter_list,
                color:
                    _selectedBandFilter != null
                        ? Theme.of(context).primaryColor
                        : null,
              ),
              onPressed: _showBandFilterDialog,
            ),
          if (_allFavorites.isNotEmpty &&
              TranslationService.instance.needsTranslation)
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
          if (_favorites.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.style),
              tooltip: l10n.flashcard,
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder:
                        (context) =>
                            FavoritesFlashcardScreen(favorites: _favorites),
                  ),
                );
              },
            ),
        ],
      ),
      body:
          _isLoading
              ? const Center(child: CircularProgressIndicator())
              : _favorites.isEmpty
              ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.favorite_border,
                      size: 80,
                      color: Colors.grey[400],
                    ),
                    const SizedBox(height: 16),
                    Text(
                      l10n.noFavoritesYet,
                      style: TextStyle(fontSize: 18, color: Colors.grey[600]),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      l10n.tapHeartToSave,
                      style: TextStyle(fontSize: 14, color: Colors.grey[500]),
                    ),
                  ],
                ),
              )
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _favorites.length,
                itemBuilder: (context, index) {
                  final word = _favorites[index];
                  final definition =
                      _showNativeLanguage &&
                              _translatedDefinitions.containsKey(word.id)
                          ? _translatedDefinitions[word.id]!
                          : word.definition;

                  return Dismissible(
                    key: Key(word.id.toString()),
                    direction: DismissDirection.endToStart,
                    onDismissed: (_) => _removeFavorite(word),
                    background: Container(
                      alignment: Alignment.centerRight,
                      padding: const EdgeInsets.only(right: 20),
                      color: Colors.red,
                      child: const Icon(Icons.delete, color: Colors.white),
                    ),
                    child: Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder:
                                  (context) => WordDetailScreen(word: word),
                            ),
                          ).then((_) => _loadFavorites());
                        },
                        title: Row(
                          children: [
                            Expanded(
                              child: Text(
                                word.getDisplayWord(
                                  displayMode:
                                      DisplayService.instance.displayMode,
                                ),
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            if (_showBandBadge)
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 8,
                                  vertical: 2,
                                ),
                                decoration: BoxDecoration(
                                  color: _getLevelColor(word.level),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Text(
                                  word.level,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 10,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                          ],
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const SizedBox(height: 4),
                            Text(
                              word.partOfSpeech,
                              style: TextStyle(
                                color: Colors.grey[600],
                                fontSize: 12,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              definition,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.favorite, color: Colors.red),
                          onPressed: () => _removeFavorite(word),
                        ),
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
