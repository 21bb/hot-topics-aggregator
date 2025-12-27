from flask import Flask, jsonify, render_template
from flask_cors import CORS # 用于处理跨域请求
from scraper import get_all_hot_topics # 导入我们刚刚编写的抓取函数
import threading
import time
import atexit # 用于在程序退出时执行清理
import os # 用于读取环境变量

app = Flask(__name__)

# 生产环境配置：根据环境变量限制CORS
# 开发环境允许所有来源，生产环境应限制为你的前端域名
if os.getenv('FLASK_ENV') == 'production':
    # 生产环境：限制CORS来源（替换为你的实际域名）
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'https://your-domain.com').split(',')
    CORS(app, origins=allowed_origins)
else:
    # 开发环境：允许所有来源
    CORS(app)

# 用于存储热榜数据，全局变量
cached_hot_topics = []
last_update_time = 0

# 用于控制更新线程的停止
update_thread_stop_event = threading.Event()

def update_hot_topics_cache():
    """定期更新热榜数据缓存的函数"""
    global cached_hot_topics, last_update_time
    while not update_thread_stop_event.is_set(): # 检查停止事件
        print("正在更新热榜数据缓存...")
        new_topics = get_all_hot_topics()
        if new_topics: # 只有当成功抓取到数据时才更新
            cached_hot_topics = new_topics
            last_update_time = time.time()
            print(f"热榜数据缓存更新完成，共 {len(cached_hot_topics)} 条。")
        else:
            print("未抓取到新数据，保持旧缓存。")
        
        # 等待一段时间，或者直到停止事件被设置
        update_thread_stop_event.wait(timeout=300) # 每 5 分钟更新一次数据，根据需求调整

# 在应用启动时启动一个线程来定期更新数据
# daemon=True 确保主程序退出时线程也退出
update_thread = threading.Thread(target=update_hot_topics_cache, daemon=True)

# 初始化数据的函数（在后台线程中执行，不阻塞启动）
def init_data_in_background():
    """在后台线程中初始化数据，避免阻塞应用启动"""
    global cached_hot_topics, last_update_time
    try:
        print("后台初始化：开始抓取热榜数据...")
        topics = get_all_hot_topics()
        if topics:
            cached_hot_topics = topics
            last_update_time = time.time()
            print(f"后台初始化完成，共 {len(cached_hot_topics)} 条数据。")
        else:
            print("后台初始化：未获取到数据，将使用模拟数据。")
    except Exception as e:
        print(f"后台初始化出错: {e}，将使用模拟数据。")

# 应用启动时自动初始化（适用于 gunicorn 启动）
# Flask 2.0+ 兼容方式：在模块加载时启动
if not update_thread.is_alive():
    update_thread.start()
    # 初始化数据
    init_thread = threading.Thread(target=init_data_in_background, daemon=True)
    init_thread.start()

# 注册一个函数，在程序退出时设置停止事件，确保线程优雅退出
@atexit.register
def stop_update_thread():
    print("正在停止更新线程...")
    update_thread_stop_event.set()
    update_thread.join(timeout=5) # 等待线程最多5秒钟结束
    if update_thread.is_alive():
        print("更新线程未能及时停止。")
    else:
        print("更新线程已停止。")

@app.route('/')
def index():
    """渲染前端页面"""
    # Flask 会在 'templates' 文件夹中寻找 'index.html'
    return render_template('index.html')

@app.route('/api/hot_topics')
def hot_topics_api():
    """提供热榜数据的API接口"""
    global cached_hot_topics, last_update_time
    # 如果缓存为空，立即抓取一次数据
    if not cached_hot_topics:
        print("缓存为空，立即抓取数据...")
        cached_hot_topics = get_all_hot_topics()
        last_update_time = time.time()
        print(f"数据抓取完成，共 {len(cached_hot_topics)} 条。")
    
    # 返回缓存的数据
    if last_update_time > 0:
        last_update_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_update_time))
    else:
        last_update_str = ""
    return jsonify({
        "data": cached_hot_topics,
        "last_update": last_update_str
    })

# 初始化数据的函数（在后台线程中执行，不阻塞启动）
def init_data_in_background():
    """在后台线程中初始化数据，避免阻塞应用启动"""
    global cached_hot_topics, last_update_time
    try:
        print("后台初始化：开始抓取热榜数据...")
        topics = get_all_hot_topics()
        if topics:
            cached_hot_topics = topics
            last_update_time = time.time()
            print(f"后台初始化完成，共 {len(cached_hot_topics)} 条数据。")
        else:
            print("后台初始化：未获取到数据，将使用模拟数据。")
    except Exception as e:
        print(f"后台初始化出错: {e}，将使用模拟数据。")

if __name__ == '__main__':
    # 启动后台更新线程（会自动初始化数据）
    update_thread.start()
    
    # 在另一个线程中初始化数据，不阻塞主线程
    init_thread = threading.Thread(target=init_data_in_background, daemon=True)
    init_thread.start()

    # 运行 Flask 应用
    # 从环境变量获取配置，如果没有则使用默认值
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    
    # 生产环境必须关闭 debug 模式
    if os.getenv('FLASK_ENV') == 'production':
        debug_mode = False
    
    print(f"Flask 应用启动在 {host}:{port}")
    app.run(debug=debug_mode, host=host, port=port)