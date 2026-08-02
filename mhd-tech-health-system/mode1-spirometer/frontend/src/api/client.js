import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: BACKEND_URL,
  timeout: 10000,
})

export async function startSession(demographics) {
  const { data } = await client.post('/session/start', demographics)
  return data.session_id
}

export async function pollSession(sessionId) {
  const { data } = await client.get(`/session/${sessionId}`)
  return data
}

export async function predict(patientPayload) {
  const { data } = await client.post('/predict', patientPayload)
  return data
}

export default client
