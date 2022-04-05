window.addEventListener("load", (event) => {
  window.stewards = [];
  window.workstreams = [];

  cachbuster = new Date().getTime();

  Promise.all([
    fetch("static/json/workstreams.json?" + cachbuster).then((value) =>
      value.json()
    ),
    fetch("static/json/stewards_data.json?" + cachbuster).then((value) => value.json()),
  ])
    .then((value) => {
      window.workstreams = value[0];
      window.stewards = value[1].data;
      init();
    })
    .catch((err) => {
      console.log(err);
    });
});

function init() {
  console.log("init...");

  // map search input field to filterCard function
  const search = document.getElementById("search");
  search.addEventListener("input", () => {
    filterStewards();
  });

  const timeVal= document.getElementById("timeVal");
  timeVal.addEventListener("input", () => {
    // data shown based on time value selected
    resetSearch();
    orderStewards();
    draw();
  })

  // map orderby input field to orderStewards function
  const orderby = document.getElementById("orderby");
  orderby.addEventListener("input", () => {
    resetSearch();
    orderStewards();
    draw();
  });

  // map direction input field to orderStewards function
  const direction = document.getElementById("direction");
  direction.addEventListener("input", () => {
    resetSearch();
    orderStewards();
    draw();
  });

  // reorder the stewards array on default order
  orderStewards();
  // add all the stewards to the #grid
  draw();

  // inspect location hash ( URL#search=xxx ) and get the params
  params = getParams();
  if (params.search) {
    // set search input field to params.search
    search.value = params.search.toLowerCase();
    // filter from all steward cards
    filterStewards();
  }
}

// get params from location hash

function getParams() {
  var hash = window.location.hash.substr(1);

  var params = hash.split("&").reduce(function (res, item) {
    var parts = item.split("=");
    res[parts[0]] = decodeURIComponent(parts[1]);
    return res;
  }, {});

  return params;
}

function resetSearch() {
  document.location.hash = "";
  search = document.getElementById("search");
  search.value = "";
}

function filterStewards() {
  search = document.getElementById("search");

  let datatags = document.querySelectorAll("[data-tags]");
  //console.log(datatags)

  searchInput = search.value.toLowerCase();
  datatags.forEach((item) => {
    tags = item.dataset.tags.toLowerCase();
    if (tags.indexOf(searchInput) !== -1) {
      item.style.display = "";
    } else {
      item.style.display = "none";
    }
  });

  document.location.hash = "search=" + encodeURIComponent(searchInput);
}

function orderStewards() {
  timeval = document.getElementById("timeVal").value;
  orderby = document.getElementById("orderby").value;
  direction = document.getElementById("direction").value;
  // console.log(orderby, direction)

  if (orderby == "health") {
    window.stewards.sort((a, b) => (a.health[timeval] < b.health[timeval] ? 1 : -1));
  }

  if (orderby == "weight") {
    window.stewards.sort((a, b) => (a.votingweight < b.votingweight ? 1 : -1));
  }

  if (orderby == "vote_participation") {
    window.stewards.sort((a, b) =>
      a.vote_participation[timeval] < b.vote_participation[timeval] ? 1 : -1
    );
  }

  if (orderby == "forum_activity") {
    window.stewards.sort((a, b) => (a.forum_activity[timeval] < b.forum_activity[timeval] ? 1 : -1));
  }

  // ascending - from low to high
  if (direction == "ascending") {
    window.stewards.reverse();
  }
}

function draw() {
  // console.log(window.stewards)

  timeval = document.getElementById("timeVal").value;
  imgpath = "static/stewards/";
  gitcoinurl = "https://gitcoin.co/";

  grid = document.querySelector("#grid");

  // delete all inner nodes
  grid.innerHTML = "";

  card = document.querySelector("#card");

  // generate all steward cards

  window.stewards.forEach((steward) => {
    clone = document.importNode(card.content, true);

    tally_url =
      "https://www.withtally.com/voter/" +
      steward.address +
      "/governance/gitcoin";
    statement_url =
      "https://gov.gitcoin.co/t/introducing-stewards-governance/41/" +
      steward.statement_post_id;

    clone.querySelector("#name").innerHTML = steward.name;
    clone.querySelector("#image").src = imgpath + steward.profile_image;

    clone.querySelector("#handle_gitcoin").innerHTML = steward.gitcoin_username;
    clone.querySelector("#handle_gitcoin").href =
      gitcoinurl + steward.gitcoin_username;

    clone.querySelector("#steward_since").innerHTML = steward.steward_since;

    clone.querySelector("#workstream_url").href = "TBD";

    clone.querySelector("#votingweight").innerHTML = steward.voting_weight;

    // wrap in if condition for 30d/lifetime
    clone.querySelector("#participation_snapshot").innerHTML =
      steward.vote_participation[timeval];

    clone.querySelector("#delegate_button").href = tally_url;
    clone.querySelector("#votingweight_url").href = tally_url;

    clone.querySelector("#forum_post").innerHTML = steward.forum_activity[timeval];
    clone.querySelector("#forum_uri").href =
      "https://gov.gitcoin.co/u/" + steward.handle_forum;

    clone.querySelector("#statement_button").href = statement_url;
    clone.querySelector("#steward_since_url").href = statement_url;

    clone.querySelector("#health").src =
      "static/images/health_" + steward.health + ".svg";

    clone.querySelector("#health_num").innerHTML = `${steward.health[timeval]}/10`;

    if (steward.workstream) {
      stream = window.workstreams.find((o) => o.id === steward.workstream);
      clone.querySelector("#workstream_name").innerHTML = stream.name;
      clone.querySelector("#workstream_url").href = stream.uri;
      workstream_tag = stream.name;
    } else {
      clone.querySelector("#workstream_none").innerHTML = "-";
      workstream_tag = " ";
    }

    // search tags
    clone.querySelector("#card").dataset.tags =
      steward.address +
      " " +
      steward.name +
      " " +
      steward.gitcoin_username +
      " " +
      steward.discourse_username +
      " " +
      workstream_tag;

    // apply highlights to cards based on orderby
    orderby = document.getElementById("orderby").value;

    if (orderby == "health") {
      clone.querySelector("#health").classList.add("highlight");
    }

    if (orderby == "weight") {
      clone.querySelector("#votingweight").classList.add("highlight");
    }

    if (orderby == "posts") {
      clone.querySelector("#forum_post").classList.add("highlight");
    }

    if (orderby == "participation") {
      clone.querySelector("#participation_snapshot").classList.add("highlight");
    }

    document.querySelector("#grid").appendChild(clone);
  });
}