
Promise.all([
    fetch("static/json/workstreams.json?" + cachbuster).then((value) =>
      value.json()
    ),
    fetch("static/json/data.json?" + cachbuster).then((value) => value.json()),
  ])
    .then((value) => {
      window.workstreams = value[0];
      window.stewards = value[1];
      init();
    })
    .catch((err) => {
      console.log(err);
    });
