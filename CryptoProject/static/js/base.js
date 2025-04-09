let selectedCoinA = null;
let selectedCoinB = null;
let selectedCoinC = null;
let USD = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});
let numFormat = new Intl.NumberFormat('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
let asPercent = (num) => `${numFormat.format(num)}%`;

// changes the dropdown menu and focus to the clicked searchbox
function dropSearch(section, dropdown, input) {
  if (document.getElementById(dropdown).classList.contains("show") === true) {
    if (document.getElementById(section).classList.contains("active") === true) {
      document.getElementById(dropdown).classList.toggle("show");
    }
  } else if (document.getElementById(dropdown).classList.contains("show") === false) {
    document.getElementById(dropdown).classList.toggle("show");
  }
  filterFunction(input, dropdown);
}

// select coin, hide search and show selected box 
function select(coin, img, symbol, MC, search, selectedBox, dropdown) {
    const imageSrc = (coin["imageLink"] && coin["imageLink"] !== "N/A") ? coin["imageLink"] : defaultImage;
    
    document.getElementById(img).src = imageSrc;
    document.getElementById(symbol).innerHTML = coin["symbol"];
    document.getElementById(MC).innerHTML = "$" + String(coin["marketCap"] * 1);
    document.getElementById(search).classList.toggle("hide");
    document.getElementById(selectedBox).classList.toggle("show-selected");
    dropdown.classList.toggle("show");
}

// hide selected box, show search and dropdown and focus search
function hideSelected(search, select, section, dropdown) {
  document.getElementById(search).classList.toggle("hide");
  document.getElementById(search).focus();
  if (document.getElementById(dropdown).classList.contains("show") === false) {
    document.getElementById(dropdown).classList.toggle("show");
  }
  document.getElementById(select).classList.toggle("show-selected");
  // clears the data in the selected box
  clearSelected(section);
}

// clear both selected coins
function clearSelected(dropdown) {
  if (dropdown === "dropdown_1") {
    document.getElementById("selected_img_1").src="";
    document.getElementById("symbol_wrapper_1").innerHTML = "";
    document.getElementById("mc_wrapper_1").innerHTML = "";
  } else if (dropdown === "dropdown_2") {
    document.getElementById("selected_img_2").src="";
    document.getElementById("symbol_wrapper_2").innerHTML = "";
    document.getElementById("mc_wrapper_2").innerHTML = "";
  } else {
    document.getElementById("selected_img_3").src="";
    document.getElementById("symbol_wrapper_3").innerHTML = "";
    document.getElementById("mc_wrapper_3").innerHTML = "";
  }
}

// calculate the results of the tool and display the results section if not already displayed
function displayResult() {
  // only update if both boxes are showing selected isntead of the search box
  if (document.getElementById('selected_box_1').classList.contains("show-selected") === true && (document.getElementById('selected_box_2').classList.contains("show-selected") === true)) {
    fdvPrice = parseFloat(selectedCoinA['price']) * (parseFloat(selectedCoinB['fdv']) / parseFloat(selectedCoinA['fdv']));
    mcPrice = parseFloat(selectedCoinA['price']) * (parseFloat(selectedCoinB['marketCap']) / parseFloat(selectedCoinA['marketCap']));
    priceText = `Current Price of ${selectedCoinA['symbol']}:`;
    fdvText = `Price of ${selectedCoinA['symbol']} with ${selectedCoinB['symbol']}'s fully diluted market cap:`;
    mcText = `Price of ${selectedCoinA['symbol']} with ${selectedCoinB['symbol']}'s market cap:`;

    document.getElementById("price_text").innerHTML = priceText;
    document.getElementById("price_of_a").innerHTML = "$" + String(selectedCoinA['price'] * 1);
    document.getElementById("result_fdv_text").innerHTML = fdvText;
    document.getElementById("result_fdv").innerHTML = "$" + String(fdvPrice * 1);
    document.getElementById("result_mc_text").innerHTML = mcText;
    document.getElementById("result_mc").innerHTML = "$" + String(mcPrice * 1);
    if (document.getElementById("results").classList.contains("show") != true) {
      document.getElementById("results").classList.toggle("show");
    }
  }
}

let isLoading = false;  // To track loading state
let nextPageUrl = null;  // To handle pagination

async function filterFunction(inputElement, dropdown) {
  // display dropdown if not displayed
  if (document.getElementById(dropdown).classList.contains("show") === false) {
    document.getElementById(dropdown).classList.toggle("show");
  }

  // set query and get dropdown dom object
  let query = inputElement.value.trim();  // Get the search query from input
  const dropdownMenu = document.getElementById(dropdown);

  // if not query select top 50
  if (query.length === 0) {
    query = "";
  }
  // Clear previous dropdown results
  if (!document.getElementById("hidden_storage").contains(document.getElementById("submit_wrapper"))) {
    document.getElementById("hidden_storage").appendChild(document.getElementById("submit_wrapper"));
  }  // add function to clear data
  dropdownMenu.innerHTML = "";
  nextPageUrl = null;

  // Fetch initial results from the API
  const initialUrl = `/api/search/?q=${query}`;
  await fetchResults(initialUrl, dropdownMenu);
}

async function fetchResults(url, dropdownMenu) {
  // Prevent multiple simultaneous requests
  if (isLoading) return;
  isLoading = true;
  let excludeCoingecko = false

  if (dropdownMenu === document.getElementById("my_dropdown_3")) {
    excludeCoingecko = true
  } 
  const fullUrl = `${url}&excludeCoingecko=${excludeCoingecko}`
  console.log(fullUrl)
  // try to get coins from api and populate the dropdown
  try {
    const response = await fetch(fullUrl);
    const data = await response.json();
    const submit = document.getElementById("submit_wrapper");
    
    if (dropdownMenu != document.getElementById("my_dropdown_3")) {
      if (!data.results || data.results.length === 0) {
        dropdownMenu.appendChild(submit);
        return;
      }
    }
	  // Populate the dropdown with results
    data.results.forEach((coin) => {
      const item = document.createElement("div");
      item.classList.add("dropdown-item");
      item.setAttribute("data-name", coin.name);
      item.setAttribute("data-symbol", coin.symbol);
      item.setAttribute("data-id", coin.crypto_id);
      item.setAttribute("data-network", coin.network);

      item.innerHTML = `<strong>${coin.name}</strong>`;
      item.onclick = () => coinSelect(coin, dropdownMenu);  // Handle coin selection
      dropdownMenu.appendChild(item);
    });
    // Update next page URL for pagination
    nextPageUrl = data.next;
  } catch (error) {
    console.error("Error fetching search results:", error);
  } finally {
    isLoading = false;
  }
}

function showDropdown(dropdown) {
  document.getElementById(dropdown).classList.toggle("show");
}

// select and save coin
function coinSelect(coin, dropdown) {

  // assign coin variables
  const coinName = coin.name;
  const coinSymbol = coin.symbol;
  const coinImage = coin.image_link;
  const coinId = coin.crypto_id;
  const price = coin.price;
  const marketCap = coin.market_cap;
  const fdv = coin.fdv;
  const circSupply = coin.circulating_supply;

  // save coin to proper list and call select to display on selected box
  if (dropdown === document.getElementById("my_dropdown_1")) {
    selectedCoinA = {'name': coinName, 'symbol': coinSymbol.toUpperCase(), 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'fdv': fdv, 'price': price};
    select(selectedCoinA, "selected_img_1", "symbol_wrapper_1", "mc_wrapper_1", "search_input_1", "selected_box_1", dropdown);
  } else if (dropdown === document.getElementById("my_dropdown_2")) {
    selectedCoinB = {'name': coinName, 'symbol': coinSymbol.toUpperCase(), 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'fdv': fdv, 'price': price};
    select(selectedCoinB, "selected_img_2", "symbol_wrapper_2", "mc_wrapper_2", "search_input_2", "selected_box_2", dropdown);
  }  else if (dropdown === document.getElementById("my_dropdown_3")) {
    const network = coin.network;
    const address = coin.contract_address;
    let uniqueId = address + ":" + network
    console.log(uniqueId);
    
    if (document.getElementById("filter_dropdown").classList.contains("hide")) {
    	document.getElementById("filter_dropdown").classList.toggle("hide")
    }

    selectedCoinC = {'name': coinName, 'symbol': coinSymbol.toUpperCase(), 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap};
    select(selectedCoinC, "selected_img_3", "symbol_wrapper_3", "mc_wrapper_3", "search_input_3", "selected_box_3", dropdown);
    getInfo(uniqueId);
  }
  // check if results can be displayed
  displayResult();
}

function showSubmit(div) {
  document.getElementById(div).classList.toggle("flex");
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("hide_submit").addEventListener("submit", function(event){
    event.preventDefault();

    let symbol = document.getElementById("submit_symbol").value;
    let price = document.getElementById("submit_price").value;
    let FDV = document.getElementById("submit_FDV").value;
    let marketCap = document.getElementById("submit_market_cap").value;
    
    if (document.getElementById("my_dropdown_1").classList.contains("show")) {
      selectedCoinA = {'name': 'N/A', 'symbol': symbol.toUpperCase(), 'imageLink': 'N/A', 'id': 'N/A', 'marketCap': marketCap, 'fdv': FDV, 'price': price};
      select(selectedCoinA, "selected_img_1", "symbol_wrapper_1", "mc_wrapper_1", "search_input_1", "selected_box_1", document.getElementById("my_dropdown_1"));
    } else if (document.getElementById("my_dropdown_2").classList.contains("show")) {
      selectedCoinB = {'name': 'N/A', 'symbol': symbol.toUpperCase(), 'imageLink': 'N/A', 'id': 'N/A', 'marketCap': marketCap, 'fdv': FDV, 'price': price};
      select(selectedCoinB, "selected_img_2", "symbol_wrapper_2", "mc_wrapper_2", "search_input_2", "selected_box_2", document.getElementById("my_dropdown_2"));
    }
    displayResult();
    
/*
    fetch("/call-python/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify({ contract: contract, network: network })  // Send JSON data
    })
    .then(response => response.json())
    .then(data => {
      alert("Response: " + data.message);
      console.log(data.message)
    })
    .catch(error => console.error("Error:", error));
*/  
  });
});

function getCSRFToken() {
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    return csrfToken;
}

function getInfo(uniqueId) {
    let call = "/call-python/"

    fetch(call, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify({ "uniqueId": uniqueId })  // Send JSON data
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("holder_count").innerHTML = ""
      if (data.message != "FOUND") {
	pollTaskStatus(data.task_id);
      } else {
        formatFilters(data.result);
      }
    })
    .catch(error => console.error("Error:", error));
}

function pollTaskStatus(taskId) {
    console.log("polling")
    document.getElementById("loading").style.display = "block";
    fetch(`/check_task_status/${taskId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === "SUCCESS") {
                // Update the page with the result data
		document.getElementById("loading").style.display = "none"; // Hide loader on error
		console.log(JSON.stringify(data.result))
                formatFilters(data.result)
            } else if (data.status === "FAILURE") {
		document.getElementById("loading").style.display = "none"; // Hide loader on error
		document.getElementById("holder_count").innerHTML = "Error retrieving this tokens data from API"
                console.error(data.error);
            } else {
                // Task is still running; check again in 5 seconds
                setTimeout(() => pollTaskStatus(taskId), 1000);
            }
        })
        .catch(error => {
	    console.error("Error checking task status:", error)
	    document.getElementById("loading").style.display = "none";
	});
}

function formatFilters(results) {
  const names = ["filter5m", "filter1", "filter4", "filter12", "filter24"];
  for (var i = 0; i < names.length; i++) {
    const item = document.createElement("div");
    let filter = results[names[i]];
    let metrics = {"Average Buy Order (in $)": numFormat.format(filter["avgBuy"]),
	          "Average Sell Order (in $)": numFormat.format(filter["avgSell"]),
	          "Unique Buyer Ratio": numFormat.format(filter["uBuySell"]),
	          "Buyer Retention Rate": asPercent(filter["retention"]),
	          "Net Buy vs Net Sells": asPercent(filter["nBuySell"]),
	    	  "Buy/Sell Ratio": asPercent(filter["buySellRatio"])};
    item.setAttribute("data-target", names[i]);
    
    for (const [key, value] of Object.entries(metrics)) {
      const metricItem = document.createElement("div");
      metricItem.className = "metric-item";
      metricItem.innerHTML = `${key}: ${value}`;
      item.appendChild(metricItem);
    }

    document.getElementById("holder_count").appendChild(item);
    if (i != 1) {
      item.classList.toggle("hide");
    }
  }
}

function changeFilter(filter) {
  document.getElementById("filter_box").innerHTML = filter.innerHTML;
  document.getElementById("my_dropdown_4").classList.toggle("show");
  var parentDiv = document.getElementById("holder_count");
  for (var i = 0; i < parentDiv.children.length; i++) {
    var child = parentDiv.children[i];
    if (child.dataset.target === filter.dataset.target && filter.classList.contains("hide")) {
      child.classList.toggle("hide");
    } else if (!child.classList.contains("hide")) {
      child.classList.toggle("hide")
    }
  }
}

// event listener for closing each dropdown
document.addEventListener('click', e => {
  if (!document.getElementById("my_dropdown_1").contains(e.target) && !document.getElementById("dropdown_1").contains(e.target)) {
    if (document.getElementById("my_dropdown_1").classList.contains("show") === true) {
      document.getElementById("my_dropdown_1").classList.toggle("show");
    }
  }
})

document.addEventListener('click', e => {
  if (!document.getElementById("my_dropdown_2").contains(e.target) && !document.getElementById("dropdown_2").contains(e.target)) {
    if (document.getElementById("my_dropdown_2").classList.contains("show") === true) {
      document.getElementById("my_dropdown_2").classList.toggle("show");
    }
  }
})

document.addEventListener('click', e => {
  if (!document.getElementById("my_dropdown_3").contains(e.target) && !document.getElementById("dropdown_3").contains(e.target)) {
    if (document.getElementById("my_dropdown_3").classList.contains("show") === true) {
      document.getElementById("my_dropdown_3").classList.toggle("show");
    }
  }
})

document.addEventListener('click', e => {
  if (!document.getElementById("my_dropdown_4").contains(e.target) && !document.getElementById("filter_dropdown").contains(e.target)) {
    if (document.getElementById("my_dropdown_4").classList.contains("show") === true) {
      document.getElementById("my_dropdown_4").classList.toggle("show");
    }
  }
})

