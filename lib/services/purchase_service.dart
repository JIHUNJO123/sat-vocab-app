import 'dart:async';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

class PurchaseService {
  static final PurchaseService _instance = PurchaseService._internal();
  static PurchaseService get instance => _instance;
  PurchaseService._internal();

  // ?곹뭹 ID
  static const String removeAdsProductId = 'sat_vocab_premium';
  static const Set<String> _productIds = {removeAdsProductId};

  final InAppPurchase _inAppPurchase = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _subscription;

  List<ProductDetails> _products = [];
  bool _isAvailable = false;
  bool _isPurchasePending = false;
  String? _errorMessage;

  // Getters
  List<ProductDetails> get products => _products;
  bool get isAvailable => _isAvailable;
  bool get isPurchasePending => _isPurchasePending;
  String? get errorMessage => _errorMessage;

  // 肄쒕갚
  Function()? onPurchaseSuccess;
  Function(String)? onPurchaseError;

  Future<void> initialize() async {
    // ???먮뒗 ?곗뒪?ы넲?먯꽌??IAP 鍮꾪솢?깊솕
    if (kIsWeb || (!Platform.isAndroid && !Platform.isIOS)) {
      _isAvailable = false;
      return;
    }

    _isAvailable = await _inAppPurchase.isAvailable();
    if (!_isAvailable) {
      debugPrint('In-app purchase is not available');
      return;
    }

    // 援щℓ ?ㅽ듃由?援щ룆
    _subscription = _inAppPurchase.purchaseStream.listen(
      _onPurchaseUpdate,
      onError: (error) {
        debugPrint('Purchase stream error: $error');
        _errorMessage = error.toString();
      },
    );

    // ?곹뭹 ?뺣낫 濡쒕뱶
    await _loadProducts();
  }

  Future<void> _loadProducts() async {
    if (!_isAvailable) return;

    debugPrint('Loading products for IDs: $_productIds');

    final ProductDetailsResponse response = await _inAppPurchase
        .queryProductDetails(_productIds);

    if (response.error != null) {
      debugPrint('Error loading products: ${response.error}');
      _errorMessage = response.error?.message;
      return;
    }

    if (response.notFoundIDs.isNotEmpty) {
      debugPrint('Products not found: ${response.notFoundIDs}');
      _errorMessage =
          'Product ID not found: ${response.notFoundIDs.join(", ")}';
    }

    _products = response.productDetails;
    debugPrint('Products loaded: ${_products.length}');
    for (var p in _products) {
      debugPrint('  - ${p.id}: ${p.title} - ${p.price}');
    }
  }

  void _onPurchaseUpdate(List<PurchaseDetails> purchaseDetailsList) {
    for (final purchaseDetails in purchaseDetailsList) {
      _handlePurchase(purchaseDetails);
    }
  }

  Future<void> _handlePurchase(PurchaseDetails purchaseDetails) async {
    debugPrint(
      '_handlePurchase: status=${purchaseDetails.status}, productID=${purchaseDetails.productID}',
    );

    if (purchaseDetails.status == PurchaseStatus.pending) {
      _isPurchasePending = true;
      debugPrint('  Purchase pending...');
    } else {
      _isPurchasePending = false;

      if (purchaseDetails.status == PurchaseStatus.error) {
        _errorMessage = purchaseDetails.error?.message ?? 'Purchase failed';
        debugPrint('  Purchase error: $_errorMessage');
        onPurchaseError?.call(_errorMessage!);
      } else if (purchaseDetails.status == PurchaseStatus.purchased ||
          purchaseDetails.status == PurchaseStatus.restored) {
        debugPrint('  Purchase successful or restored!');
        // 구매 성공 - 콜백 호출
        if (purchaseDetails.productID == removeAdsProductId) {
          onPurchaseSuccess?.call();
          debugPrint('  Purchase completed successfully');
        }
      } else if (purchaseDetails.status == PurchaseStatus.canceled) {
        debugPrint('  Purchase canceled by user');
        _errorMessage = 'Purchase canceled';
      }

      // 援щℓ ?꾨즺 泥섎━
      if (purchaseDetails.pendingCompletePurchase) {
        debugPrint('  Completing purchase...');
        await _inAppPurchase.completePurchase(purchaseDetails);
      }
    }
  }

  // 愿묎퀬 ?쒓굅 援щℓ
  Future<bool> buyRemoveAds() async {
    debugPrint('buyRemoveAds called');
    debugPrint('  isAvailable: $_isAvailable');
    debugPrint('  products count: ${_products.length}');

    if (!_isAvailable) {
      _errorMessage = 'In-app purchase is not available';
      debugPrint('  Error: $_errorMessage');
      return false;
    }

    if (_products.isEmpty) {
      _errorMessage =
          'No products available. Please check your internet connection.';
      debugPrint('  Error: $_errorMessage');
      return false;
    }

    final ProductDetails? product = _products
        .cast<ProductDetails?>()
        .firstWhere((p) => p?.id == removeAdsProductId, orElse: () => null);

    if (product == null) {
      _errorMessage = 'Product "$removeAdsProductId" not found';
      debugPrint('  Error: $_errorMessage');
      return false;
    }

    debugPrint('  Purchasing product: ${product.id} - ${product.price}');

    // 鍮꾩냼紐⑥꽦 ?곹뭹?쇰줈 援щℓ
    final PurchaseParam purchaseParam = PurchaseParam(productDetails: product);
    try {
      final result = await _inAppPurchase.buyNonConsumable(
        purchaseParam: purchaseParam,
      );
      debugPrint('  Purchase initiated: $result');
      return result;
    } catch (e) {
      _errorMessage = e.toString();
      debugPrint('  Purchase error: $e');
      return false;
    }
  }

  // 援щℓ 蹂듭썝
  Future<void> restorePurchases() async {
    if (!_isAvailable) return;
    await _inAppPurchase.restorePurchases();
  }

  // 愿묎퀬 ?쒓굅 ?곹뭹 媛寃?媛?몄삤湲?
  String? getRemoveAdsPrice() {
    final product =
        _products.where((p) => p.id == removeAdsProductId).firstOrNull;
    return product?.price;
  }

  void dispose() {
    _subscription?.cancel();
  }
}

