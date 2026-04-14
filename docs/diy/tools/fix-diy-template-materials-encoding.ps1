$ErrorActionPreference = 'Stop'

# Fix encoding issues inside the DIY metaobject template (theme asset):
# - templates/metaobject/diy_experience.json
#
# Specifically targets the "materials/products" Custom Liquid block labels that
# sometimes end up stored as U+FFFD replacement chars (rendering as "�").
#
# This script stays ASCII by constructing non-ASCII chars from codepoints.

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'

$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}

if (-not $shopDomain -or -not $token) {
  throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile"
}

$headersGet = @{ 'X-Shopify-Access-Token' = $token }
$headersPut = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }

$themeId = '196991385938' # Maerz 2026 (main theme)

function StrFromCodes([int[]]$codes) {
  $sb = New-Object System.Text.StringBuilder
  foreach ($c in $codes) { [void]$sb.Append([char]$c) }
  return $sb.ToString()
}

# Replacement character: "�" (U+FFFD). Build from codepoint to keep this file ASCII.
$repl = [string][char]0xFFFD

# Bad strings (as currently rendered in-store).
$bad_auswaehlen = 'Ausw' + $repl + 'hlen'
$bad_ausgewaehlte = 'Ausgew' + $repl + 'hlte'

# Good strings using HTML entities (ASCII-only, avoids future encoding issues).
$good_auswaehlen = 'Ausw&auml;hlen'
$good_ausgewaehlte = 'Ausgew&auml;hlte'

$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value

$fixed = $orig.
  Replace($bad_auswaehlen, $good_auswaehlen).
  Replace($bad_ausgewaehlte, $good_ausgewaehlte)

# Also defensively normalize already-correct umlauts if someone pasted them into the JSON.
# (Keeps it ASCII in-store, reducing the chance of mojibake in future edits.)
$ae = [string][char]0x00E4
$fixed = $fixed.
  Replace('Ausw' + $ae + 'hlen', $good_auswaehlen).
  Replace('Ausgew' + $ae + 'hlte', $good_ausgewaehlte)

# Sanity: ensure we didn't break JSON.
$jsonOk = $true
try { $null = $fixed | ConvertFrom-Json -ErrorAction Stop } catch { $jsonOk = $false }
if (-not $jsonOk) { throw "Refusing to push: $assetKey is not valid JSON after fix." }

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 50
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

# Post-check: ensure the asset no longer contains U+FFFD.
$hasReplInAsset = $fixed.Contains($repl)

# Live verification (raw UTF-8 bytes; avoids misleading PowerShell text decoding).
$urls = @(
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj',
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$results = @()
foreach ($u in $urls) {
  $cacheBust = $u + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing

  $ms = New-Object System.IO.MemoryStream
  $resp.RawContentStream.CopyTo($ms)
  $bytes = $ms.ToArray()
  $html = [Text.Encoding]::UTF8.GetString($bytes)

  $labelMatch = ''
  $labelCodepoints = @()
  $m = [regex]::Match($html, 'Ausw.{0,6}hlen')
  if ($m.Success) {
    $labelMatch = $m.Value
    foreach ($ch in $labelMatch.ToCharArray()) { $labelCodepoints += [int][char]$ch }
  }

  $results += [pscustomobject]@{
    url = $u
    status = [int]$resp.StatusCode
    has_replacement_char = $html.Contains($repl)
    has_entity_auswaehlen = $html.Contains($good_auswaehlen)
    has_entity_ausgewaehlte = $html.Contains($good_ausgewaehlte)
    first_ausw_label_match = $labelMatch
    first_ausw_label_codepoints = $labelCodepoints
  }
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  changed = $changed
  asset_has_replacement_char = $hasReplInAsset
  checks = $results
} | ConvertTo-Json -Compress
