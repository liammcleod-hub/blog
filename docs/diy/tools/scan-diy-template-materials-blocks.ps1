$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$headers = @{ 'X-Shopify-Access-Token' = $token }
$themeId = '196991385938'
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$value = (Invoke-RestMethod -Uri $getUrl -Headers $headers -Method Get).asset.value

$matches = [regex]::Matches($value, '\.diy-materials__grid')
$blocks = @()
foreach ($m in $matches) {
  $start = [Math]::Max(0, $m.Index - 200)
  $len = [Math]::Min(900, $value.Length - $start)
  $snippet = $value.Substring($start, $len)
  $blocks += [pscustomobject]@{
    index = $m.Index
    has_autofit = $snippet.Contains('repeat(auto-fit')
    has_repeat4 = $snippet.Contains('repeat(4, minmax(0, 220px))')
    snippet = $snippet
  }
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  occurrences = $blocks.Count
  blocks = $blocks
} | ConvertTo-Json -Compress -Depth 6

