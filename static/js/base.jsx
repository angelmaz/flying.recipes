function TemperatureDiv() {
    const [fahrenheit, setFahrenheit] = React.useState("");
    const [celsius, setCelsius] = React.useState("");
    
    function CtoF(Cvalue) {
        console.log(Cvalue)
        const f_value = ((parseFloat(Cvalue) * 1.8) + 32).toFixed(0);
        if (isNaN(f_value)) {
            setFahrenheit("")
          }
          else {
            setFahrenheit(f_value)
          }
    }
    function FtoC(Fvalue) {
        const c_value = ((parseFloat(Fvalue) - 32) / 1.8).toFixed(0);
        if (isNaN(c_value)) {
            setCelsius("")
          }
          else {
            setCelsius(c_value)
          }
    }
    function handleCtoF(event){
        setCelsius(event.target.value)
        CtoF(event.target.value)    
    }
    function handleFtoC(event){
        setFahrenheit(event.target.value)
        FtoC(event.target.value)
    }
    return (<React.Fragment>Temperature
        <input type="text" id="quick_temperature_c" onChange={(event) => handleCtoF(event)} value={celsius} /> C
        <input type="text" id="quick_temperature_f" onChange={(event) => handleFtoC(event)} value={fahrenheit} /> F
    </React.Fragment>);
}
ReactDOM.render(<TemperatureDiv />, document.querySelector('#temperature'))
