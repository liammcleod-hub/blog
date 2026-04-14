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

$sectionBlockKeys = @()
if ($sec.blocks -is [System.Collections.IDictionary]) { $sectionBlockKeys = @($sec.blocks.Keys) }
else { $sectionBlockKeys = @($sec.blocks.PSObject.Properties.Name) }

$groups = @()
foreach ($bk in $sectionBlockKeys) {
  $b = $sec.blocks.$bk
  $innerKeys = @()
  if ($null -ne $b.blocks) {
    if ($b.blocks -is [System.Collections.IDictionary]) { $innerKeys = @($b.blocks.Keys) }
    else { $innerKeys = @($b.blocks.PSObject.Properties.Name) }
  }
  $groups += [pscustomobject]@{
    group_key = $bk
    type = $b.type
    inner_block_count = $innerKeys.Count
    first_inner_blocks = ($innerKeys | Select-Object -First 30)
  }
}

[pscustomobject]@{
  section = 'section_Hi3V48'
  section_blocks = $groups
} | ConvertTo-Json -Compress -Depth 8

