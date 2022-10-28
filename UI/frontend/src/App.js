import React, {Component} from 'react'
import {Form} from 'react-bootstrap';
import {Col} from 'react-bootstrap';
import {Container} from 'react-bootstrap';
import {Row} from 'react-bootstrap';
import {Button} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';

class App extends Component{
  constructor(props){
    super(props);

    this.state = {
      isLoading: false,
      formData:{
        Age:" ",
        Sex:'',
        Chestpain:'',
        RestingBP:"",
        Cholesterol:"",
        FastingBS:'',
        RestingECG:'',
        MaxHR:"",
        ExerciseAngina:'',
        Oldpeak:'',
        ST_slope:''
      },
      result: "",
    };
  }

    handleChange = (Event) =>{
      const value = Event.target.value;
      const name = Event.target.name;
      var formData = this.state.formData;
      formData[name] = value;
      this.setState({
        formData
      });
    }

    handlePredictClick = (Event) => {
      const formData = this.state.formData;
      this.setState({isLoading: true});
      console.log(JSON.stringify(formData))
      fetch("https://heartprediction-app.herokuapp.com/prediction",
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
    }

    handleCancelClick = (Event) => {
      this.setState({result: ""});
    }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return(
      <Container>
        <div>
          <h1 className="title">Heart Disease Predictor</h1>
        </div>
       <div className='content'>
        <Form>
            <Row>
              <Form.Group as={Col}>
                <Form.Label>Age</Form.Label>
                <Form.Control 
                  type="number" 
                  name="Age"
                  value={formData.Age}
                  onChange={this.handleChange} 
                />
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Sex</Form.Label>
                <Form.Control 
                  as="select" 
                  name="Sex"
                  value={formData.Sex}
                  onChange={this.handleChange}>
                  <option>M</option>
                  <option>F</option>
                  </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Chest Pain</Form.Label>
                <Form.Control 
                  as="select" 
                  name="Chestpain"
                  value={formData.Chestpain}
                  onChange={this.handleChange}>
                  <option>ATA</option>
                  <option>NAP</option>
                  <option>ASY</option>
                  <option>TA</option>
                  </Form.Control>
              </Form.Group>
            </Row>
            <Row>
              <Form.Group as={Col}>
                <Form.Label>Resting BP</Form.Label>
                <Form.Control 
                  type="number"
                  value={formData.RestingBP}
                  name="RestingBP"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Cholesterol</Form.Label>
                <Form.Control 
                  type="number"
                  value={formData.Cholesterol}
                  name="Cholesterol"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>FastingBS</Form.Label>
                <Form.Control 
                  as="select"
                  value={formData.FastingBS}
                  name="FastingBS"
                  onChange={this.handleChange}>
                  <option>0</option>
                  <option>1</option>
                </Form.Control>
              </Form.Group>
            </Row>
            <Row>
              <Form.Group as={Col}>
              <Form.Label>RestingECG</Form.Label>
              <Form.Control
                as="Select"
                value={formData.RestingECG}
                name="RestingECG"
                onChange={this.handleChange}>
                  <option>LVH</option>
                  <option>Normal</option>
                  <option>ST</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
              <Form.Label>Max HR</Form.Label>
              <Form.Control
                type="number"
                value={formData.MaxHR}
                name="MaxHR"
                onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
              <Form.Label>Exercise Angina</Form.Label>
              <Form.Control
                as="select"
                value={formData.ExerciseAngina}
                name="ExerciseAngina"
                onChange={this.handleChange}>
                  <option>N</option>
                  <option>Y</option>
                </Form.Control>
              </Form.Group>
            </Row>
            <Row>
              <Form.Group as={Col}>
              <Form.Label>Oldpeak</Form.Label>
              <Form.Control
                type="number"
                value={formData.Oldpeak}
                name="Oldpeak"
                onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
              <Form.Label>ST_slope</Form.Label>
              <Form.Control
                as="select"
                value={formData.ST_slope}
                name="ST_slope"
                onChange={this.handleChange}>
                  <option>Up</option>
                  <option>Down</option>
                  <option>Flat</option>
                </Form.Control>
              </Form.Group>
            </Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Making prediction' : 'Predict' }
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Reset prediction
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
        </div>
      </Container>
    );
  }
}

export default App;
