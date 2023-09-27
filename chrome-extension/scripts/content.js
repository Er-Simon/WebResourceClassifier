function closeResourceClassificationInformation() {
    document.getElementById("webResourceClassifierContainer").style.display = "none";
}

async function resourceClassification(title, description) {
    
    let response = await fetch('http://localhost:5000/', {
        method: 'POST',
        body: JSON.stringify({
            "title": title,
            "description": description
        })
    }).catch(e => {
        console.log("[ERROR resourceClassification] ", e);
        document.getElementById("category").innerText = "INTERNAL ERROR";
    });

    if (response && response.ok) {
        document.getElementById("category").innerText = await response.text();
    }
}

var title = document.title
var description;

if (title == null) {

    var title_element = document.querySelector("meta[property='og:title']");

    if (title_element) {
        title = title_element.getAttribute("content")
    }
}

var description_element = document.querySelector('meta[name="description"]');

if (description_element) {
    description = description_element.getAttribute("content");
}

if (description == null) {
    description_element = document.querySelector('meta[property="og:description"]')

    if (description_element) {
        description = description_element.getAttribute("content");
    }
}


// `document.querySelector` may return null if the selector doesn't match anything.
if (title && description) {
    console.log(title);
    console.log(description);

    var outside_container = document.createElement("div");
    outside_container.id = "webResourceClassifierContainer";
    outside_container.classList.add("border", "border-3", "border-danger");
    outside_container.style.cssText = "width: 100%; top: 0px; left: 0px; padding: 0px; position: fixed; z-index: 2147483647; visibility: visible; background-color: #212529 !important;"

    var container = document.createElement("div");
    container.classList.add("container");
    container.style.color = "white";

    var extension_title = document.createElement('h1');
    extension_title.classList.add("my-5");
    extension_title.innerText = "Web Resource Classifier"
    container.appendChild(extension_title);

    var resourceURL = document.createElement("p");
    resourceURL.classList.add("lead", "my-3");
    resourceURL.innerHTML = "<code>URL: </code>" + window.location.href;
    container.appendChild(resourceURL);

    var resourceTitle = document.createElement("p");
    resourceTitle.classList.add("lead", "my-3");
    resourceTitle.innerHTML = "<code>Title: </code>" + title;
    container.appendChild(resourceTitle);

    var resourceDescription = document.createElement("p");
    resourceDescription.classList.add("lead", "my-3");
    resourceDescription.innerHTML = "<code>Description: </code>" + description;
    container.appendChild(resourceDescription);

    var loadingAssetUrl = chrome.runtime.getURL(
        "./loading.gif"
    );

    var category = document.createElement("h3");
    category.classList.add("mt-5");
    category.innerHTML = "<code>Recognized category: </code><span id='category' class='badge text-bg-light'>" +
        "<img src='" + loadingAssetUrl + "' height=32 width=32>" + "</span>";
    container.appendChild(category);

    var button = document.createElement("button");
    button.id = "websiteClassificationButton";
    button.classList.add("my-5", "btn", "btn-danger", "btn-lg", "float-end");
    button.innerText = "CLOSE";
    button.addEventListener("click", closeResourceClassificationInformation);
    container.appendChild(button);

    outside_container.appendChild(container);
    document.body.prepend(outside_container);

    resourceClassification(title, description);
}