param (
    [string]$buildArtifactStagingDirectory,
    [string]$targetDirectory,
    [string]$versionStampFile
)

if (!(Test-Path -Path $targetDirectory)) {
    New-Item -ItemType Directory -Path $targetDirectory
}

Copy-Item -Path "$buildArtifactStagingDirectory\*" -Destination $targetDirectory -Recurse -Force

$versionFilePath = "$targetDirectory\$versionStampFile"
if (Test-Path $versionFilePath) {
    $version = Get-Content -Path $versionFilePath
    $newVersion = [int]$version + 1
} else {
    $newVersion = 1
}
$newVersion | Out-File -FilePath $versionFilePath

