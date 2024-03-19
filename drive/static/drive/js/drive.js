// Parse user email, first name, and last name from DOM elements
const user_email = JSON.parse(document.getElementById("user_email").textContent);
const user_firstn = JSON.parse(document.getElementById("english_name").textContent)? null : '';
const user_lastn = JSON.parse(document.getElementById("arabic_name").textContent)? null : '';



document.addEventListener("DOMContentLoaded", function () {

  history.replaceState({ drivebox: "home" }, "Default state", "#home");

  // Sidebar toggler
  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("side_active");
    $(".main").toggleClass("spread");

    // Show overlay when menu appears on mobile devices
    if ($(window).width() <= 768) {
      $(".overlay").addClass("over_active");
    }
  });

  // Hide overlay when it is clicked
  $(".overlay").on("click", function () {
    // Hide sidebar
    $("#sidebar").removeClass("side_active");
    // Hide overlay
    $(".overlay").removeClass("over_active");
  });


  // Handle window resize event
  window.addEventListener('resize', function(event){
    if ($(window).width() > 768) {
      if($(".main").hasClass("spread")){
        // Add side_active class to sidebar if main has spread class
        $("#sidebar").addClass("side_active");
      }
      document.querySelector('.navbar').style.display = "flex";
    }
    if ($(window).width() <= 768){
      if($("#sidebar").hasClass("side_active")){
        // Add over_active class to overlay if sidebar has side_active class
        $(".overlay").addClass("over_active");
      }
      else{
        // Remove over_active class from overlay if sidebar doesn't have side_active class
        $(".overlay").removeClass("over_active");
      }
    }
  });

  // Active Nav-links style
  $(".nav-link").each(function () {
    var link = this;
    
    link.addEventListener("click", function () {
      let maildiv;
      
      if (document.querySelector("#files-view").style.display !== "none") {
        maildiv = document.querySelector(".mailbox_head").textContent;
        if (maildiv.toLowerCase() !== link.id) {
          // Push state with drivebox id and load drivebox if it's not compose
          history.pushState({ drivebox: link.id }, "", `./#${link.id}`);
          if (link.id !== "compose") load_drivebox(link.id);
        }
      } else {
        // Push state with drivebox id and load drivebox if it's not compose
        history.pushState({ drivebox: link.id }, "", `./#${link.id}`);
        if (link.id !== "compose") load_drivebox(link.id);
      }
    });
  });


  document.querySelector(".srch-form").addEventListener("submit", (e) => {
    let srch_query = document.querySelector(".srch-inp").value;

    if (srch_query.trim().length > 0) {
      // Push state with search query and load drivebox with search query
      history.pushState({ query: srch_query.trim() }, "", `./#search/${srch_query.trim()}`);
      load_drivebox("search", srch_query.trim());
    }
    e.preventDefault();
  });

  // Load the inbox by default
  load_drivebox("home");
});


function load_drivebox(drivebox, query = "") {
  tog_menu(); // Toggle sidebar when on mobile devices

  // If the drivebox is not "search", remove the "active" class from all .nav-link elements
  // and add the "active" class to the element with the ID equal to the drivebox value.
  if(drivebox !== "search"){
    $(".nav-link").each(function () {
      $(this).removeClass("active");
    });
    $(`#${drivebox}`).addClass("active");
  }

  // If the window width is less than or equal to 768 pixels, set the display property of the .navbar element to "flex".
  if($(window).width() <= 768){
    document.querySelector('.navbar').style.display = "flex";
  }


  // Create a spinner HTML element using template literals and assign it to the 'spinner' variable.
  const spinner = `
  <div class="d-flex justify-content-center spin my-5">
    <div class="spinner-border text-danger" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>`;

  // Set the inner HTML of the #files-view element to include a mailbox header (mailbox name capitalized) and the spinner.
  document.querySelector(
    "#files-view"
  ).innerHTML = `<h4 class="mailbox_head py-3 pl-3 m-0 mx-1 mb-3 d-block w-100">${
    drivebox.charAt(0).toUpperCase() + drivebox.slice(1)
  }</h4> ${spinner}`;


  // If the mailbox is "search", modify the mailbox value to include the search query.
  if (drivebox === "search") {
    drivebox = `search/${query}`;
  }


  // Send a fetch request to the server to retrieve emails for the specified mailbox.
  fetch(`/drive/${drivebox}`)
    .then((response) => response.json())
    .then((files) => {
      console.log(files)
      // Remove the "d-flex" class and add the "d-none" class to the spinner element.
      $(".spin").removeClass("d-flex").addClass("d-none");

      // If there is an error property in the response, display an error message in the #files-view element.
      if (files.error) {
        document.querySelector(
          "#files-view"
        ).innerHTML += `<h5 class="pl-3 pt-2">${files.error} for "${query}"</h5>`;
      }

      // If there are files, iterate over each email and create HTML elements to display them.
      else if(files.length > 0){
        files.forEach((file) => {
          const filesView = document.createElement("div");

          filesView.classList.add(
            "col-xl-4",
            "col-lg-6",
          );

          const element = document.createElement("div");

          element.classList.add(
            "file",
            "d-flex",
            "justify-content-between",
            "align-items-center"
          );

          filesView.appendChild(element);

          const element2 = document.createElement("div");

          element2.classList.add(
            "d-flex",
            "align-items-top"
          );

          element.appendChild(element2);

          const imgDiv = document.createElement("div");

          imgDiv.classList.add(
            "mr-3",
            "img"
          );

          element2.appendChild(imgDiv);

          const img = document.createElement("img");

          img.src = '/static/drive/img/png-icon/f1.png';

          imgDiv.appendChild(img);


          const contentDiv = document.createElement("div");

          contentDiv.classList.add(
            "content"
          );

          element2.appendChild(contentDiv);

          const title = document.createElement("p");

          title.classList.add(
            "black",
            "mb-0"
          );

          title.textContent = file.file;

          contentDiv.appendChild(title);

          const fileSize = document.createElement("p");

          fileSize.classList.add(
            "font-13",
            "c4",
            "p-0"
          );

          fileSize.textContent = '5mb',

          contentDiv.appendChild(fileSize);

          document.querySelector("#files-view").append(filesView);


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
        <div class="text-center empty_text">Nothing in ${mailbox}</div>`
        document.querySelector("#emails-view").append(empty);
      }

    });


}











function tog_menu() {
  const targetWidth = 768;

  // Check if the window width is less than or equal to the target width
  if ($(window).width() <= targetWidth) {
    // Remove the 'side_active' class from the sidebar element
    $("#sidebar").removeClass("side_active");

    // Remove the 'spread' class from the '.main' element
    $(".main").removeClass("spread");

    // Remove the 'over_active' class from the '.overlay' element
    $(".overlay").removeClass("over_active");

    // Add your JavaScript code for screens wider than or equal to 768 here
  }
}