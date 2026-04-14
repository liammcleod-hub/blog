$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$headersGet = @{ 'X-Shopify-Access-Token' = $token }
$themeId = '196991385938'
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
$value = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  has_custom_liquid_faq = $value.Contains('custom_liquid_faq')
  has_faqpage_jsonld = $value.Contains('FAQPage')
  references_faq_items_field = $value.Contains('diy.faq_items.value')
} | ConvertTo-Json -Compress
