let selectedCoinA = null;
let selectedCoinB = null;
let USD = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});

function dropSearch(input) {
  console.log("dropSearch");
  if (document.getElementById("my_dropdown").classList.contains("show") === true) {
    if (document.getElementById(input).classList.contains("active") === true) {
      document.getElementById("my_dropdown").classList.toggle("show");
    }
  } else if (document.getElementById("my_dropdown").classList.contains("show") === false) {
    document.getElementById("my_dropdown").classList.toggle("show");
  }

  if (input === "dropdown_1") {
    changeActive("dropdown_1", "dropdown_2");
  } else {
    changeActive("dropdown_2", "dropdown_1");
  }
}

function filterFunction(search, drop) {
  console.log("filter");
  var input, filter, ul, li, a, i;
  input = document.getElementById(search);
  filter = input.value.toUpperCase();
  div = document.getElementById(drop);
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function changeActive(to, from) {
  console.log("changeActive");
  if (document.getElementById(from).classList.contains("active") === true) {
    document.getElementById(from).classList.toggle("active");
    document.getElementById(to).classList.toggle("active");
  } else if (document.getElementById(from).classList.contains("active") === false && document.getElementById(to).classList.contains("active") === false) {
    document.getElementById(to).classList.toggle("active");
  }
  moveDropdown(to);
}

function coinSelect(event) {
  event.preventDefault();
  
  const link = event.currentTarget;
  const coinName = link.getAttribute("data-name");
  const coinSymbol = link.getAttribute("data-symbol");
  const coinImage = link.getAttribute("data-image_link");
  const coinId = link.getAttribute("data-id");
  const marketCap = link.getAttribute("data-market-cap");
  const circSupply = link.getAttribute("data-circ-supply");
  // to be changed
  
  if (document.getElementById("dropdown_1").classList.contains("active") === true) {
    selectedCoinA = {'name': coinName, 'symbol': coinSymbol, 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'circSupply': circSupply};
    select("dropdown_1", selectedCoinA, "selected_img_1", "symbol_wrapper_1", "mc_wrapper_1", "search_input_1", "selected_box_1", "search_input_2", "selected_box_2", "symbol_wrapper_2");
  } else if (document.getElementById("dropdown_2").classList.contains("active") === true) {
    selectedCoinB = {'name': coinName, 'symbol': coinSymbol, 'imageLink': coinImage, 'id': coinId, 'marketCap': marketCap, 'circSupply': circSupply};
    select("dropdown_2", selectedCoinB, "selected_img_2", "symbol_wrapper_2", "mc_wrapper_2", "search_input_2", "selected_box_2", "search_input_1", "selected_box_1", "symbol_wrapper_1");
  }
  displayResult();
}

function select(div, coin, img, symbol, MC, search, selectedBox, swapSearch, swapBox, swapSymbol) {
    console.log("select");
    document.getElementById(img).src=coin["imageLink"];
    document.getElementById(symbol).innerHTML = coin["symbol"];
    document.getElementById(MC).innerHTML = USD.format(coin["marketCap"]);
    document.getElementById(search).classList.toggle("hide");
    document.getElementById(selectedBox).classList.toggle("show-selected");
    document.getElementById("my_dropdown").classList.toggle("show");
    if (document.getElementById(swapSymbol).innerHTML == coin['symbol']) {
      document.getElementById(swapBox).classList.toggle("show-selected");
      document.getElementById(swapSearch).classList.toggle("hide");
      if (div === "dropdown_1") {
	changeActive("dropdown_2", div);
	document.getElementById(search).focus();
        document.getElementById("my_dropdown").classList.toggle("show");
      } else {
	changeActive("dropdown_1", div);
        document.getElementById(search).focus();
        document.getElementById("my_dropdown").classList.toggle("show");
      }
   }
}

function hideSelected(search, select, dropdown) {
  console.log("hideSelected");
  document.getElementById(search).classList.toggle("hide");
  document.getElementById(search).focus();
  if (document.getElementById("my_dropdown").classList.contains("show") === false) {
    document.getElementById("my_dropdown").classList.toggle("show");
  }
  document.getElementById(select).classList.toggle("show-selected");
  clearSelected(dropdown);
  if (dropdown === "dropdown_1") {
    changeActive("dropdown_1", "dropdown_2");
  } else {
    changeActive("dropdown_2", "dropdown_1");
  }
}

function clearSelected(dropdown) {
  if (dropdown === "dropdown_1") {
    document.getElementById("selected_img_1").src="";
    document.getElementById("symbol_wrapper_1").innerHTML = "";
    document.getElementById("mc_wrapper_1").innerHTML = "";
  } else {
    document.getElementById("selected_img_2").src="";
    document.getElementById("symbol_wrapper_2").innerHTML = "";
    document.getElementById("mc_wrapper_2").innerHTML = "";
  }
}

function displayResult() {
  if (document.getElementById('selected_box_1').classList.contains("show-selected") === true && (document.getElementById('selected_box_2').classList.contains("show-selected") === true)) {
    hmc = parseFloat(selectedCoinB['marketCap']) * (parseFloat(selectedCoinB['circSupply']) / parseFloat(selectedCoinA['circSupply']))
    display = `Market Cap of ${selectedCoinA['name']} with ${selectedCoinB['name']}'s market cap:`;
    document.getElementById("result_text").innerHTML = display;
    document.getElementById("result_MC").innerHTML = USD.format(hmc);
  }

  if (document.getElementById("results").classList.contains("show") != true) {
      document.getElementById("results").classList.toggle("show");
  }
}

function moveDropdown(destination) {
    console.log("moveDropdown")
    dropdown = document.getElementById("my_dropdown");
    document.getElementById(destination).appendChild(dropdown);
}
