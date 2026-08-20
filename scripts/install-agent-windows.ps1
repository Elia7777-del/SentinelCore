param(
  [Parameter(Mandatory=$true)][string]$ApiBaseUrl,
  [Parameter(Mandatory=$true)][string]$EnrollmentToken
)

$ErrorActionPreference = "Stop"
Write-Host "SentinelCore agent enrollment"
Write-Host "API: $ApiBaseUrl"
Write-Host "Enrollment token received."
Write-Host "Production requirement: install a signed, independently tested agent package."
# This script intentionally does not download or execute an untrusted binary.
