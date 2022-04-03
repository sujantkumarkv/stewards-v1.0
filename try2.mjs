//const data= require("static/json/stewards_data.json")
import fetch from 'node-fetch';

fetch("/static/json/stewards_data.json")
.then(response => {
   return response.json();
})
.then(data => console.log(data));




