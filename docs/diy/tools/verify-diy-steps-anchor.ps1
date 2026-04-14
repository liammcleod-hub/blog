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
$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value
$template = $orig | ConvertFrom-Json -ErrorAction Stop

$stepsLiquid = $template.sections.section_PQQgbR.blocks.group_KJ6ae3.blocks.group_TaPk8k.blocks.group_tUmKXk.blocks.custom_liquid_steps_grid.settings.custom_liquid

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  has_anchor_substring = ($stepsLiquid -match 'diy-steps-anchor')
  sample = ($stepsLiquid.Substring(0, [Math]::Min(220, $stepsLiquid.Length)))
} | ConvertTo-Json -Compress

