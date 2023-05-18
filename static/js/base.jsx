// Temperature

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
  function handleCtoF(event) {
    setCelsius(event.target.value)
    CtoF(event.target.value)
  }
  function handleFtoC(event) {
    setFahrenheit(event.target.value)
    FtoC(event.target.value)
  }
  return (<React.Fragment>
    <tr>
      <td className="q-td">
        <input type="number" className="q-input" id="quick_temperature_c" onChange={(event) => handleCtoF(event)} value={celsius} />
      </td>
      <td className="q-td"> C</td>
    </tr>
    <tr>
      <td className="q-td">
        <input type="number" className="q-input" id="quick_temperature_f" onChange={(event) => handleFtoC(event)} value={fahrenheit} />
      </td>
      <td className="q-td"> F</td>
    </tr>
  </React.Fragment>);
}
ReactDOM.render(<TemperatureDiv />, document.querySelector('#temperature'))

// Unit options component

function UnitOptions(props) {
  if (!props.units) {
    return <option>Loading...</option>
  }
  const options = [];
  for (const unit of props.units) {
    options.push(<option value={unit} key={unit}>{unit}</option>)
  }

  return <React.Fragment>
    {options}
  </React.Fragment>
}

// Convert function

function convert(fromQuantity, fromUnit, toUnit, setOutputFn) {
  if (fromQuantity == "") {
    setOutputFn("");
  } else {
    fetch('/quick_convert', {
      method: 'POST',
      body: JSON.stringify({ 'quantity': fromQuantity, 'unit': fromUnit, 'new_unit': toUnit }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        const new_quantity = responseJson['new_quantity'];
        setOutputFn(parseFloat(new_quantity).toFixed(2));
      });
  }
}


// Weight

function QweightDiv() {
  const [fromUnit, setFromUnit] = React.useState("g");
  const [toUnit, setToUnit] = React.useState("g");
  const [fromQuantity, setFromQuantity] = React.useState("");
  const [toQuantity, setToQuantity] = React.useState("");
  const [weightUnits, setWeightUnits] = React.useState(undefined);

  React.useEffect(() => {
    fetch('/get_all_units')
      .then((response) => response.json())
      .then((responseJson) => {
        setWeightUnits(responseJson['weight_units']);
      });
  }, []);

  React.useEffect(() => {
    convert(fromQuantity, fromUnit, toUnit, setToQuantity);
  },
    [fromQuantity, fromUnit, toUnit]);

  return (<React.Fragment>
    <tr>
      <td className="q-td text-end">
        From:
      </td>
      <td className="q-td">
        <input type="number" className="q-input" value={fromQuantity} onChange={(e) => { setFromQuantity(e.target.value); }} />
      </td>
      <td className="q-td">
        <select value={fromUnit} onChange={(e) => { setFromUnit(e.target.value); }}>
          <UnitOptions units={weightUnits} />
        </select>
      </td>
    </tr>
    <tr>
      <td className="q-td text-end">
        To:
      </td>
      <td className="q-td">
        <span>{toQuantity}</span>
      </td>
      <td className="q-td">
        <select value={toUnit} onChange={(e) => { setToUnit(e.target.value); }}>
          <UnitOptions units={weightUnits} />
        </select>
      </td>
    </tr>
  </React.Fragment>);
}

ReactDOM.render(<QweightDiv />, document.querySelector('#Qweight'))

// Volume

function QvolumeDiv() {
  const [fromUnit, setFromUnit] = React.useState("ml");
  const [toUnit, setToUnit] = React.useState("ml");
  const [fromQuantity, setFromQuantity] = React.useState("");
  const [toQuantity, setToQuantity] = React.useState("");
  const [volumeUnits, setVolumeUnits] = React.useState(undefined);

  React.useEffect(() => {
    fetch('/get_all_units')
      .then((response) => response.json())
      .then((responseJson) => {
        setVolumeUnits(responseJson['volume_units']);
      });
  }, []);

  React.useEffect(() => {
    convert(fromQuantity, fromUnit, toUnit, setToQuantity);
  },
    [fromQuantity, fromUnit, toUnit]);

  return (<React.Fragment>
    <tr>
      <td className="q-td text-end">
        From:
      </td>
      <td className="q-td">
        <input type="number" className="q-input" value={fromQuantity} onChange={(e) => { setFromQuantity(e.target.value); }} />
      </td>
      <td className="q-td">
        <select value={fromUnit} onChange={(e) => { setFromUnit(e.target.value); }}>
          <UnitOptions units={volumeUnits} />
        </select>
      </td>
    </tr>
    <tr>
      <td className="q-td text-end">
        To:
      </td>
      <td className="q-td">
        <span>{toQuantity}</span>
      </td>
      <td className="q-td">
        <select value={toUnit} onChange={(e) => { setToUnit(e.target.value); }}>
          <UnitOptions units={volumeUnits} />
        </select>
      </td>
    </tr>
  </React.Fragment>);
}

ReactDOM.render(<QvolumeDiv />, document.querySelector('#Qvolume'))
