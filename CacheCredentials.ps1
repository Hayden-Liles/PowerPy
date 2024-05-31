##########################################################################################################################
#
# Created By: Isaac McLaughlin
# 
# Description: This script will prompt users to cache credentials to be used with other scripts made by Isaac. It prompts
# the user to input credentials (User's username + _A should auto populate). Once they are input, it will save the encrypted
# information in a .key file on the users Home drive (F:\temp\cred.key). It also logs use. 
#
# ChangeLog:
# -v1-
# 10/31/2019 - Script completed and moved to "production".
#
# ToDo:
# - error handling
#
##########################################################################################################################

$key = [byte]1..16
    $keyLocation = "\\home.slhs.org\" + $env:username + "$" + "\temp\cred.key"
    $OneDriveUse = $false
    if(!([string]::IsNullOrEmpty($env:OneDrive))){
        if(Test-Path $Env:OneDrive){
            $keylocation = $env:OneDrive + "\temp\cred.key"
            Write-Host "Using OneDrive..."
            $OneDriveUse = $true
        }
    }

Function Get-UserCredential {
    if ($script:Creds -eq $null) {
        try{
            $UN = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name + '_a'
            Write-Host "Please input Admin credentials:" -ForegroundColor black -BackgroundColor Green
            $script:Creds = Get-Credential -Credential $UN -ErrorAction Ignore

            }
        Catch{
            #write-timestamp
            write-host "There was an error" -ForegroundColor red
            pause
            Get-UserCredential
            }
        }
    Else {
        #Credentials already entered
        #Do Nothing / Continue
        }
}

Function Encrypt-UserCredential {
    $CachedCreds = Test-Path -Path $KeyLocation
    if ($CachedCreds -ne "True"){
        $newkey = New-Item -Path $keyLocation -Force
        }
    try {
        Write-Host "Caching Credentials..."
        #$script:Creds.Password | ConvertFrom-SecureString -Key $Key | Set-Content F:\temp\cred.key -Force
        $script:Creds.Password | ConvertFrom-SecureString -Key $Key | Set-Content $keyLocation -Force
        Write-Host "Credentials Cached!" -ForegroundColor Green
        } Catch {
        Write-Host "There was an error..." -ForegroundColor Red
        pause
        Encrypt-UserCredential
        }
    }

Function Intro {
    Write-host "This script will cache your admin credentials to be used with other scripts"
    pause
    }

function Write-LogUse {
    try {
        $LogStamp = (Get-Date).toString("yyyy/MM/dd HH:mm:ss")
        $useLogLocation = "\\IHT\desktopsupport$\Temp\Logs\Creds\Credential Use.log"
        $line = "$logstamp - User: $env:username - Cache Credentials - $env:COMPUTERNAME - One Drive Use: $onedriveuse"
        $addlog = Add-Content -PassThru $useloglocation -Value $line -force
        }
    Catch {
        #Do Nothing 
        }
    }  

Function MeatAndPotatoes {
    Intro
    Get-UserCredential
    Encrypt-UserCredential
    Write-LogUse
    Pause
    }

MeatAndPotatoes