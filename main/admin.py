from django.contrib import admin

from main.models import (
    Feature,
    SubscriptionProduct,
    SubscriptionProductPrice,
    SubscriptionProductFeature,
)


@admin.register(SubscriptionProduct)
class SubscriptionProductAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")


@admin.register(SubscriptionProductPrice)
class SubscriptionProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product", "is_active", "nickname", "recurring_interval", "price")


@admin.register(SubscriptionProductFeature)
class SubscriptionProductFeatureAdmin(admin.ModelAdmin):
    list_display = ("product", "feature", "value")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "unit", "default")
