import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',  // FastAPI 默认端口
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const fetchData = () => {
  return api.get('/api/data')
}

export default api 