import { useState } from 'react'



const App = () => {
  const [average, setAverage] = useState(0)

  const fetchAverage = () => {
    setAverage(Math.random)
    //tässä triggeröidään azure functio
  }

  return (
    <div>
      <h1>Electricity prices</h1>
      <h3>Fetch market defined electricity price average within specified time period</h3>
      <label>start time </label><input></input><br /> 
      <label>end time </label><input></input><br /> 
      <button onClick={fetchAverage}>fetch average</button>
      <div>
        {average}
      </div>
    </div>
  )
}

export default App