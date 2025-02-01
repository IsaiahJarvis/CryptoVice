let selectedCoinA = null;
let selectedCoinB = null;
let selectedCoinC = null;
let USD = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});

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
    document.getElementById(img).src=coin["imageLink"];
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
    priceText = `Current Price of ${selectedCoinA['name']}:`;
    fdvText = `Price of ${selectedCoinA['name']} with ${selectedCoinB['name']}'s fully diluted market cap:`;
    mcText = `Price of ${selectedCoinA['name']} with ${selectedCoinB['name']}'s market cap:`;

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

  // try to get coins from api and populate the dropdown
  try {
    const response = await fetch(url);
    const data = await response.json();
    const submit = document.getElementById("submit_wrapper");
    
    if (!data.results || data.results.length === 0) {
      dropdownMenu.appendChild(submit);
      return;
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
    selectedCoinA = {'name': coinName, 'symbol': coinSymbol, 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'fdv': fdv, 'price': price};
    select(selectedCoinA, "selected_img_1", "symbol_wrapper_1", "mc_wrapper_1", "search_input_1", "selected_box_1", dropdown);
  } else if (dropdown === document.getElementById("my_dropdown_2")) {
    selectedCoinB = {'name': coinName, 'symbol': coinSymbol, 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'fdv': fdv, 'price': price};
    select(selectedCoinB, "selected_img_2", "symbol_wrapper_2", "mc_wrapper_2", "search_input_2", "selected_box_2", dropdown);
  }  else if (dropdown === document.getElementById("my_dropdown_3")) {
    selectedCoinC = {'name': coinName, 'symbol': coinSymbol, 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'fdv': fdv, 'price': price};
    select(selectedCoinC, "selected_img_3", "symbol_wrapper_3", "mc_wrapper_3", "search_input_3", "selected_box_3", dropdown);
  }
  // check if results can be displayed
  displayResult();
}

// show network dropdown
function netDrop(dropdown) {
  document.getElementById(dropdown).classList.toggle("show");
}

// select the network
function selectNetwork(input) {
  document.getElementById('network_box').value = input.innerHTML;
  document.getElementById("network_dropdown").classList.toggle("show");
}

function showSubmit(div) {
  document.getElementById(div).classList.toggle("flex");
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("hide_submit").addEventListener("submit", function(event){
    event.preventDefault();

    let contract = document.getElementById("submit_contract").value;
    let network = document.getElementById("network_box").value;
  
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
  });
});

function getCSRFToken() {
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    return csrfToken;
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
  if (!document.getElementById("network_dropdown").contains(e.target) && !document.getElementById("network_box").contains(e.target)) {
    if (document.getElementById("network_dropdown").classList.contains("show") === true) {
      document.getElementById("network_dropdown").classList.toggle("show");
    }
  }
})

