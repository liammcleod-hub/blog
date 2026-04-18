# Shopify Blog Pipeline

This directory contains tools and scripts for integrating with the Bastelschachtel Shopify blog.

## Shopify Skills Available

Based on the available skills, we can use:

1. `shopify-admin` - For accessing Shopify admin APIs
2. `shopify-storefront-graphql` - For storefront operations
3. `shopify-custom-data` - For working with Metafields and Metaobjects

## Environment Setup

The following environment variables need to be set in `.env`:

```
SHOPIFY_ACCESS_TOKEN=your_admin_api_token_here
SHOPIFY_SHOP_DOMAIN=bastelschachtel.myshopify.com
```

## Integration Plan

1. Use `shopify-admin` skill to fetch blog articles
2. Parse HTML content to markdown for analysis
3. Apply SEO optimizations
4. Publish updated articles back via Shopify API

## Key Operations

- Fetch blog articles by handle
- Convert HTML to markdown for analysis
- Apply SEO improvements
- Publish updated articles

## Next Steps

1. Populate SHOPIFY_ACCESS_TOKEN in .env
2. Test connection with shopify-admin skill
3. Implement article fetching and parsing
4. Build optimization pipeline