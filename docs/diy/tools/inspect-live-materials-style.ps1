param(
  [string]$Url = 'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$ErrorActionPreference = 'Stop'

$cacheBust = $Url + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
$ms = New-Object System.IO.MemoryStream
$resp.RawContentStream.CopyTo($ms)
$html = [Text.Encoding]::UTF8.GetString($ms.ToArray())

$needle = '.diy-materials__grid'
$ix = $html.IndexOf($needle)
if ($ix -lt 0) {
  [pscustomobject]@{ url = $Url; status = [int]$resp.StatusCode; found = $false } | ConvertTo-Json -Compress
  exit 0
}

$start = [Math]::Max(0, $ix - 400)
$len = [Math]::Min(1800, $html.Length - $start)
$snippet = $html.Substring($start, $len)
$snippet = $snippet -replace "\r|\n"," "

[pscustomobject]@{
  url = $Url
  status = [int]$resp.StatusCode
  found = $true
  snippet = $snippet
  has_autofit_substring = $html.Contains('repeat(auto-fit')
  has_maxwidth_calc_substring = $html.Contains('max-width: calc(4 * 220px + 3 * 20px)')
} | ConvertTo-Json -Compress
