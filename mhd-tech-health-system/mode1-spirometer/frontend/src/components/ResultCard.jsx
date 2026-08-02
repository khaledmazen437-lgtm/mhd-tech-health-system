export default function ResultCard({ result }) {
  const isCOPD = result.diagnosis === 1

  return (
    <div
      className={`rounded-xl shadow p-6 max-w-md border-2 ${
        isCOPD ? 'bg-red-50 border-red-400' : 'bg-green-50 border-green-400'
      }`}
    >
      <h2 className={`text-2xl font-bold ${isCOPD ? 'text-red-700' : 'text-green-700'}`}>
        {result.diagnosis_label}
      </h2>
      <p className="text-sm text-gray-600 mt-1">
        Model confidence: {(result.confidence * 100).toFixed(1)}%
      </p>
      <p className="text-sm text-gray-600">
        FEV1/FVC ratio: {result.fev1_fvc_ratio.toFixed(2)}
      </p>

      {isCOPD && (
        <p className="text-xs text-gray-500 mt-4 italic">
          This is a decision-support screening result, not a standalone clinical diagnosis.
          Recommend follow-up clinical evaluation.
        </p>
      )}
    </div>
  )
}
