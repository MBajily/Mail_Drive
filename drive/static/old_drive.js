// Parse user email, first name, and last name from DOM elements
const user_email = JSON.parse(document.getElementById("user_email").textContent);
const user_firstn = JSON.parse(document.getElementById("first_name").textContent);
const user_lastn = JSON.parse(document.getElementById("last_name").textContent);


const navbar = document.getElementById('sidebar');

// Define an array of categories
const categories = [
  { id: 'home', label: 'Home' },
  { id: 'recent', label: 'Recent' },
  { id: 'archive', label: 'Archived' },
  { id: 'starred', label: 'Starred' },
  { id: 'trash', label: 'Trash' }
];

// Add event listener to navbar items
categories.forEach(category => {
  const categoryItem = document.createElement('li');
  categoryItem.textContent = category.label;
  categoryItem.addEventListener('click', () => {
    fetchFiles(category.id);
  });
  navbar.appendChild(categoryItem);
});

// Function to fetch files from the REST API
function fetchFiles(categoryId) {
  const apiUrl = `http://127.0.0.1:8000/drive/${categoryId}`; // Replace '/drive/#id/' with the actual REST API endpoint
  fetch(apiUrl)
    .then(response => response.json())
    .then((files) => {
      // Remove the "d-flex" class and add the "d-none" class to the spinner element.
      $(".spin").removeClass("d-flex").addClass("d-none");

      // If there is an error property in the response, display an error message in the #emails-view element.
      if (files.error) {
        document.querySelector(
          "#emails-view"
        ).innerHTML += `<h5 class="pl-3 pt-2">${files.error} for "${query}"</h5>`;
      }
      // If there are emails, iterate over each email and create HTML elements to display them.
      else if(files.length > 0){
        files.forEach((file) => {
          console.log(file)
          // Create a div element to reprerecent a single email and assign it to the 'element' variable.
          const element = document.getElementById("drivebox");
          // Set the inner HTML of the 'element' div to contain various information about the email using template literals.
          element.innerHTML = `
            <div class="file d-flex justify-content-between align-items-center">
               <div class="d-flex align-items-center">
                  <div class="img mr-3">
                     <img src="" alt="">
                  </div>
                  <div class="content">
                     <p class="black mb-0">${file.file}</p>
                     <p class="font-13 c4">${file.timestamp}</p>
                  </div>
               </div>

               <div>
                  <!-- Dropdown Button -->
                  <div class="dropdown-button">
                     <a href="#" class="d-flex align-items-center" data-toggle="dropdown">
                        <div class="menu-icon mr-0">
                           <span></span>
                           <span></span>
                           <span></span>
                        </div>
                     </a>
                     <div class="dropdown-menu dropdown-menu-right">
                        <a href="#" class="details">Details</a>
                        <a href="#" class="share">Share</a>
                        <a href="#" class="delete">Delete</a>
                        <a href="#" class="select">Select</a>
                     </div>
                  </div>
                  <!-- End Dropdown Button -->
               </div>
            </div>
          `;

        if(drivebox === "trash"){
          element.querySelector(".del_forever").addEventListener("click", (e)=>{
            fetch(`/drive/${email.id}`, {
              method: "DELETE",
            });
            custm_alert("Conversation deleted forever")
            hide_element(element);
            e.stopImmediatePropagation();
          })
        }
        if ($(window).width() >= 768) {
          element.addEventListener(
            "mouseover",
            () => {
              element.classList.add("shadow", "mail");
              element.querySelector(":scope > div > #time").style.display =
                "none";
              element.querySelector(
                ":scope > div > .btn-list"
              ).style.visibility = "visible";
            },
            false
          );

          element.addEventListener(
            "mouseout",
            () => {
              element.classList.remove("shadow", "mail");
              // $('[data-toggle="tooltip"]').tooltip('hide');
              element.querySelector(
                ":scope > div > .btn-list"
              ).style.visibility = "hidden";
              element.querySelector(":scope > div > #time").style.display =
                "block";
            },
            false
          );
        }
      });
      }
      else{
        const empty = document.createElement("div");
        empty.classList.add(
          // "row",
          "d-flex",
          "flex-column",
          "mt-5",
        );
        empty.innerHTML = `
        <div class="text-center empty_icon"><i class="far fa-folder-open"></i></div>
        <div class="text-center empty_text">Nothing in ${drivebox}</div>`
        document.querySelector("#emails-view").append(empty);
    }
      $('[data-toggle="tooltip"]').tooltip();
    })
    .catch(error => {
      console.error('Error fetching files:', error);
    });
}

