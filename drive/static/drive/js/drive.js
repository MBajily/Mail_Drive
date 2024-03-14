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
  const apiUrl = `/drive/${categoryId}/`; // Replace '/drive/#id/' with the actual REST API endpoint
  fetch(apiUrl)
    .then(response => response.json())
    .then(files => {
      displayFiles(files);
    })
    .catch(error => {
      console.error('Error fetching files:', error);
    });
}

// Function to display the files as a list
function displayFiles(files) {
  const fileList = document.getElementById('drivebox'); // Replace 'file-list' with the actual ID of your file list element

  // Clear the previous list
  fileList.innerHTML = '';

  // Create a list item for each file
  files.forEach(file => {
    const listItem = document.createElement('div');
    listItem.classList.add('col-xl-4', 'col-lg-6');
    listItem.innerHTML = `
      <div class="file d-flex justify-content-between align-items-center">
         <div class="d-flex align-items-center">
            <div class="img mr-3">
               <img src="{% static 'drive/img/png-icon/f1.png' %}" alt="">
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
    fileList.appendChild(listItem);
  });}




document.addEventListener("DOMContentLoaded", function () {
  // Set default state for history
  history.replaceState({ drivebox: "home" }, "Default state", "#home");

  // Handle popstate event when the user navigates back or forward
  window.addEventListener("popstate", (e) => {
    if (e.state.query) {
      // Load drivebox with search query
      load_drivebox("search", e.state.query);
    } else if (e.state.email) {
      // Parse HTML document from state element
      let doc = new DOMParser().parseFromString(e.state.element, 'text/html');
      // View email with parsed email, document, and mail state
      veiw_email(e.state.email, doc, e.state.mail);
    } else if (e.state.drivebox !== null) {
      if (e.state.drivebox !== "compose") {
        // Load drivebox other than compose
        load_drivebox(e.state.drivebox);
      } else {
        // Open compose email view
        compose_email();
      }
    }
  });

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
      
      if (document.querySelector("#emails-view").style.display !== "none") {
        maildiv = document.querySelector(".drivebox_head").textContent;
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

  // Set avatar background color based on user email and display the first character of first name
  let avatars = document.querySelectorAll(".user-icon");
  avatars.forEach((avatar) => {
    avatar.style.backgroundColor = calculateColor(user_email);
    avatar.innerHTML = user_firstn.charAt(0).toUpperCase();
  });

  // Handle search form submission
  document.querySelector(".srch-form").addEventListener("submit", (e) => {
    let srch_query = document.querySelector(".srch-inp").value;

    if (srch_query.trim().length > 0) {
      // Push state with search query and load drivebox with search query
      history.pushState({ query: srch_query.trim() }, "", `./#search/${srch_query.trim()}`);
      load_drivebox("search", srch_query.trim());
    }
    e.preventDefault();
  });

  // Handle compose email button click
  document.querySelector("#compose").addEventListener("click", () => {
    if (document.querySelector("#compose-view").style.display === "none") {
      compose_email();
    }
  });

  // Load the home by default
  load_drivebox("home");
});



function load_drivebox(drivebox, query = "") {
  // Call the 'tog_menu' function to toggle the menu (presumably a navigation menu).
  tog_menu();

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

  // Set the display property of the #emails-view, #check-email, and #compose-view elements.
  // #emails-view is set to "block" while #check-email and #compose-view are set to "none".
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#check-email").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Create a spinner HTML element using template literals and assign it to the 'spinner' variable.
  const spinner = `
  <div class="d-flex justify-content-center spin my-5">
    <div class="spinner-border text-danger" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>`;

  // Set the inner HTML of the #emails-view element to include a drivebox header (drivebox name capitalized) and the spinner.
  document.querySelector(
    "#emails-view"
  ).innerHTML = `<h4 class="drivebox_head py-2 pl-3 m-0 mx-1">${
    drivebox.charAt(0).toUpperCase() + drivebox.slice(1)
  }</h4> ${spinner}`;

  // If the drivebox is "search", modify the drivebox value to include the search query.
  if (drivebox === "search") {
    drivebox = `search/${query}`;
  }

  // Send a fetch request to the server to retrieve emails for the specified drivebox.
  fetch(`/drive/${drivebox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Remove the "d-flex" class and add the "d-none" class to the spinner element.
      $(".spin").removeClass("d-flex").addClass("d-none");

      // If there is an error property in the response, display an error message in the #emails-view element.
      if (emails.error) {
        document.querySelector(
          "#emails-view"
        ).innerHTML += `<h5 class="pl-3 pt-2">${emails.error} for "${query}"</h5>`;
      }
      // If there are emails, iterate over each email and create HTML elements to display them.
      else if(emails.length > 0){
        emails.forEach((email) => {
          // Create a div element to reprerecent a single email and assign it to the 'element' variable.
          const element = document.createElement("div");
          element.classList.add(
            "row",
            "my-0",
            "mx-1",
            "single-mail"
          );
          element.style.cursor = "pointer";
          // Set the inner HTML of the 'element' div to contain various information about the email using template literals.
          element.innerHTML = `
            ${(() => {
              // Set the 'sender' variable to the username of the email sender.
              let sender = email.username;
              // Create a user avatar element with the sender's initial inside a circle.
              let user_avatar = `<div class="user-icon-wrapper" >
                                 <span class="singlemail-user-icon rounded-circle text-white" style="background-color:${calculateColor(
                                   email.sender
                                 )}">${sender.charAt(0).toUpperCase()}</span>
                                </div>`;
              // Set the 'sendto' variable to the recipients of the email.
              let sendto = email.recipients;
              // If the sender is in the recipients list, replace their name with "me".
              if (sendto.includes(sender)) {
                let index = sendto.indexOf(email.username);
                sendto[index] = "me";
                sender = "me";
              }
              // If the email is recent by the current user, set the sender to "me".
              if(user_email === email.sender){
                sender = "me";
              }
              // If the drivebox is "recent", modify the sender to display the recipients.
              if (drivebox === "recent") {
                sender = `To: ${sendto}`;
              }
              let archive_stat = email.archived ? "Unarchive" : "Archive";
          let star_stat = email.starred ? "Starred" : "Not starred"
          let del_stat = email.deleted ? "Restore" : "Delete"

          let mark_read_stat = "Mark as Unread";
          if (!email.read) {
            mark_read_stat = "Mark as Read";
            element.classList.add("unread");
          } else {
            element.classList.add("light");
            element.classList.remove("unread");
          }

          let archive_slash = email.archived
            ? `<i class="fas fa-slash"></i>`
            : "";
          let mark_class = email.read ? "fa-envelope-open" : "fa-envelope";
          let star_class = email.starred ? "fas" : "far";
          let del_class = email.deleted ? "fa-recycle" : "fa-trash";
          let del_forever = drivebox === "trash" ?`<li class="btn-item del_forever" data-toggle="tooltip" data-placement="bottom" title="Delete forever"><i class="fas fa-trash"></i></li>   ` :"";
          let ext_btn = drivebox === "trash" ? "ext_btn": "";
          return `
            ${user_avatar}
            <div class="star-wrapper"  data-toggle="tooltip" data-placement="bottom" title="${star_stat}">
              <span class="star"> <i class="${star_class} fa-star"></i> </span>
            </div>
            <div class="sender">${sender}</div>
            <div class="subject text-left">
              <div class="d-inline">${
                email.subject.length > 0 ? email.subject : "(no subject)"
              }</div>
            <span class="text-muted font-weight-normal">${email.body.replace(
              /<(.|\n)*?>/gi,
              " "
            )}</span></div>
            <div class="timestamp ${ext_btn}">
            <span id="time">${readable_date(email.timestamp)}</span>
            <ul class="btn-list">
                <li class="btn-item archive" id="archive" data-toggle="tooltip" data-placement="bottom" title="${archive_stat}" >${archive_slash}</li>
                <li class="btn-item mark-read" data-toggle="tooltip" data-placement="bottom" title="${mark_read_stat}"><i class="fas ${mark_class}"></i></li>
                <li class="btn-item delete" data-toggle="tooltip" data-placement="bottom" title="${del_stat}"><i class="fas ${del_class}"></i></li>   
                ${del_forever}
            </ul>
            </div>
            `;
        })()}`;
        element.addEventListener(
          "click",
          (e) => {
            fetch(`/drive/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true,
              }),
            });
            history.pushState(
              { email: email.id ,
                element : element.innerHTML,
                mail: drivebox },
              "",
              `#${drivebox}/${email.id}`
            );
            // console.log(email.id);
            veiw_email(email.id, element, drivebox);

            e.stopImmediatePropagation();
          },
          false
        );

        mark_read(email, element, drivebox);
        mark_archive(email, element, drivebox);
        mark_star(email, element, drivebox);
        mark_del(email, element, drivebox);
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
        document.querySelector("#emails-view").append(element);
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
    .catch((error) => {
      console.log(error);
    });
}


function custm_alert(val) {
  // Select the elements for the toast
  const toastHead = document.querySelector("#head");
  const toast = document.querySelector("#myToast");

  // Remove the 'hideToast' class to show the toast
  toast.classList.remove('hideToast');

  // Update the toast content based on the value
  if (val.error) {
    toastHead.innerHTML = val.error;
  } else if (val.message) {
    load_drivebox("recent");
    toastHead.innerHTML = val.message;
  } else {
    toastHead.innerHTML = val;
  }

  // Configure the toast options
  $("#myToast").toast({ delay: 4000 });

  // Show the toast
  $("#myToast").toast("show");

  // Add event listener for when the toast is hidden
  $('#myToast').on('hidden.bs.toast', function () {
    // Add the 'hideToast' class to hide the toast
    toast.classList.add('hideToast');
  });
}


function readable_date(mail_date) {
  // Split the mail_date into day, year, and time components
  const [mail_day, mail_year, mail_time] = mail_date.split("-");

  // Create a new Date object
  const currentDate = new Date();

  // Check if the mail year matches the current year
  if (mail_year === currentDate.getFullYear().toString()) {
    // Check if the mail day matches the current day
    if (mail_day.split(" ")[1] === currentDate.getDate().toString()) {
      // Return the mail time
      return mail_time;
    }
    // Return the mail day
    return mail_day;
  } else {
    // Return the formatted date with day and year
    return `${mail_day}/${mail_year}`;
  }
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


function hide_element(element) {
  // Add the 'fade' class to the element using jQuery
  $(element).addClass("fade");

  // Add an event listener for the 'animationend' event
  element.addEventListener("animationend", () => {
    // Remove the element using jQuery
    $(element).remove();
  });
}

//Random user avatar based on email

var colors = [
  "#FFB900",
  "#D83B01",
  "#B50E0E",
  "#E81123",
  "#B4009E",
  "#5C2D91",
  "#0078D7",
  "#00B4FF",
  "#008272",
  "#107C10",
];

function calculateColor(email) {
  let sum = 0;

  // Calculate the sum of character codes in the email
  for (const index in email) {
    sum += email.charCodeAt(index);
  }

  // Return the color from the colors array based on the sum modulo colors.length
  return colors[sum % colors.length];
}
