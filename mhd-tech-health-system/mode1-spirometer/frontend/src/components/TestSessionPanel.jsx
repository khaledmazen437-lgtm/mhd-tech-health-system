export default function TestSessionPanel({ sessionId, reading }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 max-w-md">
      <h2 className="text-lg font-semibold text-gray-800 mb-2">Waiting for Device Reading</h2>
      <p className="text-sm text-gray-500 mb-4">
        Session: <span className="font-mono">{sessionId}</span>
      </p>

      {!reading ? (
        <div className="flex items-center gap-3 text-gray-600">
          <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full" />
          <span>Ask the patient to blow into the spirometer now…</span>
        </div>
      ) : (
        <div className="space-y-1 text-sm text-gray-700">
          <p>FVC: {reading.fvc.toFixed(1)} mL</p>
          <p>FEV1: {reading.fev1.toFixed(1)} mL</p>
          <p>PEF: {reading.pef.toFixed(1)} mL/s</p>
        </div>
      )}
    </div>
  )
}
