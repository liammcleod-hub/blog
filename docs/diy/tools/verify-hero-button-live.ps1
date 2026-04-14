param(
  [string]$Url = 'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$ErrorActionPreference = 'Stop'

$cacheBust = $Url + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
$ms = New-Object System.IO.MemoryStream
$resp.RawContentStream.CopyTo($ms)
$html = [Text.Encoding]::UTF8.GetString($ms.ToArray())

$hasAnchor = $html.Contains('diy-steps-anchor')
$hasButton = $html.Contains('diy.download_file.value') -or $html.Contains('#diy-steps-anchor') -or $html.Contains('PDF herunterladen') -or $html.Contains('Zu den Schritten')

[pscustomobject]@{
  url = $Url
  status = [int]$resp.StatusCode
  has_steps_anchor_markup = $hasAnchor
  has_scroll_href = $html.Contains('#diy-steps-anchor')
} | ConvertTo-Json -Compress

