import { useState } from 'react'

const App = () => {
  const [average, setAverage] = useState('')
  const [startDate, setStart] = useState(new Date(new Date().setDate(new Date().getDate()-1)).toISOString().split('T')[0])
  const [endDate, setEnd] = useState(new Date().toISOString().split('T')[0])
  const [startTime, setStartTime] = useState(new Date(new Date().setDate(new Date().getDate()-1)).toLocaleTimeString([], {hour: '2-digit'}))
  const [endTime, setEndTime] = useState(new Date().toLocaleTimeString([], {hour: '2-digit'}))

  const fetchAverage = async () => {
      setAverage('fetching')
      fetch(`https://electricity-prices-2612.azurewebsites.net/api/httptrigger1?START_TIME=${startDate}-${startTime}&END_TIME=${endDate}-${endTime}`)
      .then(async response => {
        const res = await response.text()
        setAverage(!res ? 'something went wrong fetching average price, check console for more info' : res)
      })
  }

  const handleStartDayChange = (event) => {
    setStart(event.target.value)
  }

  const handleStartTimeChange = (event) => {
    setStartTime(event.target.value)
  }

  const handleEndDayChange = (event) => {
    setEnd(event.target.value)
  }

  const handleEndTimeChange = (event) => {
    setEndTime(event.target.value)
  }

  return (
    <div>
      <h1>Electricity prices</h1>
      <h3>Fetch market defined electricity price average within specified time period</h3>
      <label>start date </label><input value={startDate} onChange={handleStartDayChange}></input>
      <label> start time </label><input value={startTime} onChange={handleStartTimeChange}></input><br /><br />
      <label>end date </label><input value={endDate} onChange={handleEndDayChange}></input>
      <label> end time </label><input value={endTime} onChange={handleEndTimeChange}></input><br /><br />
      <button onClick={fetchAverage}>fetch average</button><br />
      <p>{average}</p>
    </div>
  )
}

export default App