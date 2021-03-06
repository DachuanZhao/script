if (Test-Path "C:\Program Files\WinRAR\WinRAR.exe"){
    $unrar_path = "C:\Program Files\WinRAR"
}else{
    $unrar_Path = read-host "请输入winrar的目标路径："
}
$unrar = $unrar_path + "\unrar.exe"

$begin_num = read-host "请输入开始编号: "
$myEnd = read-host "请输入结束编号: "
#$begin_num = 26
#$myEnd = 42
$out_path = "c:\output"
if (-not (Test-Path $out_path)){
    new-item -path c:/ -name output -type directory
}
write-host 在C盘创建输出目录output完成

$ps1_path = Split-Path -Parent $MyInvocation.MyCommand.Definition
write-host "当前脚本所在路径为："$ps1_path

#第25个字母为数字开端
$hs_rar_name_length = 25

#删除output里之前的文件
Remove-Item ($out_path + "\*") -Recurse -Force

foreach ($rar_name in (Get-ChildItem ($ps1_path + "\*.rar") -name)){

    #保留压缩包内部的文件结构，即以完整路径提取文件
    &$unrar x $rar_name $ps1_path -y
    
    #$rar_name = (Get-ChildItem ($ps1_path + "\*.rar") -name)[10]
    
    if (Test-Path ($ps1_path + "\UFT2.0_UF2.0\期货UF2.0系统\Sql\*.sql")){
        new-item -path $out_path -name $rar_name.Substring($hs_rar_name_length,$rar_name.Length-$hs_rar_name_length - 4) -type directory
        Copy-Item ($ps1_path + "\UFT2.0_UF2.0\期货UF2.0系统\Sql\*.sql") ($out_path + "\" + $rar_name.Substring($hs_rar_name_length,$rar_name.Length-$hs_rar_name_length - 4))
    }
    
    #删除解压的文件
    Get-ChildItem ($ps1_path) | ?{$_.psiscontainer -eq $true} | Remove-Item -Recurse -Force
    if (Test-Path ($ps1_path + "\readme.txt")){Remove-Item ($ps1_path + "\readme.txt") -Recurse -Force}
}


