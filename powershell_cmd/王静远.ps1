#新建一个hash表，用来存储数据，参见http://www.pstips.net/powershell-using-hash-tables.html
$dataBase = @{}

#创建数据表，第一列表示步骤号，第二列表示应该有的步骤
$dataBase."4" = "lcw4zz1","su zz1svc","svc4zz1"
$dataBase."5" = "ping zz1sysoo1-e0"
$dataBase."6" = "ping zz1sysoo1-e1"
$dataBase."7" = "cd /usr/users/zz1svc"
$dataBase."8" = "cd etc"
$dataBase."9" = "ls"
$dataBase."10" = "vi ptopZONEZDZATS1.stderrout"
$dataBase."11" = "/dor"
$dataBase."12" = ":q"
$dataBase."13" = "ssh zz1s53ats","svc4zz1"
$dataBase."14" = ":q"
$dataBase."15" = "su","enter","reboot"
$dataBase."16" = "exit"

#主代码开始
write-host "即将开始第4步到第16步测试命令，每次输入命令后按回车键继续"

for(;;){
    $id = Read-Host "请输入题号，并按回车"
    if($id -eq 0){
        break
    }
    foreach($command in $dataBase.$id){
        for(;;){
            $commandInput = Read-Host "请输入命令，并按回车"
            if($commandInput -eq $command){
                Write-Host "输入正确，请继续输入此步骤下一条命令"
                break
            }else{
                Write-Host "输入错误，请重新输入"
            }    
        }
    }
}


