import datetime
import socket  # ip转换模块
import struct  # ip转换模块
import pymysql
file_name = 'C:/Users/Administrator/Desktop/0718.log'
file = open(file_name, 'r')
list_a = [a.split('|') for a in file]  # 按照|分类出来
sortLs = sorted(list_a, key=lambda x: (socket.ntohl(struct.unpack(
    "I", socket.inet_aton(str(x[0])))[0]), x[1]))  # 分别按照ip数值，及时间排序
lenLs = len(sortLs)  # 文件长度
# 提出数据并整理格式
sortLsIp = [ip[0] for ip in sortLs]  # ip存储
sortLsUrl = [Url[5] for Url in sortLs]  # URL存储\

# url分级处理
UrlBigList = []  # 所有拆分连接的存储表


def tiqu_lianjie(Url, numLeve):  # 提取所有连接段,以及需要的连接段数
    UrlSmallList = [''] * numLeve  # 每一个拆分连接的存储表
    protocol, *urlList = Url.split('//')  # 先区分开协议模式
    if urlList != []:  # 如果存在域名
        UrlSmallList[0] = protocol  # 第一个存储协议
        idx = 1  # 连接内容从第一个开始存储
        for x in urlList[0].split('/'):
            if idx < numLeve:  # 只存储规定的等级目录
                UrlSmallList[idx] = x
                idx += 1
        return(UrlSmallList)
    else:
        UrlSmallList[0] = protocol  # 第一个存储协议
        return (UrlSmallList)


for UrlCat in sortLsUrl:
    UrlBigList.append(tiqu_lianjie(UrlCat, 6))


sortLsUrlGp = [Gp[2] for Gp in sortLs]  # 获取传输存储
sortLsTime = [datetime.datetime.strptime(
    Time[1], "%d/%b/%Y:%H:%M:%S +0800") for Time in sortLs]  # 浏览时间时间
# 处理时间差及浏览状态
timeLs = []  # 存放时间差的空列表
status = []  # 0进入并跳转，1 跳转，2 跳出，3 进入并跳出 4最后跳出 5 进入并最后跳出
tiaoru = []  # 跳入链接
tiaochu = []  # 跳出链接
# 第一条处理
if sortLs[0][0] == sortLs[1][0]:  # 如果与下一个ip相等
    benci = datetime.datetime.strptime(
        sortLs[0][1], "%d/%b/%Y:%H:%M:%S +0800")  # 本次浏览时间
    xiaci = datetime.datetime.strptime(
        sortLs[1][1], "%d/%b/%Y:%H:%M:%S +0800")  # 下次浏览时间
    oneTimeDiff = (benci - xiaci).seconds  # 与下次的时间差，对应的格式时间转换
    timeLs.append(oneTimeDiff)  # 本次停留时间
    if oneTimeDiff <= 3600:  # 并且下一次跳转时间在3600秒以内,即为0进入并跳转，无跳入链接，有跳出链接
        status.append(0)
        tiaoru.append('')
        tiaochu.append(sortLs[1][5])
    else:  # 并且下一次跳转时间大于3600秒,即为3 进入并跳出，无跳入链接，无跳出链接
        status.append(3)
        tiaoru.append('')
        tiaochu.append('')
else:  # 与下一个ip不相等 即为3 进入并跳出，无跳入链接，无跳出链接
    timeLs.append(0)  # 本次停留时间0
    status.append(3)
    tiaoru.append('')
    tiaochu.append('')
# 第二条到倒数第二条
for x in range(1, lenLs - 1):
    benci = datetime.datetime.strptime(
        sortLs[x][1], "%d/%b/%Y:%H:%M:%S +0800")  # 本次浏览时间
    shangci = datetime.datetime.strptime(
        sortLs[x - 1][1], "%d/%b/%Y:%H:%M:%S +0800")  # 上次浏览时间
    xiaci = datetime.datetime.strptime(
        sortLs[x + 1][1], "%d/%b/%Y:%H:%M:%S +0800")  # 下次浏览时间
    xiaTimeDiff = (xiaci - benci).seconds  # 与下次的时间差，对应的格式时间转换
    timeDiff = (benci - shangci).seconds  # 与上次的时间差，对应的格式时间转换
    if sortLs[x][0] == sortLs[x - 1][0]:  # 如果与上一条ip相同
        if timeDiff <= 3600:  # 并且上一次的跳转时间小于3600秒，有跳入链接
            tiaoru.append(sortLs[x - 1][5])
            if sortLs[x][0] == sortLs[x + 1][0]:  # 如果与下一个ip相同
                timeLs.append(xiaTimeDiff)  # 本次停留时间
                if xiaTimeDiff <= 3600:  # 并且下一次跳转时间在3600秒以内,即为1跳转，有跳入链接，有跳出链接
                    status.append(1)
                    tiaochu.append(sortLs[x + 1][5])
                else:  # 并且下一次跳转时间大于3600秒,即为2 跳出，有跳入链接，无跳出链接
                    status.append(2)
                    tiaochu.append('')
            else:  # 与下一个ip不相等 即为2跳出，有跳入链接，无跳出链接
                timeLs.append(0)  # 本次停留时间0
                status.append(2)
                tiaochu.append('')
        else:  # 并且上一次的跳转时间大于3600秒，无跳入链接
            tiaoru.append('')
            if sortLs[x][0] == sortLs[x + 1][0]:  # 如果与下一个ip相同
                timeLs.append(xiaTimeDiff)  # 本次停留时间
                if xiaTimeDiff <= 3600:  # 并且下一次跳转时间在3600秒以内,即为0进入并跳转，无跳入链接，有跳出链接
                    status.append(0)
                    tiaochu.append(sortLs[x + 1][5])
                else:  # 并且下一次跳转时间大于3600秒,即为3 进入并跳出，无跳入链接，无跳出链接
                    status.append(3)
                    tiaochu.append('')
            else:  # 与下一个ip不相等 即为3 进入并跳出，无跳入链接，无跳出链接
                timeLs.append(0)  # 本次停留时间0
                status.append(3)
                tiaochu.append('')
    else:  # 如果与上一个ip不同
        if sortLs[x][0] == sortLs[x + 1][0]:  # 如果与下一个ip相同
            timeLs.append(xiaTimeDiff)  # 本次停留时间
            if xiaTimeDiff <= 3600:  # 并且下一次跳转时间在3600秒以内,即为0进入并跳转，无跳入链接，有跳出链接
                status.append(0)
                tiaoru.append('')
                tiaochu.append(sortLs[x + 1][5])
            else:  # 并且下一次跳转时间大于3600秒,即为3 进入并跳出，无跳入链接，无跳出链接
                status.append(3)
                tiaoru.append('')
                tiaochu.append('')
        else:  # 与下一个ip不相等 即为3 进入并跳出，无跳入链接，无跳出链接
            timeLs.append(0)  # 本次停留时间0
            status.append(3)
            tiaoru.append('')
            tiaochu.append('')
# 最后一条处理
benci = datetime.datetime.strptime(
    sortLs[lenLs - 1][1], "%d/%b/%Y:%H:%M:%S +0800")  # 本次浏览时间
shangci = datetime.datetime.strptime(
    sortLs[lenLs - 2][1], "%d/%b/%Y:%H:%M:%S +0800")  # 上次浏览时间
timeDiff = (benci - shangci).seconds  # 与上次跳转的时间差，对应的格式时间转换
timeLs.append(0)  # 本次停留时间0
if sortLs[lenLs - 1][0] == sortLs[lenLs - 2][0]:  # 如果与上一个ip相等
    if timeDiff <= 3600:  # 并且上一次跳转时间在3600秒以内,即为4最后跳出，有跳入链接，无跳出链接
        status.append(4)
        tiaoru.append('')
        tiaochu.append(sortLs[lenLs - 2][0])
    else:  # 并且上一次跳转时间大于3600秒,即为5 进入并最后跳出，无跳入链接，无跳出链接
        status.append(5)
        tiaoru.append('')
        tiaochu.append('')
else:  # 与下一个ip不相等 即为5 进入并最后跳出，无跳入链接，无跳出链接
    status.append(5)
    tiaoru.append('')
    tiaochu.append('')
# 插入数据
# 打开数据库连接
db = pymysql.connect("localhost", "ro", "8511", "loging")
# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = 'INSERT INTO loggingm (logip, logtime, url,url1,url2,url3,url4,url5, gp, timediff,status,tiaoru,tiaochu) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
args = [(str(sortLsIp[k]), str(sortLsTime[k].strftime("%Y-%m-%d %H:%M:%S")),
         str(sortLsUrl[k]), str(UrlBigList[k][0]), str(UrlBigList[k][1]), str(UrlBigList[k][2]), str(
             UrlBigList[k][3]), str(UrlBigList[k][4]), str(sortLsUrlGp[k]), str(timeLs[k]),
         str(status[k]), str(tiaoru[k]), str(tiaochu[k])) for k in range(0, lenLs)]
try:
    cursor.executemany(sql, args)
except Exception as e:
    print('执行MySQL: % s 时出错：% s' % (sql, e))
finally:
    cursor.close()
    db.commit()
    db.close()
