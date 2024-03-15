// Parse user email, first name, and last name from DOM elements
const user_email = JSON.parse(document.getElementById("user_email").textContent);
const user_firstn = JSON.parse(document.getElementById("first_name").textContent);
const user_lastn = JSON.parse(document.getElementById("last_name").textContent);



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
  // document.querySelector("#compose").addEventListener("click", () => {
  //   if (document.querySelector("#compose-view").style.display === "none") {
  //     compose_email();
  //   }
  // });

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
    .then((files) => {
      console.log(files)
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
          // Create a div element to represent a single email and assign it to the 'element' variable.
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
              let sender = file.file;
              // Create a user avatar element with the sender's initial inside a circle.
              let user_avatar = `<div class="user-icon-wrappeWr" >
                                 <span class="singlemail-user-icon rounded-circle text-white" style="background-color:${calculateColor(
                                   file.file
                                 )}">${sender.charAt(0).toUpperCase()}</span>
                                </div>`;
              // Set the 'sendto' variable to the recipients of the file.
              let sendto = file.file;
              // If the sender is in the recipients list, replace their name with "me".
              if (sendto.includes(sender)) {
                let index = sendto.indexOf(file.file);
                sendto[index] = "me";
                sender = "me";
              }
              // If the email is sent by the current user, set the sender to "me".
              if(user_email === file.file){
                sender = "me";
              }
              // If the drivebox is "sent", modify the sender to display the recipients.
              if (drivebox === "sent") {
                sender = `To: ${sendto}`;
              }
              let archive_stat = file.archived ? "Unarchive" : "Archive";
          let star_stat = file.starred ? "Starred" : "Not starred"
          let del_stat = file.deleted ? "Restore" : "Delete"

          let mark_read_stat = "Mark as Unread";
          if (!file.read) {
            mark_read_stat = "Mark as Read";
            element.classList.add("unread");
          } else {
            element.classList.add("light");
            element.classList.remove("unread");
          }

          let archive_slash = file.archived
            ? `<i class="fas fa-slash"></i>`
            : "";
          let mark_class = file.read ? "fa-envelope-open" : "fa-envelope";
          let star_class = file.starred ? "fas" : "far";
          let del_class = file.deleted ? "fa-recycle" : "fa-trash";
          let del_forever = drivebox === "trash" ?`<li class="btn-item del_forever" data-toggle="tooltip" data-placement="bottom" title="Delete forever"><i class="fas fa-trash"></i></li>   ` :"";
          let ext_btn = drivebox === "trash" ? "ext_btn": "";
          return `
            <img src="drive/img/png-icon/f1.png">
            <div class="star-wrapper"  data-toggle="tooltip" data-placement="bottom" title="${star_stat}">
              <span class="star"> <i class="${star_class} fa-star"></i> </span>
            </div>
            <div class="sender">${sender}</div>
            <div class="subject text-left">
              <div class="d-inline">${
                file.file.length > 0 ? file.file : "(no subject)"
              }</div>
            <span class="text-muted font-weight-normal">${file.file}</span></div>
            <div class="timestamp ${ext_btn}">
            <span id="time">${readable_date(file.timestamp)}</span>
            <ul class="btn-list">
                <li class="btn-item archive" id="archive" data-toggle="tooltip" data-placement="bottom" title="${archive_stat}" >${archive_slash}</li>
                <li class="btn-item mark-read" data-toggle="tooltip" data-placement="bottom" title="${mark_read_stat}"><i class="fas ${mark_class}"></i></li>
                <li class="btn-item delete" data-toggle="tooltip" data-placement="bottom" title="${del_stat}"><i class="fas ${del_class}"></i></li>   
                ${del_forever}
            </ul>
            </div>
            `;
        })()}`;

        mark_read(file, element, drivebox);
        mark_archive(file, element, drivebox);
        mark_star(file, element, drivebox);
        mark_del(file, element, drivebox);
        if(drivebox === "trash"){
          element.querySelector(".del_forever").addEventListener("click", (e)=>{
            fetch(`/drive/${file.id}`, {
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



function mark_archive(file, element, drivebox) {
  // Add event listener to archive button
  element.querySelector("#archive").addEventListener(
    "click",
    (e) => {
      if (drivebox !== "archive" && drivebox !== "trash") {
        console.log(file.id)
        // If the file is not in the archive or trash drivebox, archive it
        fetch(`/drive/${file.id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: true,
          }),
        });
        console.log("here")
        custm_alert("Conversation archived");
        // Uncomment the following lines if you need to modify the CSS classes of the archive button
        // element.querySelector(":scope > #archive").classList.remove('archive')
        // element.querySelector(":scope > #archive").classList.add('unarchive')
      } else if (drivebox === "archive") {
        // If the file is already in the archive drivebox, unarchive it and move it to the home
        fetch(`/drive/${file.id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: false,
          }),
        });
        custm_alert("Conversation moved to home");
      }
      // Hide the tooltip of the archive button
      $(element.querySelector("#archive")).tooltip("hide");
      
      // If the drivebox is not the trash drivebox, hide the file element
      if (drivebox !== "trash") {
        hide_element(element);
      }
      e.stopImmediatePropagation();
    },
    false
  );
}



function mark_read(email, element, drivebox) {
  // Add event listener to mark as read button
  element.querySelector(".mark-read").addEventListener(
    "click",
    (e) => {
      let read = element.querySelector(":scope .mark-read > i");
      
      if (read.classList.contains("fa-envelope-open")) {
        // If the email is currently marked as read, mark it as unread
        read.classList.remove("fa-envelope-open");
        read.classList.add("fa-envelope");
        
        // Update tooltip and show it
        $(element.querySelector(".mark-read"))
          .attr("data-original-title", "Mark as read")
          .tooltip("show");
        
        element.classList.add("unread");
        element.classList.remove("light");
        
        // Update the email's read status on the server
        fetch(`/drive/${email.id}`, {
          method: "PUT",
          body: JSON.stringify({
            read: false,
          }),
        });
      } else {
        // If the email is currently marked as unread, mark it as read
        read.classList.remove("fa-envelope");
        read.classList.add("fa-envelope-open");
        
        // Update tooltip and show it
        $(element.querySelector(".mark-read"))
          .attr("data-original-title", "Mark as unread")
          .tooltip("show");
        
        element.classList.add("light");
        element.classList.remove("unread");
        
        // Update the email's read status on the server
        fetch(`/drive/${email.id}`, {
          method: "PUT",
          body: JSON.stringify({
            read: true,
          }),
        });
      }
      
      e.stopImmediatePropagation();
      $('[data-toggle="tooltip"]').tooltip();
    },
    false
  );
}



function mark_star(email, element, drivebox) {
  // Add event listener to star wrapper
  element.querySelector(".star-wrapper").addEventListener("click", (e) => {
    let star = element.querySelector(".fa-star");
    
    if (star.classList.contains("fas")) {
      // If the email is currently starred, unstar it
      star.classList.remove("fas");
      star.classList.add("far");
      
      // Update tooltip and show it
      $(element.querySelector(".star-wrapper"))
        .attr("data-original-title", "Not starred")
        .tooltip("show");
      
      // Update the email's starred status on the server
      fetch(`/drive/${email.id}`, {
        method: "PUT",
        body: JSON.stringify({
          starred: false,
        }),
      });
      
      // If the drivebox is the starred drivebox, hide the email element and hide tooltip
      if (drivebox === "starred") {
        $(element.querySelector(".star-wrapper")).tooltip("hide");
        hide_element(element);
      }
    } else {
      // If the email is not currently starred, star it
      star.classList.add("fas");
      
      // Update tooltip and show it
      $(element.querySelector(".star-wrapper"))
        .attr("data-original-title", "Starred")
        .tooltip("show");
      
      // Update the email's starred status on the server
      fetch(`/drive/${email.id}`, {
        method: "PUT",
        body: JSON.stringify({
          starred: true,
        }),
      });
    }

    e.stopImmediatePropagation();
    $('[data-toggle="tooltip"]').tooltip();
  });
}



function mark_del(email, element, drivebox) {
  // Add event listener to delete button
  element.querySelector(".delete").addEventListener("click", (e) => {
    if (drivebox !== "trash") {
      // If the email is not in the trash drivebox, move it to the trash
      fetch(`/drive/${email.id}`, {
        method: "PUT",
        body: JSON.stringify({
          deleted: true,
        }),
      });
      $(element.querySelector(".delete")).tooltip("hide");
      custm_alert("Conversation moved to trash");
    } else {
      // If the email is in the trash drivebox, restore it
      fetch(`/drive/${email.id}`, {
        method: "PUT",
        body: JSON.stringify({
          deleted: false,
        }),
      });
      $(element.querySelector(".delete")).tooltip("hide");
      custm_alert("Conversation restored from trash");
    }
    
    // Hide the email element
    hide_element(element);
    
    e.stopImmediatePropagation();
  });
}


function veiw_email(email_id, element, drivebox) {

  document.querySelector('.navbar').style.display = $(window).width() <= 768 ? "none" :"flex";
  document.querySelector("#emails-view").style.display = "none";
  // console.log(id);
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      if(email.error){
        custm_alert(email.error)
        load_drivebox(drivebox)
      }
      else{
        document.querySelector("#check-email").style.display = "block";
        let read = element.querySelector(".mark-read > i");
  // console.log(read)
  if(read.classList.contains("fa-envelope")){
    read.classList.remove("fa-envelope"),
      read.classList.add("fa-envelope-open"),
      $(element.querySelector("#check-email .mark-read"))
        .attr("data-original-title", "Mark as unread")
  }
  let star_title = email.starred ? "Starred": "Not Starred"
  let star_class = email.starred ? "fas" : "far";
  let sender = email.username;
  let user_avatar = `<div class="sing-icon-wrapper" >
                     <span class="sing-icon rounded-circle text-white" style="background-color:${calculateColor(
                       email.sender
                     )}">${sender.charAt(0).toUpperCase()}</span>
                    </div>`;
  let sendto = email.recipients.slice(0);
  // console.log(email.recipients)
  let subject =  email.subject.length > 0 ? email.subject : "(no subject)"
  if (sendto.includes(sender)) {
    let index = sendto.indexOf(email.username);
    sendto[index] = "me";
  }
  // console.log(email.recipients)
  let btn_list = element.querySelector(".btn-list").innerHTML 
  // console.log(btn_list)
      document.querySelector("#check-email").innerHTML = `
        <div class="px-md-4 px-sm-0">
         <div class="action_bar bg-white">
           <span class="btn-item back-btn"><i class="fas fa-arrow-left"></i></span>  
           <ul class="view-mail-btn-list">
           ${btn_list}
          </ul>         
         </div>
        
          <div class="row mx-auto">
            <h4 class="sing-sub">${
             subject
            }</h4>
          </div>

          <div class="sing-detail">
          ${user_avatar}
            <div class="sing-username-wrapper">
              <div class="sing-username">
                <p class="d-inline-block text-truncate p-0 m-0"><strong>${sender}</strong>  <span class="detail-small d-none d-lg-inline"><span><</span>${email.sender}></span> </p>
              </div>
            
              <div class="dropdown">
               <a class="dropdown-toggle text-muted h6 text-decoration-none detail-small tome" href="#" id="dropdownMenuButton" data-toggle="dropdown" data-display="static" >to ${sendto}</a>
                <div class="dropdown-menu dropdown-menu-right dropdown-menu-md-left shadow dropdown-tome" aria-labelledby="dropdownMenu2" style="top: 1rem;">
                <table class="table table-borderless my-2 detail-small">
                  <tbody>
                    <tr class="py-0">
                      <td class="text-muted text-right">From:</td>
                      <td><span class="font-weight-bold">${email.username}</span> . ${email.sender}</td>
                    </tr>
                    <tr>
                      <td class="text-muted text-right">To:</td>
                      <td>${email.recipients}</td>
                    </tr>
                    <tr>
                      <td class="text-muted text-right">Date:</td>
                      <td>${email.timestamp}</td>
                    </tr>
                    <tr>
                      <td class="text-muted text-right">Subject:</td>
                      <td>${subject}</td>
                    </tr>
                  </tbody>
                </table>
                </div>
              </div>
            </div>
 
            <div class="sing-timestamp">
              <p class="detail-small d-inline time">${$(window).width() <= 768 ? readable_date(email.timestamp) : email.timestamp}</p>
            </div>
         
            <div class="timestamp-icons pl-2">
              <span class="st" data-toggle="tooltip" data-placement="bottom" title="${star_title}" style="cursor:pointer"> <i class="${star_class} fa-star"></i> </span>
              <span data-toggle="tooltip" data-placement="bottom" title="Reply"><i class="fas fa-reply pl-3 replybtn" ></i></span>
          </div>
          </div>
          
          <div class="row-fluid sing-body my-3">
            <div class="p-0">${email.body}</div>
            
          </div>
          
          <div class="row mx-auto reply-btn">
            <button class="btn btn-light border my-3 mb-4 px-4 replybtn" id="reply" ><i class="fas fa-reply pr-3"></i>Reply</button>
            <button class="btn btn-light border my-3 mb-4 px-4 ml-3" id="forward" ><i class="fas fa-arrow-right pr-3"></i>Forward</button>
          </div>
          
        </div> 
      `;
      let btn_items = document.querySelectorAll("#check-email .btn-item")
      btn_items.forEach((btn_item) => {
        btn_item.addEventListener("click", () => {
          if(drivebox.startsWith("search")){
            let [,query] = drivebox.split("/")
            history.pushState({ query: query }, "", `./#search/${query}`);
          }
          history.pushState({ drivebox: drivebox }, "", `./#${drivebox}`);
 
        if(btn_item.classList.contains("archive")) {
          // mark_archive(email,element,drivebox)
           
          $(element.querySelector("#archive")).click()
            // hide_element(element);           
        }

        else if(btn_item.classList.contains("mark-read"))
        {
          // load_drivebox(drivebox)
          $(element.querySelector(".mark-read")).click()
          $(element.querySelector(".mark-read")).tooltip('hide')
          // setTimeout(() => { load_drivebox(drivebox)   }, 100);
        }
        
        else if(btn_item.classList.contains("delete")){
          $(element.querySelector(".delete")).click()
          // $(element.querySelector(".mark-read")).tooltip('hide')
        }
        else if(btn_item.classList.contains("del_forever")){
          $(element.querySelector(".del_forever")).click()
          // $(element.querySelector(".mark-read")).tooltip('hide')
        }
        let url = window.location.hash
        if(url.startsWith("#search")){
          let [,query] = url.split('/')
          setTimeout(() => { load_drivebox("search",query)   }, 300);
        }
        else{
          setTimeout(() => { load_drivebox(drivebox)   }, 300);
        }
        })
      })
      document.querySelector(".st").addEventListener("click" , (e) =>{
        let star = document.querySelector(".st .fa-star");
        if (star.classList.contains("fas")) {
          star.classList.remove("fas"),
            star.classList.add("far"),
            $( document.querySelector(".st"))
              .attr("data-original-title", "Not starred")
              .tooltip("show");
    
          fetch(`/drive/${email.id}`, {
            method: "PUT",
            body: JSON.stringify({
              starred: false,
            }),
          });
         
        } else {
          star.classList.add("fas"),
            $(document.querySelector(".st"))
              .attr("data-original-title", "Starred")
              .tooltip("show");
          fetch(`/drive/${email.id}`, {
            method: "PUT",
            body: JSON.stringify({
              starred: true,
            }),
          });
        }
    
        // e.stopImmediatePropagation();
      });
      let replybtns =  document.querySelectorAll(".replybtn")
      replybtns.forEach((btn) => {
        btn.addEventListener("click", (e) => {
          compose_email(email, "reply");
          e.stopImmediatePropagation();
        });
      })
      document.querySelector("#forward").addEventListener("click", (e)=>{
        compose_email(email, "forward");
          e.stopImmediatePropagation();
      })
      $('[data-toggle="tooltip"]').tooltip();
 
      }
    });
     //   // ... do something else with email ...
    // });
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
    load_drivebox("sent");
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
