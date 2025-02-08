<template>
    <div class="app-container">
      <!-- 侧边栏 -->
      <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
        <div class="sidebar-header">
          <div class="logo-wrapper">
            <span class="logo-text">Mate<span class="logo-highlight">Gen</span></span>
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
              <h2>我是 MateGen, 很高兴见到你!</h2>
              <p>我可以帮你写代码、读文件、写作各种创意内容，请把你的任务交给我吧~</p>
            </div>
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
                    <button class="tool-btn">
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
                <div class="message-content">
                  {{ message.content }}
                </div>
              </div>
            </div>
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
                    <button class="tool-btn">
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
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, nextTick, onMounted } from 'vue'
  import { marked } from 'marked'
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
  const currentAgent = ref('ChatAutoGen')
  const currentTaskId = ref<string | null>(null)

  const scrollToBottom = async () => {
    await nextTick()
    const container = document.querySelector('.chat-messages')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  }

  const startNewChat = () => {
    messages.value = []
    currentChatIndex.value = 0
  }

  const loadChat = (index: number) => {
    currentChatIndex.value = index
    messages.value = [...chatHistory.value[index].messages]
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

    // 如果是第一条消息，创建新的历史记录
    if (messages.value.length === 1) {
      const newChat: ChatHistory = {
        id: Date.now(),
        title: userQuestion.slice(0, 20) + (userQuestion.length > 20 ? '...' : ''),
        time: new Date(),
        messages: [...messages.value]
      }
      chatHistory.value = [newChat, ...chatHistory.value]
      currentChatIndex.value = 0
    } else {
      // 更新现有对话的消息
      if (chatHistory.value[currentChatIndex.value]) {
        chatHistory.value[currentChatIndex.value].messages = [...messages.value]
      }
    }

    userInput.value = ''

    try {
      messages.value.push({
        role: 'assistant',
        content: ''
      })

      const currentAssistantMessage = messages.value[messages.value.length - 1]

      let apiEndpoint = 'http://localhost:8000/api/chat/stream'
      let requestBody: any = {
        messages: [{
          role: 'user',
          content: userQuestion
        }]
      }

      if (currentAgent.value === 'TwoAgentChat') {
        apiEndpoint = currentTaskId.value 
          ? 'http://localhost:8000/api/execute/follow-up'
          : 'http://localhost:8000/api/execute'
        
        requestBody = {
          prompt: userQuestion,
          taskId: currentTaskId.value
        }
      }

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('无法创建流读取器')
      }

      let buffer = ''
      let markdown = '' // 用于存储执行过程的 Markdown

      const processChunk = async (chunk: string) => {
        try {
          const data = JSON.parse(chunk) as (StreamResponse | ExecutionResponse)
          
          if ('type' in data) {
            const currentAssistantMessage = messages.value[messages.value.length - 1] as ChatMessage
            
            switch (data.type) {
              case 'conclusion':
                currentAssistantMessage.conclusion = data.content
                currentAssistantMessage.content = data.content // 保持兼容性
                await scrollToBottom()
                break
                
              case 'process':
                currentAssistantMessage.process = data.content
                currentAssistantMessage.hasDetails = true
                currentAssistantMessage.showDetails = false
                await scrollToBottom()
                break
                
              case 'files':
                currentAssistantMessage.files = data.content
                currentAssistantMessage.hasDetails = true
                currentAssistantMessage.showDetails = false
                await scrollToBottom()
                break
                
              case 'cost':
                currentAssistantMessage.cost = data.content
                currentAssistantMessage.hasDetails = true
                currentAssistantMessage.showDetails = false
                await scrollToBottom()
                break
            }
          } else {
            // 处理普通聊天接口的响应
            if (!data.done) {
              const currentAssistantMessage = messages.value[messages.value.length - 1]
              await new Promise<void>(resolve => {
                setTimeout(() => {
                  currentAssistantMessage.content += data.content
                  resolve()
                }, 50)
              })
              await scrollToBottom()
            }
          }
        } catch (e) {
          console.error('解析流数据失败:', e)
        }
      }

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const messages = buffer.split('\n\n')
        buffer = messages.pop() || ''

        for (const msg of messages) {
          if (msg.startsWith('data: ')) {
            await processChunk(msg.slice(6))
          }
        }
      }

      if (buffer.startsWith('data: ')) {
        await processChunk(buffer.slice(6))
      }

    } catch (error) {
      console.error('Error:', error)
      messages.value.push({
        role: 'assistant',
        content: '抱歉，发生了一些错误。请稍后再试。'
      })
    }
  }

  const selectAgent = (agent: string) => {
    if (agent === 'TwoAgentChat') {
      messages.value = []
      currentTaskId.value = null
      messages.value.push({
        role: 'assistant',
        content: '已切换到 TwoAgentChat 模式。请描述您的任务，我会协助您完成。'
      })
    }
    currentAgent.value = agent
  }

  const renderMarkdown = (content: string) => {
    return DOMPurify.sanitize(marked(content))
  }

  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value;
  }

  // 初始化
  onMounted(() => {
    startNewChat()
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
  }

  /* 聊天内容区域 */
  .chat-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    height: 100%;
    transition: all 0.3s ease;
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

  .chat-messages {
    flex: 1;
    overflow-y: auto;
  }

  .chat-input {
    width: 100%;
    margin-top: 20px;
    transition: all 0.3s ease;
  }

  .chat-messages + .chat-input {
    margin-top: 20px;
    animation: slideUp 0.3s ease;
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

  /* 消息区域样式 */
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: auto;
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
    font-size: 20px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  
  .logo-highlight {
    color: #4b4bff;
  }
  
  .collapse-btn {
    background: none;
    border: none;
    color: #666;
    padding: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .collapse-btn:hover {
    color: #fff;
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
    background-color: #4b4bff;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    font-size: 14px;
  }
  
  .new-chat-btn:hover {
    background-color: #3a3edf;
    transform: translateY(-1px);
  }

  .new-chat-btn svg {
    transition: transform 0.3s ease;
  }

  .new-chat-btn:hover svg {
    transform: rotate(90deg);
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
  }

  .tool-btn:hover {
    color: #fff;
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

  /* 修改有消息时的输入框样式 */
  .chat-input {
    width: 100%;
    margin-top: auto;
  }

  .chat-input .input-wrapper {
    max-width: 800px;
  }

  /* Markdown 样式优化 */
  :deep(.markdown-body) {
    font-size: 14px;
    line-height: 1.4;
    color: #ffffff;
  }

  :deep(.markdown-body p) {
    margin: 0;
  }

  :deep(.markdown-body ul),
  :deep(.markdown-body ol) {
    margin: 0.2em 0;
    padding-left: 1.2em;
  }

  :deep(.markdown-body li) {
    margin: 0;
    line-height: 1.4;
  }

  :deep(.markdown-body h1),
  :deep(.markdown-body h2),
  :deep(.markdown-body h3),
  :deep(.markdown-body h4),
  :deep(.markdown-body h5),
  :deep(.markdown-body h6) {
    margin: 0.3em 0 0.1em;
    line-height: 1.3;
  }

  :deep(.markdown-body pre) {
    margin: 0.2em 0;
    padding: 0.5em;
    background-color: #363636;
    border-radius: 4px;
    overflow-x: auto;
  }

  :deep(.markdown-body code) {
    background-color: #363636;
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-size: 13px;
  }

  :deep(.markdown-body blockquote) {
    margin: 0.2em 0;
    padding: 0.2em 0.5em;
    border-left: 3px solid #4a4eff;
    background-color: #363636;
    color: #aaa;
  }

  .assistant-response {
    width: 100%;
  }

  .details-section {
    margin-top: 0.5rem;
  }

  .details-btn {
    background-color: transparent;
    border: 1px solid #4a4eff;
    color: #4a4eff;
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s;
  }

  .details-btn:hover {
    background-color: #4a4eff22;
  }

  .details-content {
    margin-top: 0.5rem;
    padding: 0.8rem;
    background-color: #2d2d2d;
    border-radius: 6px;
  }

  .detail-block {
    margin-bottom: 1rem;
  }

  .detail-block:last-child {
    margin-bottom: 0;
  }

  .detail-block h4 {
    margin: 0 0 0.5rem 0;
    color: #888;
  }

  .files-list {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .file-link {
    color: #4a4eff;
    text-decoration: none;
    padding: 0.2rem 0;
  }

  .file-link:hover {
    text-decoration: underline;
  }

  .cost-info {
    font-size: 0.9rem;
  }

  .cost-details {
    margin-top: 0.3rem;
    color: #888;
  }

  /* 添加空状态样式 */
  .empty-state-content {
    background-color: #2d2d2d;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    max-width: 600px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .empty-state-content .input-wrapper {
    margin-top: 1.5rem;
    width: 100%;
  }

  .empty-state-content input {
    flex: 1;
    background: none;
    border: none;
    color: white;
    padding: 0.5rem;
    font-size: 0.9rem;
    outline: none;
  }

  .empty-state-content .action-btn {
    background-color: #4a4eff;
    color: white;
    border: none;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 0.9rem;
  }

  .empty-state-content .action-btn:hover {
    background-color: #3a3edf;
  }

  .empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .empty-state-content h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    color: #ffffff;
  }

  .empty-state-content p {
    margin: 0;
    color: #888;
    font-size: 0.9rem;
    line-height: 1.4;
  }

  /* 展开按钮样式 */
  .expand-btn {
    position: fixed;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    background: #2d2d2d;
    border: none;
    padding: 8px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    color: #666;
    z-index: 100;
    transition: all 0.2s;
  }

  .expand-btn:hover {
    color: #fff;
    background: #3d3d3d;
  }

  /* 添加历史聊天相关样式 */
  .chat-history {
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 20px;
    overflow-y: auto;
  }

  .history-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .history-item {
    padding: 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .history-item:hover {
    background-color: #363636;
  }

  .history-item.active {
    background-color: #363636;
  }

  .history-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .history-title {
    color: #fff;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .history-time {
    color: #666;
    font-size: 12px;
  }
  </style>