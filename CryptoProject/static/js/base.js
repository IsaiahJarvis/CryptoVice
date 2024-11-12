
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


