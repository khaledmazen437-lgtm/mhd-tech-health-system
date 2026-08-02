import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

/**
 * Expects `samples`: an array of { volume: number, flow: number } points.
 *
 * TODO: this requires the ESP32 to stream raw time-series samples during
 * the blow (not just the final FVC/FEV1/PEF summary) — see firmware
 * spirometry_calc.cpp, which currently only returns the finalized result.
 * Add a streaming endpoint (WebSocket or repeated POSTs) if you want a
 * real-time curve rather than a static one rendered after the fact.
 */
export default function FlowVolumeGraph({ samples = [] }) {
  if (samples.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-6 max-w-md text-sm text-gray-500">
        No flow-volume data yet — sample streaming not wired up.
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow p-6 max-w-md">
      <h3 className="text-sm font-semibold text-gray-700 mb-2">Flow-Volume Curve</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={samples}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="volume" label={{ value: 'Volume (mL)', position: 'insideBottom', offset: -5 }} />
          <YAxis label={{ value: 'Flow (mL/s)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Line type="monotone" dataKey="flow" stroke="#2563eb" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
