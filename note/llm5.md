上节课的补丁：

修复bug：在首页点进其他用户的个人空间后，再去右上角点击自己的个人空间，页面内容没更新。
1. 实现聊天后端
安装langgraph：pip install langgraph langchain langchain_openai

安装python-dotenv：pip install python-dotenv，负责加载环境变量

1.1 创建数据库
在AIFriends/backend/web/models/friend.py中创建数据库Message。

1.2 实现views
注册阿里云账号：https://www.aliyun.com/
打开阿里云百练平台：https://bailian.console.aliyun.com/cn-beijing/#/home
阿里云DeepSeek文档：https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2868565

在模型服务 -> 秘钥管理 中创建API Key
创建文件：AIFriends/backend/.env，用来存环境变量。

在AIFriends/.gitignore中添加*.env。
如果git status后仍然有.env，可以执行：git rm --cached -f backend/.env来清除对.env的索引。
在文件中添加：
API_KEY=""  # 替换成自己创建的API Key
API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
在AIFriends/backend/backend/settings.py开头添加：

from dotenv import load_dotenv

load_dotenv()
然后要重启Django服务，这样才可以加载环境变量。

实现AIFriends/backend/web/views/friend/message/chat/chat.py。

langgraph数据类型：

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
1.3 添加路由
在AIFriends/backend/web/urls.py中添加路由。

2. 实现聊天前端
打开聊天页面后，自动聚焦输入框。

对接并调试后端api。

3. 实现流式回复
3.1 改造后端
ChatOpenAI中添加参数：

streaming=True  # 流式输出

model_kwargs={
    "stream_options": {
        "include_usage": True,  # 输出token消耗数量
    }
}
实现event_stream：

def event_stream():
    final_usage = {}
    for msg, metadata in app.stream(inputs, stream_mode="messages"):
        if isinstance(msg, BaseMessageChunk):
            if msg.content:
                yield f"data: {json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n"
            if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                final_usage = msg.usage_metadata
    yield "data: [DONE]\n\n"
    print(final_usage)
定义一个伪渲染器，防止 DRF 报错：

class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]  # 引入渲染器
    def post(self, request):
        ...
返回StreamingHttpResponse：

response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
response['Cache-Control'] = 'no-cache'
return response
3.2 改造前端
安装fetch-event-source：npm install @microsoft/fetch-event-source
将如下代码添加到AIFriends/frontend/src/js/http/streamApi.js。
/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，那么调用api刷新token`，
 * 如果刷新成功，则重新发送原请求。
*/

import { fetchEventSource } from '@microsoft/fetch-event-source';
import { useUserStore } from "@/stores/user.js";
import api from "./api.js";

const BASE_URL = 'http://127.0.0.1:8000'

/**
 * 通用的流式请求工具
 * @param {string} url 请求地址
 * @param {object} options 配置项 (method, body, onmessage, onerror等)
 */
export default async function streamApi(url, options = {}) {
    const userStore = useUserStore();

    const startFetch = async () => {
        return await fetchEventSource(BASE_URL + url, {
            method: options.method || 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.accessToken}`,
                ...options.headers,
            },
            body: JSON.stringify(options.body || {}),

            openWhenHidden: true,  // 允许后台运行，防止浏览器因隐藏页面而强制关闭它
            async onopen(response) {
                // 1. 处理 401 Token 过期
                if (response.status === 401) {
                    try {
                        // 触发 api.js 中的 Axios 拦截器进行静默刷新
                        await api.post('/api/user/account/refresh_token/', {});
                        // 抛出特定错误触发下面的 onerror 重试逻辑
                        throw new Error("TOKEN_REFRESHED");
                    } catch (err) {
                        // 如果刷新失败（refresh_token也过期），直接报错由上层处理
                        throw err;
                    }
                }

                if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `请求失败: ${response.status}`);
                }
            },

            onmessage(msg) {
                if (msg.data === '[DONE]') {
                    if (options.onmessage) options.onmessage('', true);
                    return
                }
                try {
                    const json = JSON.parse(msg.data);
                    if (options.onmessage) options.onmessage(json, false);
                } catch (e) {
                    console.error("流解析失败:", e);
                }
            },

            onerror(err) {
                // 2. 捕获重试信号并递归
                if (err.message === "TOKEN_REFRESHED") {
                    return startFetch();
                }

                // 其他错误则按用户定义的 onerror 处理
                if (options.onerror) {
                    options.onerror(err);
                }
                throw err; // 停止自动重试
            },

            onclose: options.onclose,
        });
    };

    return await startFetch();
}
将HTTP请求修改成SSE请求。
4. 实现聊天记录的创建和加载
4.1 实现后端
大模型回复结束后自动创建Message，记得截断user_message、input、output等信息。

实现AIFriends/backend/web/views/friend/message/get_history.py。

在AIFriends/backend/web/urls.py中添加路由。

4.2 实现前端
在AIfriends/frontend/src/components/character/chat_field/ChatField.vue中定义history，用来存储历史聊天信息。

将输入信息和回复信息更新到history中。

可以用crypto.randomUUID()生成消息的唯一ID。
在AIfriends/frontend/src/components/character/chat_field/chat_history/目录下实现组件：

ChatHistory.vue。
message/Message.vue
聊天气泡要加上whitespace-pre-wrap来保留空格和回车。

隐藏掉聊天记录旁的滚动条：

<style scoped>
/* 隐藏 Chrome, Safari 和 Opera 的滚动条 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 隐藏 IE, Edge 和 Firefox 的滚动条 */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>
聊天记录自动滚动到底部，每次添加完消息后触发：

const scrollRef = useTemplateRef('scroll-ref')

async function scrollToBottom() {
  await nextTick()

  scrollRef.value.scrollTop = scrollRef.value.scrollHeight
}
实现聊天记录的流式加载。

每次加载消息后，要更新滚动区域到顶部的距离。
判断哨兵能否被看到的逻辑要修改，之前是判断是否跟视窗有交集，现在是判断是否跟scrollRef标签有交集：

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}
5. 添加系统提示词和短期记忆（多轮对话）
创建数据库SystemPrompt，用来存储所有agent的系统提示词。
存到数据库中修改更方便。如果写到代码里，每次都要打开编辑器，修改代码后再重启服务，很麻烦。

将参考提示词更新到数据库中：

参考提示词：https://www.acwing.com/file_system/file/content/whole/index/content/14043188/
添加系统提示词。

添加最近的10条对话。

6. 添加function call
定义工具函数，一定要实现函数的文档：

@tool
def get_time():
    """查询当前的精确时间，返回格式为：年-月-日 时:分:秒"""
    return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

tools = [get_time]

llm = ChatOpenAI(
    ...
).bind_tools(tools)

tool_node = ToolNode(tools)
添加工具节点和条件边。

7. 添加长期记忆
系统提示词数据库中添加长期记忆。

创建一个新的agent，每10轮对话更新一遍memory。

聊天的系统提示词里添加长期记忆。

8. 打包代码
删除调试信息。

将前端代码打包到后端。
