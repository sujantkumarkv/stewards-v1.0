const fs= require("fs")
fs.readFile("app/static/json/stewards_data.json", 'utf-8', (data) => {
                  console.log(data)
})
