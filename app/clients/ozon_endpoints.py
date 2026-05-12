"""Canonical Ozon Seller API endpoint paths used by the service layer."""


class OzonEndpoint:
    CATEGORY_TREE = "v1/description-category/tree"
    CATEGORY_ATTRIBUTES = "v1/description-category/attribute"
    CATEGORY_ATTRIBUTE_VALUES = "v1/description-category/attribute/values"
    CATEGORY_ATTRIBUTE_VALUES_SEARCH = "v1/description-category/attribute/values/search"

    PRODUCT_INFO_LIMIT = "v4/product/info/limit"
    PRODUCT_IMPORT = "v3/product/import"
    PRODUCT_IMPORT_INFO = "v1/product/import/info"
    PRODUCT_ATTRIBUTES_UPDATE = "v1/product/attributes/update"
    PRODUCT_PICTURES_IMPORT = "v1/product/pictures/import"
    PRODUCT_INFO_LIST = "v3/product/info/list"
    PRODUCT_INFO_ATTRIBUTES = "v4/product/info/attributes"
    PRODUCT_INFO_STOCKS = "v4/product/info/stocks"

    PRODUCT_ARCHIVE = "v1/product/archive"
    PRODUCT_UNARCHIVE = "v1/product/unarchive"

    SELLER_INFO = "v1/seller/info"
    WAREHOUSE_LIST = "v2/warehouse/list"
    PRODUCTS_STOCKS_UPDATE = "v2/products/stocks"
