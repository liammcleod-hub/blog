$ErrorActionPreference = 'Stop'

$url = 'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj'
$cacheBust = $url + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
$ms = New-Object System.IO.MemoryStream
$resp.RawContentStream.CopyTo($ms)
$html = [Text.Encoding]::UTF8.GetString($ms.ToArray())

# Find anchors whose class contains the token "button".
$matches = [regex]::Matches(
  $html,
  '<a[^>]*class=\"[^\"]*\\bbutton\\b[^\"]*\"[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>',
  'IgnoreCase'
)

$href = ''
$text = ''
$found = $false
if ($matches.Count -gt 0) {
  $found = $true
  $href = $matches[0].Groups[1].Value
  # Best-effort strip tags inside the anchor.
  $text = ($matches[0].Groups[2].Value -replace '<[^>]+>', '') -replace '\\s+', ' '
  $text = $text.Trim()
}

[pscustomobject]@{
  url = $url
  status = [int]$resp.StatusCode
  found_button = $found
  href = $href
  text = $text
  href_has_pdf = ($href -match '\\.pdf(\\?|$)') -or ($href -match '\\.PDF(\\?|$)')
} | ConvertTo-Json -Compress
