from k4 import *
from urllib.parse import quote

autocomplete_paths = []

style = """
<style>
/* Remove default bullets */
ul, #myUL {
  list-style-type: none;
}

/* Remove margins and padding from the parent ul */
#myUL {
  margin: 0;
  padding: 0;
}

/* Style the caret/arrow */
.caret {
  cursor: pointer; 
  user-select: none; /* Prevent text selection */
}

/* Create the caret/arrow with a unicode, and style it */
.caret::before {
  content: "\\25B6";
  color: black;
  display: inline-block;
  margin-right: 6px;
  -ms-transform: rotate(90deg); 
  -webkit-transform: rotate(90deg); 
  transform: rotate(90deg);
}

.caret-down::before {
  -ms-transform: rotate(0deg); 
  -webkit-transform: rotate(0deg); 
  transform: rotate(0deg);  
  ;
}

/* Hide the tree_nested list */
.tree_nested {
  display: block;
}

/* Show the tree_nested list when the user clicks on the caret/arrow (with JavaScript) */
.tree_active {
  display: none;
}
</style>
"""

script = """
<script>
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".tree_nested").classList.toggle("tree_active");
    this.classList.toggle("caret-down");
  });
}


function checkSubmit(e) {
   if(e && e.keyCode == 13) {
      document.forms[0].submit();
   }
}

</script>
"""

button = """
<form action="" autocomplete="off" methond="get">
    <div class="autocomplete" onKeyPress="return checkSubmit(event)"> 
        <input autocomplete="off" 
            style="font-size:14px;" type="text"
            id="files_dir"
            name="files_dir"
            value="FILES_DIR"
            placeholder="path"
        >
        <input hidden readonly type="text" id="city_tab" name="city_tab" value=\"Files\">
        <input type="submit" value="Submit"/>

    </div>
</form>
"""
#<input  type="submit" value="Submit">
autocomplete_script0 = """
<script>
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

/*An array containing all the country names in the world:*/
"""

autocomplete_script1 = """
/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("files_dir"), countries);
</script>
"""

autocomplete_style = """
<style>
* {
  box-sizing: border-box;
}

body {
  font: 16px Arial;  
}

/*the container must be positioned relative:*/
.autocomplete {
  position: relative;
  display: inline-block;
}

input {
  border: 1px solid transparent;
  background-color: #f1f1f1;
  padding: 10px;
  font-size: 16px;
}

input[type=text] {
  background-color: #f1f1f1;
  width: 100%;
}

input[type=submit] {
  background-color: DodgerBlue;
  color: #fff;
  cursor: pointer;
}

.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}

.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff; 
  border-bottom: 1px solid #d4d4d4; 
}

/*when hovering an item:*/
.autocomplete-items div:hover {
  background-color: #e9e9e9; 
}

/*when navigating through the items using the arrow keys:*/
.autocomplete-active {
  background-color: DodgerBlue !important; 
  color: #ffffff; 
}
</style>
"""
def get_tree(p):

    global autocomplete_paths

    p = p.replace(opjh(),'')
    if p[-1] == '/' and len(p) > 1:
        p = p[:-1]

    D = {p:files_to_dict(opjh(p))}

    a = all_values(D)
    
    b = []
    for c in a:
        b.append(pname(c).replace(opjh(),''))
    
    autocomplete_paths = list(set(autocomplete_paths + b))

    script_array = "var countries = ["
    for a in sorted(autocomplete_paths):
        script_array += d2n("\"",a,"\",",)
    script_array = script_array[:-1]+']'

    s = [
        style,
        button.replace('FILES_DIR',p),"<ul id='myUL'>",
        autocomplete_script0 + script_array + autocomplete_script1
    ]

    

    def a(D):
        if type(D) is dict:
            for k in kys(D):
                if '__pycache__' in k:
                    continue
                if k != '__init__.py' and k[0] == '_':
                    continue
                if k != '.':
                    s.append(d2s("<li><span class='caret'>"+fname(k)+"</span>"))
                    s.append(d2s("<ul class='tree_nested'>"))
                    
                a(D[k])
                if k != '.':
                    s.append(d2s('</ul></li>'))
        elif type(D) is list:
            for e in D:
                if False:#exname(e) not in ['js','py','html','txt','c','cpp']:
                    continue
                q = quote(e.replace(opjh(),'/'))
                #cb(q)
                s.append(d2s("<li><a href='"+q+"?city_tab=Files'>",fname(e),"</a></li>"))

    a(D)

    s.append(script)

    return '\n'.join(s)#,D


#EOF
