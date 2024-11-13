
function dropSearch(input) {
  if (input == 'my_dropdown_1') {
    document.getElementById(input).classList.toggle("show");
    if (document.getElementById('my_dropdown_2').classList.contains("show") === true) {
      document.getElementById('my_dropdown_2').classList.toggle("show");
    }
  } else {
    document.getElementById(input).classList.toggle("show");
    if (document.getElementById('my_dropdown_1').classList.contains("show") === true) {
      document.getElementById('my_dropdown_1').classList.toggle("show");
    }
  }
}

function filterFunction(search, drop) {
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

function coinSelect(event, search) {
  event.preventDefault();
  
  const link = event.currentTarget;
  const coinName = link.getAttribute("data-name");
  const coinSymbol = link.getAttribute("data-symbol");
  const coinImage = link.getAttribute("data-image_link");
  const coinId = link.getAttribute("data-id");
  const marketCap = link.getAttribute("data-market-cap");
  const circSupply = link.getAttribute("data-circ-supply");
  // to be changed
  
  if (search == 'search_input_1') {
    document.getElementById("selected_img_1").src=coinImage;
    document.getElementById("symbol_wrapper_1").innerHTML = coinSymbol;
    document.getElementById("mc_wrapper_1").innerHTML = marketCap;
    document.getElementById(search).classList.toggle("hide");
    document.getElementById("selected_box_1").classList.toggle("show-selected");
    document.getElementById('my_dropdown_1').classList.toggle("show");
  }
  
  if (search == 'search_input_2') {
    document.getElementById("selected_img_2").src=coinImage;
    document.getElementById("symbol_wrapper_2").innerHTML = coinSymbol;
    document.getElementById("mc_wrapper_2").innerHTML = marketCap;
    document.getElementById(search).classList.toggle("hide");
    document.getElementById("selected_box_2").classList.toggle("show-selected");
    document.getElementById('my_dropdown_2').classList.toggle("show");
  }
}

function hideSelected(search, select, dropdown) {
  document.getElementById(search).classList.toggle("hide");
  document.getElementById(search).focus();
  document.getElementById(dropdown).classList.toggle("show");
  document.getElementById(select).classList.toggle("show-selected");
}
