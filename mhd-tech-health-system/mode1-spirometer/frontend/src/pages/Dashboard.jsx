import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { startSession, pollSession, predict } from '../api/client'
import PatientForm from '../components/PatientForm'
import TestSessionPanel from '../components/TestSessionPanel'
import ResultCard from '../components/ResultCard'

const STAGES = {
  FORM: 'form',
  WAITING_FOR_DEVICE: 'waiting_for_device',
  RESULT: 'result',
}

export default function Dashboard() {
  const [stage, setStage] = useState(STAGES.FORM)
  const [sessionId, setSessionId] = useState(null)
  const [demographics, setDemographics] = useState(null)
  const [result, setResult] = useState(null)

  const startMutation = useMutation({
    mutationFn: startSession,
    onSuccess: (id, variables) => {
      setSessionId(id)
      setDemographics(variables)
      setStage(STAGES.WAITING_FOR_DEVICE)
    },
  })

  // Poll every 2s once we're waiting on the ESP32 reading
  const { data: sessionData } = useQuery({
    queryKey: ['session', sessionId],
    queryFn: () => pollSession(sessionId),
    enabled: stage === STAGES.WAITING_FOR_DEVICE && !!sessionId,
    refetchInterval: 2000,
  })

  const predictMutation = useMutation({
    mutationFn: predict,
    onSuccess: (data) => {
      setResult(data)
      setStage(STAGES.RESULT)
    },
  })

  // Once the device reading arrives, trigger prediction automatically
  if (sessionData?.ready && stage === STAGES.WAITING_FOR_DEVICE && !predictMutation.isPending) {
    predictMutation.mutate({
      ...demographics,
      fvc: sessionData.reading.fvc,
      fev1: sessionData.reading.fev1,
      pef: sessionData.reading.pef,
    })
  }

  const handleReset = () => {
    setStage(STAGES.FORM)
    setSessionId(null)
    setDemographics(null)
    setResult(null)
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">MHD Tech — Smart Spirometer</h1>

      {stage === STAGES.FORM && (
        <PatientForm onStartTest={startMutation.mutate} isStarting={startMutation.isPending} />
      )}

      {stage === STAGES.WAITING_FOR_DEVICE && (
        <TestSessionPanel sessionId={sessionId} reading={sessionData?.reading} />
      )}

      {stage === STAGES.RESULT && result && (
        <div className="space-y-4">
          <ResultCard result={result} />
          <button
            onClick={handleReset}
            className="text-sm text-blue-600 underline"
          >
            Start new test
          </button>
        </div>
      )}
    </div>
  )
}
