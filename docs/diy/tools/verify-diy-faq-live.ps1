param(
  [string]$Url = 'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$ErrorActionPreference = 'Stop'

$cacheBust = $Url + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
$ms = New-Object System.IO.MemoryStream
$resp.RawContentStream.CopyTo($ms)
$html = [Text.Encoding]::UTF8.GetString($ms.ToArray())

[pscustomobject]@{
  url = $Url
  status = [int]$resp.StatusCode
  has_diy_faq_markup = $html.Contains('diy-faq-')
  has_faqpage_jsonld = $html.Contains('"@type": "FAQPage"')
} | ConvertTo-Json -Compress
