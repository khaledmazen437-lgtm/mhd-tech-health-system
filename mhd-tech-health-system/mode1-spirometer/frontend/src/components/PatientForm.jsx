import { useState } from 'react'

const initialForm = {
  gender: 1,
  age_years: '',
  height_cm: '',
  weight_kg: '',
}

export default function PatientForm({ onStartTest, isStarting }) {
  const [form, setForm] = useState(initialForm)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onStartTest({
      gender: Number(form.gender),
      age_years: Number(form.age_years),
      height_cm: Number(form.height_cm),
      weight_kg: Number(form.weight_kg),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow p-6 space-y-4 max-w-md">
      <h2 className="text-lg font-semibold text-gray-800">Patient Demographics</h2>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">Gender</label>
        <select
          name="gender"
          value={form.gender}
          onChange={handleChange}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value={1}>Male</option>
          <option value={2}>Female</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">Age (years)</label>
        <input
          type="number"
          name="age_years"
          value={form.age_years}
          onChange={handleChange}
          required
          min="0"
          max="120"
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">Height (cm)</label>
        <input
          type="number"
          name="height_cm"
          value={form.height_cm}
          onChange={handleChange}
          required
          min="50"
          max="250"
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">Weight (kg)</label>
        <input
          type="number"
          name="weight_kg"
          value={form.weight_kg}
          onChange={handleChange}
          required
          min="2"
          max="300"
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      <button
        type="submit"
        disabled={isStarting}
        className="w-full bg-blue-600 text-white rounded-lg py-2 font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {isStarting ? 'Starting…' : 'Start Test'}
      </button>
    </form>
  )
}
