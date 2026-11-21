# README 이미지 렌더: diagrams.html 의 각 <section id> 를 Edge headless로 캡처해 docs/images/<id>.png 로 저장
# 사용: powershell -ExecutionPolicy Bypass -File docs\diagrams\render.ps1            (전체)
#       powershell -ExecutionPolicy Bypass -File docs\diagrams\render.ps1 pipeline   (특정 섹션만)
param([string[]]$Only)
$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path (Split-Path -Parent $here) 'images'
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$sections = 'system-flow', 'collect-process', 'pipeline', 'erd', 'bio-translate', 'trial-automation', 'trial-api', 'screens'
if ($Only) { $sections = $Only }

$src = ([System.Uri](Join-Path $here 'diagrams.html')).AbsoluteUri
$profileDir = Join-Path $env:TEMP 'sportory-diagram-edge'
$scale = 1.5

Add-Type -AssemblyName System.Drawing
if (-not ('SportoryTrim' -as [type])) {
  Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System; using System.Drawing; using System.Drawing.Imaging; using System.Runtime.InteropServices;
public static class SportoryTrim {
  public static int LastContentRow(Bitmap b) {
    var d = b.LockBits(new Rectangle(0, 0, b.Width, b.Height), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
    byte[] buf = new byte[d.Stride * b.Height];
    Marshal.Copy(d.Scan0, buf, 0, buf.Length);
    b.UnlockBits(d);
    for (int y = b.Height - 1; y >= 0; y--) {
      int o = y * d.Stride;
      for (int x = 0; x < b.Width; x++) {
        int i = o + x * 4;
        if (buf[i] < 245 || buf[i + 1] < 245 || buf[i + 2] < 245) return y;
      }
    }
    return 0;
  }
}
'@
}

foreach ($s in $sections) {
  $raw = Join-Path $env:TEMP "sportory-$s-raw.png"
  if (Test-Path $raw) { Remove-Item $raw }
  $edgeArgs = @('--headless=new', '--disable-gpu', '--hide-scrollbars', "--user-data-dir=`"$profileDir`"",
                "--force-device-scale-factor=$scale", '--window-size=1200,2600', '--virtual-time-budget=4000',
                "--screenshot=`"$raw`"", "`"$src#$s`"")
  Start-Process -FilePath $edge -ArgumentList $edgeArgs -Wait -WindowStyle Hidden
  if (-not (Test-Path $raw)) { throw "캡처 실패: $s" }

  $img = [System.Drawing.Bitmap]::FromFile($raw)
  $bottom = [SportoryTrim]::LastContentRow($img)
  $h = [Math]::Min($img.Height, $bottom + 1 + [int](28 * $scale))
  $crop = $img.Clone((New-Object System.Drawing.Rectangle 0, 0, $img.Width, $h), $img.PixelFormat)
  $img.Dispose()
  $out = Join-Path $outDir "$s.png"
  $crop.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
  "{0,-18} {1}x{2}  {3} KB" -f $s, $crop.Width, $crop.Height, [int]((Get-Item $out).Length / 1KB)
  $crop.Dispose()
  Remove-Item $raw
}
