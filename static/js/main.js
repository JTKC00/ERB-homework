const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(() => $("#message").fadeOut("slow"), 3000); // L function to fade out the message after 3 seconds   