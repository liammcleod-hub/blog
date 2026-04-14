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

$themeId = '196991385938' # Maerz 2026
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value
$template = $orig | ConvertFrom-Json -ErrorAction Stop

$btn = $template.sections.section_Hca4zN.blocks.group_rjq9Lc.blocks.button_wEwTDT
if (-not $btn) { throw "button_wEwTDT not found in section_Hca4zN/group_rjq9Lc." }
if ($btn.type -ne 'custom-liquid') { throw "button_wEwTDT is not custom-liquid (type=$($btn.type))." }

$liquid = @'
{% assign diy = closest.metaobject.diy_experience %}
{% assign url = diy.download_url.value | strip %}
{% assign file = diy.download_file.value %}
{% assign label = diy.download_button_label.value | strip %}

{% if url != blank %}
  {% if label == blank %}{% assign label = 'Download' %}{% endif %}
  <a class="button" href="{{ url | escape }}" target="_blank" rel="noopener">{{ label | escape }}</a>
{% elsif file != blank %}
  {% if label == blank %}{% assign label = 'Download' %}{% endif %}
  <a class="button" href="{{ diy.download_file.value | file_url }}" target="_blank" rel="noopener">{{ label | escape }}</a>
{% else %}
  {% if label == blank %}{% assign label = 'Zu den Schritten' %}{% endif %}
  <a class="button" href="#diy-steps-anchor">{{ label | escape }}</a>
{% endif %}
'@

$btn.settings.custom_liquid = $liquid
$template.sections.section_Hca4zN.blocks.group_rjq9Lc.blocks.button_wEwTDT = $btn

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
} | ConvertTo-Json -Compress
