// Parse user email, first name, and last name from DOM elements
const user_email = JSON.parse(document.getElementById("user_email").textContent);
const user_firstn = JSON.parse(document.getElementById("english_name").textContent)? null : '';
const user_lastn = JSON.parse(document.getElementById("arabic_name").textContent)? null : '';



document.addEventListener("DOMContentLoaded", function () {

  history.replaceState({ drivebox: "home" }, "Default state", "#home");

  window.addEventListener("popstate", (e) => {
    if (e.state.query) {
      // Load mailbox with search query
      load_drivebox("search", e.state.query);
    } else if (e.state.file) {
      // Parse HTML document from state element
      let doc = new DOMParser().parseFromString(e.state.element, 'text/html');
      // View email with parsed email, document, and mail state
      veiw_email(e.state.file, doc, e.state.file);
    } else if (e.state.drivebox !== null) {
      if (e.state.drivebox !== "uploading") {
        // Load drivebox other than compose
        load_drivebox(e.state.drivebox);
      } else {
        // Open compose email view
        upload_files();
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
      
      if (document.querySelector("#files-view").style.display !== "none") {
        maildiv = document.querySelector(".mailbox_head").textContent;
        if (maildiv.toLowerCase() !== link.id) {
          // Push state with drivebox id and load drivebox if it's not compose
          history.pushState({ drivebox: link.id }, "", `./#${link.id}`);
          if (link.id !== "uploading") load_drivebox(link.id);
          else upload_files(link.id);
        }
      } else {
        // Push state with drivebox id and load drivebox if it's not compose
        history.pushState({ drivebox: link.id }, "", `./#${link.id}`);
        if (link.id !== "uploading") load_drivebox(link.id);
        else upload_files(link.id);
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

  // Handle compose email button click
  document.querySelector("#uploading").addEventListener("click", () => {
    if (document.querySelector("#files-upload").style.display === "none") {
      upload_files();
    }
  });

  // Load the inbox by default
  load_drivebox("home");
});


function upload_files(drivebox, query="") {

  $("#files-view").removeClass("d-flex").addClass("d-none");
  $("#files-upload").removeClass("d-none").addClass("d-flex");
  // $(".nav-link.active").removeClass("active")

  // Active Nav-links style
  $(".nav-link.active").each(function () {
    var link = this;
    
    link.addEventListener("click", function () {
      
      // Push state with drivebox id and load drivebox if it's not compose
      // history.pushState({ drivebox: link.id }, "", `./#${link.id}`);
      // if (link.id !== "uploading") load_drivebox(link.id);
      $("#files-view").removeClass("d-none").addClass("d-flex");
      $("#files-upload ").removeClass("d-flex").addClass("d-none");
      
    });
  });

}

function load_drivebox(drivebox, query="") {
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


  $("#files-view").removeClass("d-none").addClass("d-flex");
  $("#files-upload").removeClass("d-flex").addClass("d-none");


  // Create a spinner HTML element using template literals and assign it to the 'spinner' variable.
  const spinner = `
  <div class="d-flex justify-content-center spin my-5 w-100">
    <div class="spinner-border" role="status">
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
            "col-xl-6",
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
          img.src = '/static/drive/img/png-icon/file2.png';
          imgDiv.appendChild(img);


          const contentDiv = document.createElement("div");
          contentDiv.classList.add(
            "content"
          );
          element2.appendChild(contentDiv);


          const title = document.createElement("a");
          title.classList.add(
            "black",
            "mb-0"
          );
          title.href = `/media/${file.file}`
          title.target = '_blank';
          title.textContent = file.file;
          contentDiv.appendChild(title);


          const fileSize = document.createElement("p");
          fileSize.classList.add(
            "font-13",
            "c4",
            "p-0"
          );
          fileSize.textContent = file.timestamp
          contentDiv.appendChild(fileSize);


          const actionList = document.createElement("ul");

          actionList.classList.add(
            "btn-list",
          );
          actionList.style.marginTop = "10px"

          let archive_stat = file.archived ? "Unarchive" : "Archive";
          let star_stat = file.starred ? "Starred" : "Not starred"
          let del_stat = file.deleted ? "Restore" : "Delete"

          let archive_slash = file.archived
            ? `<i class="fas fa-slash" style="margin-left: 1.2rem; margin-top: 4px;"></i>`
            : "";
          let star_class = file.starred ? "fas" : "far";
          let del_class = file.deleted ? "fa-recycle" : "fa-trash";
          let del_forever = drivebox === "trash" ?`<li class="btn-item del_forever" data-toggle="tooltip" data-placement="bottom" title="Delete forever"><i class="fas fa-trash" style="margin-left: 0.8rem;"></i></li>   ` :"";
          let ext_btn = drivebox === "trash" ? "ext_btn": "";

          actionList.innerHTML = `
                <li class="star-wrapper" data-toggle="tooltip" data-placement="bottom" title="${star_stat}" style="margin:10px 5px 0 5px;"><i class="${star_class} fa-star pe-auto" style="font-size: 18px;"></i></li>
                <li class="btn-item archive" id="archive" data-toggle="tooltip" data-placement="bottom" title="${archive_stat}" style="margin-top: -1px;">${archive_slash}</li>
                <li class="btn-item delete" data-toggle="tooltip" data-placement="bottom" title="${del_stat}"><i class="fas ${del_class}" style="margin-left: 0.8rem;"></i></li>   
                ${del_forever}
          `

          element2.appendChild(actionList);

          document.querySelector("#files-view").append(filesView);


          filesView.addEventListener(
          "click",
          (e) => {
            fetch(`/drive/file/${file.id}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true,
              }),
            });
            history.pushState(
              { file: file.id ,
                filesView : filesView.innerHTML,
                file: drivebox },
              "",
              `#${drivebox}/${file.id}`
            );

            e.stopImmediatePropagation();
          },
          false
        );

        mark_archive(file, filesView, drivebox);
        mark_star(file, filesView, drivebox);
        mark_del(file, filesView, drivebox);
        if(drivebox === "trash"){
          element.querySelector(".del_forever").addEventListener("click", (e)=>{
            fetch(`/drive/file/${file.id}`, {
              method: "DELETE",
            });
            custm_alert("Conversation deleted forever")
            hide_element(filesView);
            e.stopImmediatePropagation();
          })
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
          "w-100",
        );
        empty.innerHTML = `
        <div class="text-center empty_icon"><i class="far fa-folder-open"></i></div>
        <div class="text-center empty_text">Nothing in ${drivebox}</div>`
        document.querySelector("#files-view").append(empty);
      }

    });
}


function mark_archive(file, element, drivebox) {
  // Add event listener to archive button
  element.querySelector("#archive").addEventListener(
    "click",
    (e) => {
      if (drivebox !== "archive" && drivebox !== "trash") {
        // If the email is not in the archive or trash drivebox, archive it
        fetch(`/drive/file/${file.id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: true,
          }),
        });
        custm_alert("Conversation archived");
        // Uncomment the following lines if you need to modify the CSS classes of the archive button
        // element.querySelector(":scope > #archive").classList.remove('archive')
        // element.querySelector(":scope > #archive").classList.add('unarchive')
      } else if (drivebox === "archive") {
        // If the email is already in the archive drivebox, unarchive it and move it to the inbox
        fetch(`/drive/file/${file.id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: false,
          }),
        });
        custm_alert("Conversation moved to inbox");
      }
      // Hide the tooltip of the archive button
      $(element.querySelector("#archive")).tooltip("hide");
      
      // If the drivebox is not the trash drivebox, hide the email element
      if (drivebox !== "trash") {
        hide_element(element);
      }
      e.stopImmediatePropagation();
    },
    false
  );
}


function mark_star(file, element, drivebox) {
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
      fetch(`/drive/file/${file.id}`, {
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
      fetch(`/drive/file/${file.id}`, {
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


function mark_del(file, element, drivebox) {
  // Add event listener to delete button
  element.querySelector(".delete").addEventListener("click", (e) => {
    if (drivebox !== "trash") {
      // If the email is not in the trash drivebox, move it to the trash
      fetch(`/drive/file/${file.id}`, {
        method: "PUT",
        body: JSON.stringify({
          deleted: true,
        }),
      });
      $(element.querySelector(".delete")).tooltip("hide");
      custm_alert("Conversation moved to trash");
    } else {
      // If the email is in the trash drivebox, restore it
      fetch(`/drive/file/${file.id}`, {
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




function custm_alert(val) {
  // Select the elements for the toast
  const toastHead = document.querySelector("#head");
  const toast = document.querySelector("#myToast");

  // Remove the 'hideToast' class to show the toast
  toast.classList.remove('hideToast');
  toastHead.classList.add("text-light")

  // Update the toast content based on the value
  if (val.error) {
    toastHead.innerHTML = val.error;
  } else if (val.message) {
    load_drivebox("home");
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
  $(element).addClass("d-none");

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
  for (const index in file) {
    sum += file.charCodeAt(index);
  }

  // Return the color from the colors array based on the sum modulo colors.length
  return colors[sum % colors.length];
}
