<template>
    <div class="app-container">
      <!-- 侧边栏 -->
      <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
        <div class="sidebar-header">
          <div class="logo-wrapper">
            <span class="logo-text">My-<span class="logo-highlight">DeepSeek</span></span>
            <button class="collapse-btn" @click="toggleSidebar">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 2L2 8L6 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- 添加历史聊天列表 -->
        <div class="chat-history">
          <button class="new-chat-btn" @click="startNewChat">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 3.33334V12.6667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M12.6667 8L3.33333 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            开启新对话
          </button>
          
          <div class="history-list">
            <div v-for="(chat, index) in chatHistory" 
                 :key="chat.id"
                 :class="['history-item', { active: index === currentChatIndex }]"
                 @click="loadChat(index)">
              <div class="history-content">
                <span class="history-title">{{ chat.title }}</span>
                <span class="history-time">{{ formatTime(chat.time) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部个人信息 -->
        <div class="user-section">
          <button class="user-info">
            <div class="user-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="12" cy="9" r="3" stroke="currentColor" stroke-width="1.5"/>
                <path d="M17.9691 20C17.81 17.1085 16.9247 15 12 15C7.07527 15 6.18997 17.1085 6.03087 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="user-text">个人信息</span>
          </button>
        </div>
      </div>

      <!-- 添加展开按钮 -->
      <button v-if="isSidebarCollapsed" 
              class="expand-btn" 
              @click="toggleSidebar">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 2L14 8L10 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>

      <!-- 主聊天区域 -->
      <div class="chat-container">
        <div class="chat-content">
          <!-- 初始状态：欢迎消息和输入框在一起居中 -->
          <div v-if="!messages.length" class="initial-state">
            <div class="welcome-message">
              <h2>我是 My-DeepSeek, 很高兴见到你!</h2>
              <p>我可以帮你写代码、读文件、写作各种创意内容，请把你的任务交给我吧~</p>
            </div>
            <div class="chat-input">
              <div class="input-wrapper">
                <input
                  v-model="userInput"
                  @keyup.enter="sendMessage"
                  type="text"
                  placeholder="给 My-DeepSeek 发送消息"
                />
                <div class="button-group">
                  <div class="left-buttons">
                    <button 
                      class="tool-btn"
                      :class="{ 'tool-btn-active': isDeepThinking }"
                      @click="toggleDeepThinking"
                    >
                      <div class="icon">🔄</div>
                      深度思考
                    </button>
                    <button class="tool-btn">
                      <div class="icon">🌐</div>
                      联网搜索
                    </button>
                  </div>
                  <div class="right-buttons">
                    <button class="tool-btn">
                      <div class="icon">📎</div>
                    </button>
                    <button 
                      class="send-btn" 
                      :class="{ 'send-btn-active': userInput.trim() }" 
                      :disabled="!userInput.trim()"
                      @click="sendMessage"
                    >
                      <div class="icon">
                        <svg width="14" height="16" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd" clip-rule="evenodd" d="M7 16c-.595 0-1.077-.462-1.077-1.032V1.032C5.923.462 6.405 0 7 0s1.077.462 1.077 1.032v13.936C8.077 15.538 7.595 16 7 16z" fill="currentColor"/>
                          <path fill-rule="evenodd" clip-rule="evenodd" d="M.315 7.44a1.002 1.002 0 0 1 0-1.46L6.238.302a1.11 1.11 0 0 1 1.523 0c.421.403.421 1.057 0 1.46L1.838 7.44a1.11 1.11 0 0 1-1.523 0z" fill="currentColor"/>
                          <path fill-rule="evenodd" clip-rule="evenodd" d="M13.685 7.44a1.11 1.11 0 0 1-1.523 0L6.238 1.762a1.002 1.002 0 0 1 0-1.46 1.11 1.11 0 0 1 1.523 0l5.924 5.678c.42.403.42 1.056 0 1.46z" fill="currentColor"/>
                        </svg>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 对话状态：消息列表在上，输入框在底部 -->
          <div v-else class="chat-state">
            <div class="chat-messages">
              <div v-for="(message, index) in messages" 
                   :key="index"
                   :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
                <div class="message-avatar">
                  <!-- 用户头像 -->
                  <svg v-if="message.role === 'user'" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
                    <circle cx="12" cy="9" r="3" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M17.9691 20C17.81 17.1085 16.9247 15 12 15C7.07527 15 6.18997 17.1085 6.03087 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <!-- AI头像 -->
                  <svg v-else width="24" height="24" viewBox="0 0 24 24">
                    <path d="M12 2L20 7V17L12 22L4 17V7L12 2Z" fill="#4b4bff" opacity="0.2"/>
                    <path d="M12 2L20 7V17L12 22L4 17V7L12 2Z" stroke="#4b4bff" stroke-width="1.5"/>
                    <circle cx="12" cy="12" r="3" fill="#4b4bff" opacity="0.2" stroke="#4b4bff" stroke-width="1.5"/>
                  </svg>
                </div>
                <div class="message-content" v-html="renderMarkdown(message.content)"></div>
              </div>
            </div>
            <div class="chat-input-container">
              <div class="chat-input">
                <div class="input-wrapper">
                  <input
                    v-model="userInput"
                    @keyup.enter="sendMessage"
                    type="text"
                    placeholder="给 MateGen 发送消息"
                  />
                  <div class="button-group">
                    <div class="left-buttons">
                      <button 
                        class="tool-btn"
                        :class="{ 'tool-btn-active': isDeepThinking }"
                        @click="toggleDeepThinking"
                      >
                        <div class="icon">🔄</div>
                        深度思考
                      </button>
                      <button class="tool-btn">
                        <div class="icon">🌐</div>
                        联网搜索
                      </button>
                    </div>
                    <div class="right-buttons">
                      <button class="tool-btn">
                        <div class="icon">📎</div>
                      </button>
                      <button 
                        class="send-btn" 
                        :class="{ 'send-btn-active': userInput.trim() }" 
                        :disabled="!userInput.trim()"
                        @click="sendMessage"
                      >
                        <div class="icon">
                          <svg width="14" height="16" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M7 16c-.595 0-1.077-.462-1.077-1.032V1.032C5.923.462 6.405 0 7 0s1.077.462 1.077 1.032v13.936C8.077 15.538 7.595 16 7 16z" fill="currentColor"/>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M.315 7.44a1.002 1.002 0 0 1 0-1.46L6.238.302a1.11 1.11 0 0 1 1.523 0c.421.403.421 1.057 0 1.46L1.838 7.44a1.11 1.11 0 0 1-1.523 0z" fill="currentColor"/>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.685 7.44a1.11 1.11 0 0 1-1.523 0L6.238 1.762a1.002 1.002 0 0 1 0-1.46 1.11 1.11 0 0 1 1.523 0l5.924 5.678c.42.403.42 1.056 0 1.46z" fill="currentColor"/>
                          </svg>
                        </div>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="disclaimer-text">内容由 AI 生成，请仔细甄别</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
  import { marked, Renderer } from 'marked'
  import DOMPurify from 'dompurify'

  interface StreamResponse {
    content: string
    done: boolean
  }

  interface ExecutionResponse {
    type: 'conclusion' | 'process' | 'files' | 'cost' | 'error' | 'done'
    content: any
  }

  interface ExecutionRequest {
    prompt: string
    taskId?: string
  }

  interface ChatRequest {
    messages: {
      role: string
      content: string
    }[]
  }

  interface ChatMessage {
    role: string
    content: string
    conclusion?: string
    process?: string
    files?: {
      files: string[]
      urls: string[]
    }
    cost?: {
      total: number
      details: Record<string, number>
    }
    hasDetails?: boolean
    showDetails?: boolean
  }

  interface ChatHistory {
    id: number
    title: string
    time: Date
    messages: ChatMessage[]
  }

  const userInput = ref('')
  const messages = ref<ChatMessage[]>([])
  const isSidebarCollapsed = ref(false)
  const chatHistory = ref<ChatHistory[]>([])
  const currentChatIndex = ref(0)
  const currentAgent = ref('openai')
  const currentResponse = ref('')
  const ws = ref<WebSocket | null>(null)
  const isDeepThinking = ref(false)
  const thinkStartTime = ref<number | null>(null)

  const scrollToBottom = async () => {
    await nextTick()
    const container = document.querySelector('.chat-content')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  }

  const startNewChat = () => {
    messages.value = []
    currentChatIndex.value = 0
    scrollToBottom()
  }

  const loadChat = (index: number) => {
    currentChatIndex.value = index
    messages.value = [...chatHistory.value[index].messages]
    scrollToBottom()
  }

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('zh-CN', {
      month: 'numeric',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric'
    }).format(date)
  }

  const sendMessage = async () => {
    if (!userInput.value.trim()) return
    const userQuestion = userInput.value

    // 添加用户消息
    const newMessage: ChatMessage = {
      role: 'user',
      content: userQuestion
    }
    messages.value.push(newMessage)

    // 处理历史记录
    if (messages.value.length === 1) {
      const newChat: ChatHistory = {
        id: Date.now(),
        title: userQuestion.slice(0, 20) + (userQuestion.length > 20 ? '...' : ''),
        time: new Date(),
        messages: [...messages.value]
      }
      chatHistory.value = [newChat, ...chatHistory.value]
      currentChatIndex.value = 0
    }

    userInput.value = ''

    // 添加 AI 回复消息
    messages.value.push({
      role: 'assistant',
      content: ''
    })

    try {
      const endpoint = isDeepThinking.value ? '/reason' : '/chat'
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [{
            role: 'user',
            content: userQuestion
          }]
        })
      })

      if (!response.ok) throw new Error('请求失败')

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) throw new Error('无法创建流读取器')

      let currentContent = ''
      let isInThinkBlock = false
      let isInListItem = false
      let currentListItem = ''
      let currentListItemContent = ''
      let isInOrderedList = false

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          
          const content = line.slice(6).trim()
          if (!content) continue
          
          // 处理思考块
          if (content === '<think>') {
            isInThinkBlock = true
            thinkStartTime.value = Date.now()
            currentContent += '\n\n> 💭 **思考过程：** *(思考中...)*\n> '
            continue
          }
          if (content === '</think>') {
            isInThinkBlock = false
            const thinkTime = thinkStartTime.value ? ((Date.now() - thinkStartTime.value) / 1000).toFixed(1) : '0.0'
            currentContent = currentContent.replace('*(思考中...)*', `*(${thinkTime}s)*`)
            currentContent += '\n\n'
            thinkStartTime.value = null
            continue
          }

          // 收集内容
          if (isInThinkBlock) {
            currentContent += content
          } else {
            // 处理非思考块内容
            if (content.match(/^\d+\.$/)) {
              // 新的有序列表项开始
              if (isInListItem) {
                // 如果之前有未完成的列表项，先添加它
                currentContent += currentListItem + '\n    ' + currentListItemContent + '\n\n'
              }
              isInListItem = true
              isInOrderedList = true
              currentListItem = content + ' '
              currentListItemContent = ''
            } else if (content.match(/^###/)) {
              // 标题
              if (isInListItem) {
                // 如果有未完成的列表项，先添加它
                currentContent += currentListItem + '\n    ' + currentListItemContent + '\n\n'
                isInListItem = false
                isInOrderedList = false
              }
              if (!currentContent.endsWith('\n\n')) {
                currentContent += '\n\n'
              }
              currentContent += content + '\n'
            } else if (content.match(/^-/)) {
              // 无序列表项
              if (isInListItem) {
                // 如果有未完成的列表项，先添加它
                currentContent += currentListItem + '\n    ' + currentListItemContent + '\n\n'
                isInListItem = false
                isInOrderedList = false
              }
              if (!currentContent.endsWith('\n')) {
                currentContent += '\n'
              }
              currentContent += content + ' '
            } else if (isInListItem) {
              // 列表项内容
              if (content === '：') {
                // 遇到冒号，继续收集内容
                currentListItem += content
              } else {
                // 收集列表项内容
                currentListItemContent += content
                
                // 如果内容以句号结尾，自动结束当前列表项
                if (content.match(/[。.!?！？]$/)) {
                  currentContent += currentListItem + '\n    ' + currentListItemContent + '\n\n'
                  isInListItem = false
                  isInOrderedList = false
                  currentListItem = ''
                  currentListItemContent = ''
                }
              }
            } else {
              // 普通文本
              currentContent += content
            }
          }

          // 更新消息内容
          const currentMessage = messages.value[messages.value.length - 1]
          currentMessage.content = currentContent
          await scrollToBottom()
        }
      }

      // 处理最后一个未完成的列表项（如果有）
      if (isInListItem) {
        currentContent += currentListItem + '\n    ' + currentListItemContent + '\n'
      }

      // 更新历史记录
      if (chatHistory.value[currentChatIndex.value]) {
        chatHistory.value[currentChatIndex.value].messages = [...messages.value]
      }

    } catch (error: any) {
      console.error('Error:', error)
      const currentMessage = messages.value[messages.value.length - 1]
      currentMessage.content = `错误：${error.message}`
    }
  }

  const selectAgent = (agent: string) => {
    if (agent === 'TwoAgentChat') {
      messages.value = []
      messages.value.push({
        role: 'assistant',
        content: '已切换到 TwoAgentChat 模式。请描述您的任务，我会协助您完成。'
      })
    }
    currentAgent.value = agent
  }

  const renderMarkdown = (content: string) => {
    if (!content) return ''
    
    try {
      marked.setOptions({
        gfm: true,
        breaks: true
      })

      // 使用 marked.parse 而不是 marked
      const html = marked.parse(content)
      return DOMPurify.sanitize(html)
    } catch (e) {
      console.error('Markdown parsing error:', e)
      return content
    }
  }

  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value;
  }

  const toggleDeepThinking = () => {
    isDeepThinking.value = !isDeepThinking.value
  }

  // 监听消息变化
  watch(messages, () => {
    scrollToBottom()
  }, { deep: true })

  // 初始化
  onMounted(() => {
    startNewChat()
    // 监听窗口大小变化
    window.addEventListener('resize', scrollToBottom)
  })

  // 组件卸载时关闭连接
  onUnmounted(() => {
    ws.value?.close()
    window.removeEventListener('resize', scrollToBottom)
  })
  </script>
  
  <style>
  /* 添加全局样式 */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
  </style>

  <style scoped>
  /* 根容器 */
  .app-container {
    display: flex;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background-color: #1e1e1e;
  }

  /* 左侧栏 */
  .sidebar {
    width: 260px;
    height: 100vh;
    background-color: #2d2d2d;
    border-right: 1px solid #333;
    display: flex;
    flex-direction: column;
    transition: width 0.3s ease;
  }

  .sidebar-collapsed {
    width: 0;
  }

  /* 右侧聊天区域 */
  .chat-container {
    flex: 1;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #1e1e1e;
    overflow: hidden;
  }

  /* 聊天内容区域 */
  .chat-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    transition: all 0.3s ease;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #4a4a4a #1e1e1e;
  }

  .chat-content::-webkit-scrollbar {
    width: 8px;
  }

  .chat-content::-webkit-scrollbar-track {
    background: #1e1e1e;
  }

  .chat-content::-webkit-scrollbar-thumb {
    background-color: #4a4a4a;
    border-radius: 4px;
    border: 2px solid #1e1e1e;
  }

  .chat-content::-webkit-scrollbar-thumb:hover {
    background-color: #666;
  }

  /* 初始状态样式 */
  .initial-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    margin: auto;
    width: 100%;
    max-width: 600px;
    opacity: 1;
    transform: translateY(0);
    transition: all 0.3s ease;
  }

  /* 对话状态样式 */
  .chat-state {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    height: 100%;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* 消息区域样式 */
  .chat-messages {
    flex: 1;
    overflow-y: visible;
    margin-bottom: 20px;
  }

  .chat-input-container {
    width: 100%;
    margin-top: auto;
    padding-bottom: 16px;
  }

  .chat-input {
    width: 100%;
    margin-bottom: 8px;
    transition: all 0.3s ease;
  }

  .chat-input .input-wrapper {
    max-width: 800px;
  }

  .disclaimer-text {
    text-align: center;
    color: #666;
    font-size: 12px;
    padding: 4px 0;
  }

  /* 聊天框样式 */
  .center-chat-box {
    display: flex;
    flex-direction: column;
    gap: 40px;
    width: 100%;
    max-width: 600px;
  }

  /* 欢迎消息样式 */
  .welcome-message {
    text-align: center;
  }

  .welcome-message h2 {
    color: #fff;
    font-size: 24px;
    margin: 0;
    font-weight: normal;
  }

  .welcome-message p {
    color: #666;
    font-size: 13px;
    margin: 0;
    margin-top: 2px;
  }

  /* 消息样式 */
  .message {
    padding: 12px 20px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    width: 100%;
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* 用户消息样式 */
  .user-message {
    background-color: #1e1e1e;
    flex-direction: row-reverse;
  }

  /* AI消息样式 */
  .assistant-message {
    background: none;
  }

  /* 头像样式 */
  .message-avatar {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
  }

  .user-message .message-avatar {
    color: #666;
  }

  /* 消息内容样式 */
  .message-content {
    font-size: 14px;
    line-height: 1.6;
    color: #fff;
  }

  /* 底部个人信息样式 */
  .user-section {
    margin-top: auto;
    padding: 12px;
    border-top: 1px solid #333;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    padding: 8px 12px;
    background: none;
    border: none;
    border-radius: 6px;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .user-info:hover {
    background-color: #363636;
  }

  .user-avatar {
    width: 24px;
    height: 24px;
    color: #888;
  }

  .user-text {
    font-size: 14px;
    color: #fff;
  }

  /* 侧边栏样式 */
  .sidebar-header {
    padding: 16px;
    border-bottom: 1px solid #333;
  }
  
  .logo-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
  }
  
  .logo-text {
    color: #fff;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.5px;
    background: linear-gradient(90deg, #fff 0%, #e0e0e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .logo-highlight {
    background: linear-gradient(90deg, #4b4bff 0%, #6b6bff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
  }
  
  .collapse-btn {
    background: none;
    border: none;
    color: #666;
    padding: 8px;
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .collapse-btn:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.1);
  }
  
  .agents-list {
    padding: 1rem 0;
    overflow-y: auto;
  }
  
  .agent-item {
    display: flex;
    align-items: center;
    padding: 0.8rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    gap: 0.8rem;
  }
  
  .agent-item:hover {
    background-color: #363636;
  }

  .agent-item.active {
    background-color: #4a4eff33;
  }

  .agent-icon {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
  }
  
  .agent-name {
    font-size: 0.9rem;
    color: #fff;
  }
  
  .new-chat-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin: 0 16px;
    padding: 8px 12px;
    font-size: 13px;
    color: #fff;
    background-color: #4b4bff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .new-chat-btn:hover {
    background-color: #3a3aff;
  }

  .new-chat-btn svg {
    width: 14px;
    height: 14px;
    color: #fff;
    opacity: 1;
  }

  /* 输入框容器样式 */
  .input-wrapper {
    width: 100%;
    background-color: #2d2d2d;
    border-radius: 25px;
    padding: 12px 16px;
  }

  input {
    width: 100%;
    background: none;
    border: none;
    color: #fff;
    font-size: 14px;
    outline: none;
    padding: 8px 0;
    margin-bottom: 4px;
  }

  input::placeholder {
    color: #666;
  }

  /* 按钮组样式 */
  .button-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }

  .left-buttons, .right-buttons {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .tool-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: none;
    border: none;
    color: #888;
    padding: 4px 8px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 4px;
  }

  .tool-btn:hover {
    color: #fff;
    background: rgba(75, 75, 255, 0.1);
  }

  .tool-btn-active {
    color: #4b4bff !important;
    background: rgba(75, 75, 255, 0.1);
  }

  .tool-btn-active:hover {
    background: rgba(75, 75, 255, 0.2);
  }

  .send-btn {
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    color: #666;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }

  .send-btn:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  .send-btn-active {
    color: #4b4bff;
  }

  .send-btn-active:hover {
    color: #3a3aff;
  }

  .send-btn .icon {
    width: 16px;
    height: 16px;
  }

  /* 空状态样式调整 */
  .empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 1rem;
  }

  .empty-state-content {
    background: none;
    padding: 0;
    box-shadow: none;
    width: 100%;
    max-width: 600px;
  }

  .empty-state-content h3 {
    color: #fff;
    font-size: 1rem;
    margin-bottom: 0.3rem;
  }

  .empty-state-content p {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .empty-state-content .input-wrapper {
    margin-top: 0;
  }

  /* 工具提示样式 */
  .tool-btn .tooltip {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #4a4a4a;
    color: #fff;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.2s;
    margin-bottom: 0.5rem;
    pointer-events: none;
  }

  .tool-btn:hover .tooltip {
    opacity: 1;
    visibility: visible;
  }

  .tool-btn .tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 4px;
    border-style: solid;
    border-color: #4a4a4a transparent transparent transparent;
  }

  /* 修改空状态下的输入框样式 */
  .empty-state-content .input-wrapper {
    margin-top: 1.5rem;
    width: 100%;
  }

  /* 修改历史聊天列表样式 */
  .chat-history {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .history-list {
    margin-top: 16px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .history-item {
    padding: 12px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    background-color: transparent;
    border-radius: 0;
  }

  .history-item:hover {
    background-color: #2d2d2d;
  }

  .history-item.active {
    background-color: #343541;
    border-left: none;
  }

  .history-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .history-title {
    color: #ececf1;
    font-size: 13px;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .history-time {
    color: #666;
    font-size: 12px;
  }

  /* Markdown 样式优化 */
  :deep(.message-content) {
    color: #fff;
    font-size: 14px;
    line-height: 1.6;

    h1, h2, h3, h4, h5, h6 {
      color: #fff;
      margin: 1em 0;
    }

    p {
      color: #fff;
      margin: 0.5em 0;
    }

    ul, ol {
      color: #fff;
      margin: 0.5em 0;
      padding-left: 2em;
    }

    li {
      margin: 0.25em 0;
    }

    blockquote {
      margin: 1em 0;
      padding: 1em;
      background: rgba(51, 51, 51, 0.6);
      border-left: 4px solid #4b4bff;
      border-radius: 4px;
      color: #666;
    }

    blockquote strong {
      color: #4b4bff;
    }
  }

  /* 修改展开按钮样式 */
  .expand-btn {
    position: fixed;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #666;
    padding: 8px;
    cursor: pointer;
    transition: all 0.2s;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .expand-btn:hover {
    color: #fff;
  }
  </style>