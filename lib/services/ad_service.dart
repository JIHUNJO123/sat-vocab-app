import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb, kDebugMode;
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AdService {
  static final AdService _instance = AdService._internal();
  factory AdService() => _instance;
  static AdService get instance => _instance;
  AdService._internal();

  RewardedInterstitialAd? _rewardedAd;
  bool _isLoading = false;

  // 단어 잠금 해제 상태
  static const String _unlockKey = 'words_unlocked_until';
  DateTime? _unlockedUntil;

  // 테스트 광고 ID (개발용) - 보상형 전면광고
  static const String _testRewardedAdUnitIdAndroid =
      'ca-app-pub-3940256099942544/5354046379';
  static const String _testRewardedAdUnitIdIOS =
      'ca-app-pub-3940256099942544/6978759866';

  // SAT 보상형 광고 ID (프로덕션)
  static const String _prodRewardedAdUnitIdAndroid =
      'ca-app-pub-5837885590326347/5886067637';
  static const String _prodRewardedAdUnitIdIOS =
      'ca-app-pub-5837885590326347/9152742266';

  // 현재 환경에 맞는 광고 ID 반환
  static String get rewardedAdUnitIdAndroid =>
      kDebugMode ? _testRewardedAdUnitIdAndroid : _prodRewardedAdUnitIdAndroid;
  static String get rewardedAdUnitIdIOS =>
      kDebugMode ? _testRewardedAdUnitIdIOS : _prodRewardedAdUnitIdIOS;

  bool get isAdReady => _rewardedAd != null;

  // 단어 잠금 해제 여부 확인
  bool get isUnlocked {
    if (_unlockedUntil == null) return false;
    return DateTime.now().isBefore(_unlockedUntil!);
  }

  // 잠금 해제 상태 로드
  Future<void> loadUnlockStatus() async {
    final prefs = await SharedPreferences.getInstance();
    final timestamp = prefs.getInt(_unlockKey);
    if (timestamp != null) {
      _unlockedUntil = DateTime.fromMillisecondsSinceEpoch(timestamp);
    }
  }

  // 자정까지 잠금 해제
  Future<void> unlockUntilMidnight() async {
    final now = DateTime.now();
    final midnight = DateTime(now.year, now.month, now.day + 1);
    _unlockedUntil = midnight;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_unlockKey, midnight.millisecondsSinceEpoch);
  }

  void loadRewardedAd() {
    if (kIsWeb) return;
    // 모바일 플랫폼에서만 광고 로드
    if (!Platform.isAndroid && !Platform.isIOS) return;
    if (_isLoading || _rewardedAd != null) return;
    _isLoading = true;

    _loadAd();
  }

  void _loadAd() {
    // 모바일이 아니면 로드하지 않음
    if (!Platform.isAndroid && !Platform.isIOS) return;
    final String adUnitId =
        Platform.isIOS ? rewardedAdUnitIdIOS : rewardedAdUnitIdAndroid;

    RewardedInterstitialAd.load(
      adUnitId: adUnitId,
      request: const AdRequest(),
      rewardedInterstitialAdLoadCallback: RewardedInterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          _rewardedAd = ad;
          _isLoading = false;
        },
        onAdFailedToLoad: (error) {
          print('Rewarded interstitial ad failed to load: ${error.message}');
          _isLoading = false;
        },
      ),
    );
  }

  Future<bool> showRewardedAd({required Function onRewarded}) async {
    if (kIsWeb) {
      onRewarded();
      return true;
    }

    if (_rewardedAd == null) {
      loadRewardedAd();
      return false;
    }

    _rewardedAd!.fullScreenContentCallback = FullScreenContentCallback(
      onAdDismissedFullScreenContent: (ad) {
        ad.dispose();
        _rewardedAd = null;
        loadRewardedAd();
      },
      onAdFailedToShowFullScreenContent: (ad, error) {
        ad.dispose();
        _rewardedAd = null;
        loadRewardedAd();
      },
    );

    await _rewardedAd!.show(
      onUserEarnedReward: (ad, reward) {
        onRewarded();
      },
    );

    return true;
  }

  void dispose() {
    _rewardedAd?.dispose();
    _rewardedAd = null;
  }
}
