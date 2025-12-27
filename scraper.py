import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import json
import datetime

# 模拟浏览器请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'https://www.baidu.com/'
}

def get_baidu_hot_search():
    url = "https://top.baidu.com/board?tab=realtime"
    hot_list = []
    try:
        print(f"尝试使用 requests 抓取百度热搜: {url} (verify=False)")
        response = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select('div.category-wrap_i4-Km') # 你的CSS选择器

        if not items:
            print("警告：百度热搜页面未找到匹配的热搜条目，请检查CSS选择器是否正确。")
            return []

        for i, item in enumerate(items):
            title_tag = item.select_one('a.c-single-text-ellipsis')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href')
            else:
                continue

            hot_value_tag = item.select_one('div.hot-index_1Lk54')
            hot_value = hot_value_tag.get_text(strip=True) if hot_value_tag else "N/A"

            rank_tag = item.select_one('div.category-rank_D_2_X')
            rank = int(rank_tag.get_text(strip=True)) if rank_tag and rank_tag.get_text(strip=True).isdigit() else (i + 1)

            hot_list.append({
                "title": title,
                "url": link,
                "source": "百度热搜",
                "rank": rank,
                "hot_value": hot_value
            })
        print(f"成功抓取百度热搜 {len(hot_list)} 条。")
        return hot_list

    except requests.exceptions.RequestException as e:  # 修正异常类型
        print(f"抓取百度热搜失败: {e}")
    except Exception as e:
        print(f"解析百度热搜数据失败: {e}")
    return []

def get_weibo_hot_search():
    url = "https://s.weibo.com/top/summary"
    hot_list = []
    try:
        print(f"尝试抓取微博热搜: {url}")
        response = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('table.table tbody tr')[1:21]  # 跳过表头，取前20条
        for i, item in enumerate(items, 1):
            title_tag = item.select_one('td a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = "https://s.weibo.com" + title_tag.get('href')
            else:
                continue
            hot_value_tag = item.select_one('td.td-02 span')
            hot_value = hot_value_tag.get_text(strip=True) if hot_value_tag else "N/A"
            hot_list.append({
                "title": title,
                "url": link,
                "source": "微博热搜",
                "rank": i,
                "hot_value": hot_value
            })
        print(f"成功抓取微博热搜 {len(hot_list)} 条。")
        return hot_list
    except Exception as e:
        print(f"抓取微博热搜失败: {e}")
    return []

def get_mock_hot_topics():
    """返回模拟的热榜数据，用于测试和演示"""
    mock_data = [
        {
            "title": "今日热点新闻1",
            "url": "https://news.sina.com.cn/",
            "source": "百度热搜",
            "rank": 1,
            "hot_value": "1,234,567"
        },
        {
            "title": "热门话题讨论2",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 2,
            "hot_value": "987,654"
        },
        {
            "title": "社会热点事件3",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 3,
            "hot_value": "876,543"
        },
        {
            "title": "娱乐新闻热点4",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 4,
            "hot_value": "765,432"
        },
        {
            "title": "科技资讯更新5",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 5,
            "hot_value": "654,321"
        },
        {
            "title": "体育赛事报道6",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 6,
            "hot_value": "543,210"
        },
        {
            "title": "财经市场动态7",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 7,
            "hot_value": "432,109"
        },
        {
            "title": "健康生活资讯8",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 8,
            "hot_value": "321,098"
        },
        {
            "title": "教育政策更新9",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 9,
            "hot_value": "210,987"
        },
        {
            "title": "国际新闻热点10",
            "url": "https://top.baidu.com/board?tab=realtime",
            "source": "百度热搜",
            "rank": 10,
            "hot_value": "109,876"
        }
    ]
    print(f"返回模拟热榜数据 {len(mock_data)} 条")
    return mock_data

def get_mock_weibo_hot_topics():
    """返回模拟的微博热搜数据"""
    mock_data = [
        {
            "title": "微博热搜话题1",
            "url": "https://weibo.com/example1",
            "source": "微博热搜",
            "rank": 1,
            "hot_value": "2,345,678"
        },
        {
            "title": "微博热搜话题2",
            "url": "https://weibo.com/example2",
            "source": "微博热搜",
            "rank": 2,
            "hot_value": "1,987,654"
        },
        {
            "title": "微博热搜话题3",
            "url": "https://weibo.com/example3",
            "source": "微博热搜",
            "rank": 3,
            "hot_value": "1,876,543"
        },
        {
            "title": "微博热搜话题4",
            "url": "https://weibo.com/example4",
            "source": "微博热搜",
            "rank": 4,
            "hot_value": "1,765,432"
        },
        {
            "title": "微博热搜话题5",
            "url": "https://weibo.com/example5",
            "source": "微博热搜",
            "rank": 5,
            "hot_value": "1,654,321"
        },
        {
            "title": "微博热搜话题6",
            "url": "https://weibo.com/example6",
            "source": "微博热搜",
            "rank": 6,
            "hot_value": "1,543,210"
        },
        {
            "title": "微博热搜话题7",
            "url": "https://weibo.com/example7",
            "source": "微博热搜",
            "rank": 7,
            "hot_value": "1,432,109"
        },
        {
            "title": "微博热搜话题8",
            "url": "https://weibo.com/example8",
            "source": "微博热搜",
            "rank": 8,
            "hot_value": "1,321,098"
        },
        {
            "title": "微博热搜话题9",
            "url": "https://weibo.com/example9",
            "source": "微博热搜",
            "rank": 9,
            "hot_value": "1,210,987"
        },
        {
            "title": "微博热搜话题10",
            "url": "https://weibo.com/example10",
            "source": "微博热搜",
            "rank": 10,
            "hot_value": "1,109,876"
        }
    ]
    print(f"返回模拟微博热搜数据 {len(mock_data)} 条")
    return mock_data

# 修改get_all_hot_topics，合并百度和微博热搜

def get_all_hot_topics():
    baidu = get_baidu_hot_search()
    weibo = get_weibo_hot_search()
    if not baidu:
        baidu = get_mock_hot_topics()
    if not weibo:
        weibo = get_mock_weibo_hot_topics()
    return baidu + weibo

# get_weibo_hot_search 和 main 函数保持不变
# ... (其余代码) ...