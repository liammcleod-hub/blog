$ErrorActionPreference = 'Stop'

$urls = @(
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj',
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$repl = [string][char]0xFFFD
$reMaxWidth = [regex]'max-width:\s*calc\(\s*4\s*\*\s*220px\s*\+\s*3\s*\*\s*20px\s*\)'

$out = @()
foreach ($u in $urls) {
  $cacheBust = $u + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
  $ms = New-Object System.IO.MemoryStream
  $resp.RawContentStream.CopyTo($ms)
  $html = [Text.Encoding]::UTF8.GetString($ms.ToArray())

  $out += [pscustomobject]@{
    url = $u
    status = [int]$resp.StatusCode
    has_replacement_char = $html.Contains($repl)
    has_materials_markup = ($html.Contains('diy-materials__grid') -or $html.Contains('diy-materials-'))
    has_autofit = $html.Contains('repeat(auto-fit')
    has_materials_maxwidth = $reMaxWidth.IsMatch($html)
  }
}

$out | ConvertTo-Json -Compress
