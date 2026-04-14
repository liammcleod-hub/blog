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

$sec = $template.sections.section_Hi3V48
$g1 = $sec.blocks.group_8RBniT
$g2 = $g1.blocks.group_phhc36

function KeysOf($obj) {
  if ($null -eq $obj) { return @() }
  if ($obj -is [System.Collections.IDictionary]) { return @($obj.Keys) }
  return @($obj.PSObject.Properties.Name)
}

$g1Keys = KeysOf $g1.blocks
$g2Keys = KeysOf $g2.blocks

[pscustomobject]@{
  section = 'section_Hi3V48'
  group1 = 'group_8RBniT'
  group1_inner_blocks = $g1Keys
  group2 = 'group_phhc36'
  group2_inner_blocks = $g2Keys
} | ConvertTo-Json -Compress -Depth 6

