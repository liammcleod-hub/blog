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
$headersPut = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }

$themeId = '196991385938'
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value
$template = $orig | ConvertFrom-Json -ErrorAction Stop

$stepsLiquid = $template.sections.section_PQQgbR.blocks.group_KJ6ae3.blocks.group_TaPk8k.blocks.group_tUmKXk.blocks.custom_liquid_steps_grid.settings.custom_liquid
if (-not $stepsLiquid) { throw "Steps custom liquid not found at expected path." }

$before = $stepsLiquid

# Ensure the anchor exists and has scroll-margin-top so it lands at the section top below sticky header.
if ($stepsLiquid -notmatch 'diy-steps-anchor') { throw "diy-steps-anchor not found; run the hero-button script first." }

if ($stepsLiquid -notmatch 'scroll-margin-top') {
  # Robust: add the style attribute onto the id attribute directly (works for escaped + unescaped variants).
  $stepsLiquid = $stepsLiquid.Replace('id="diy-steps-anchor"', 'id="diy-steps-anchor" style="scroll-margin-top: 120px;"')
  $stepsLiquid = $stepsLiquid.Replace('id=\"diy-steps-anchor\"', 'id=\"diy-steps-anchor\" style=\"scroll-margin-top: 120px;\"')
}

$template.sections.section_PQQgbR.blocks.group_KJ6ae3.blocks.group_TaPk8k.blocks.group_tUmKXk.blocks.custom_liquid_steps_grid.settings.custom_liquid = $stepsLiquid

$fixed = $template | ConvertTo-Json -Depth 90 -Compress
$null = $fixed | ConvertFrom-Json -ErrorAction Stop

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 20
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  changed = $changed
  anchor_has_scroll_margin = ($stepsLiquid -match 'scroll-margin-top')
} | ConvertTo-Json -Compress
