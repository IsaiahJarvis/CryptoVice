
function dropsearch(input) {
  if (input == 'myDropdown1') {
    document.getElementById(input).classList.toggle("show");
    if (document.getElementById('myDropdown2').classList.contains("show") === true) {
      document.getElementById('myDropdown2').classList.toggle("show");
    }
  } else {
    document.getElementById(input).classList.toggle("show");
    if (document.getElementById('myDropdown1').classList.contains("show") === true) {
      document.getElementById('myDropdown1').classList.toggle("show");
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
  document.getElementById(search).value = coinSymbol + " " + marketCap + " " + circSupply;
}
