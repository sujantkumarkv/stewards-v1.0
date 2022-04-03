

  window.addEventListener("load", (event) => {
  window.stewards = [];
  window.workstreams = [];

  cachbuster = new Date().getTime();

  Promise.all([
    fetch("static/json/workstreams.json").then((value) =>
      value.json()
    ),
    fetch("static/json/stewards_data.json").then((value) => value.json()),
  ])
    .then((value) => {
      window.workstreams = value[0];
      window.stewards = value[1]["data"];
      init();
    })
    .catch((err) => {
      console.log(err);
    });
});

function checktimeVal() {
  //show data based on time value - 30days or lifetime
  const timeVal= document.getElementById("timeVal");
  timeVal.addEventListener("input", () => {
    // data shown based on time value selected
    return timeVal.value
  })
}



function init() {
  console.log("init...")
  timeVal= checktimeVal()
  // map search input field to filterCard function
  const search = document.getElementById("search");
  search.addEventListener("input", () => {
    filterStewards();
  });

  // map orderby input field to orderStewards function
  const orderby = document.getElementById("orderby");
  orderby.addEventListener("input", () => {
    resetSearch();
    orderStewards(timeVal);
    draw(timeVal);
  });

  // map direction input field to orderStewards function
  const direction = document.getElementById("direction");
  direction.addEventListener("input", () => {
    resetSearch();
    orderStewards(timeVal);
    draw(timeVal);
  });




  // reorder the stewards array on default order
  orderStewards(timeVal);
  // add all the stewards to the #grid
  draw(timeVal);


// get params from location hash

function getParams() {
  var hash = window.location.hash.substring(1);

  var params = hash.split("&").reduce(function (res, item) {
    var parts = item.split("=");
    res[parts[0]] = decodeURIComponent(parts[1]);
    return res;
  }, {});

  return params;
}
  // inspect location hash ( URL#search=xxx ) and get the params
  params = getParams();
  if (params.search) {
    // set search input field to params.search
    search.value = params.search.toLowerCase();
    // filter from all steward cards
    filterStewards();
  }
}

// clear the search bar, resetting the cards basically :)
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

function orderStewards(timeVal) {
  orderby = document.getElementById("orderby").value;
  direction = document.getElementById("direction").value;
  // console.log(orderby, direction)

  if (orderby == "health") {
    window.stewards.sort((a, b) => (a.health[$`timeVal`] < b.health[$`timeVal`] ? 1 : -1));
  }

  if (orderby == "weight") {
    window.stewards.sort((a, b) => (a.votingweight < b.votingweight ? 1 : -1));
  }

  if (orderby == "participation") {
    window.stewards.sort((a, b) =>
      a.voteparticipation[$`timeVal`] < b.voteparticipation[$`timeVal`] ? 1 : -1
    );
  }

  if (orderby == "forum_activity") {
    window.stewards.sort((a, b) => (a.forum_activity[$`timeVal`] < b.forum_activity[$`timeVal`] ? 1 : -1));
  }

  // ascending - from low to high
  if (direction == "ascending") {
    window.stewards.reverse();
  }


}

function draw(timeVal) {
  // console.log(window.stewards)

  imgpath = "static/stewards/";
  gitcoinurl = "https://gitcoin.co/";

  grid = document.querySelector("#grid");

  // delete all inner nodes
  //grid.innerHTML = "";

  card = document.querySelector("#card");

  // generate all steward cards

  window.stewards.forEach((steward) => {
    clone = document.importNode(card.content, true);

    tally_url =
      "https://www.withtally.com/voter/" +
      steward.address +
      "/governance/gitcoin";
    statement_url =
      steward.statement_post;

    clone.querySelector("#name").innerHTML = steward.name;
    clone.querySelector("#image").src = imgpath + steward.profile_image;

    clone.querySelector("#gitcoin_username").innerHTML = steward.gitcoin_username;
    clone.querySelector("#gitcoin_username").href = gitcoinurl + steward.gitcoin_username;

    clone.querySelector("#steward_since").innerHTML = steward.steward_since;

    clone.querySelector("#workstream_url").href = "TBD";

    clone.querySelector("#votingweight").innerHTML = steward.votingweight;

    clone.querySelector("#voteparticipation").innerHTML =
      steward.voteparticipation[$`timeVal`];

    clone.querySelector("#delegate_button").href = tally_url;
    clone.querySelector("#votingweight_url").href = tally_url;

    clone.querySelector("#forum_activity").innerHTML = steward.forum_activity[$`timeVal`];
    clone.querySelector("#forum_uri").href =
      "https://gov.gitcoin.co/u/" + steward.discourse_username;

    clone.querySelector("#statement_button").href = statement_url;
    clone.querySelector("#steward_since_url").href = statement_url;

    clone.querySelector("#health").src =
      "static/images/health_" + steward.health['30d'] + ".svg";

    clone.querySelector("#health_num").innerHTML = `${steward.health['30d']}/10`;

    console.log(steward.health['30d']);

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

    if (orderby == "forum_activity") {
      clone.querySelector("#forum_activity").classList.add("highlight");
    }

    if (orderby == "voteparticipation") {
      clone.querySelector("#voteparticipation").classList.add("highlight");
    }

    document.querySelector("#grid").appendChild(clone);
  });
}
