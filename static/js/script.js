const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
    bar.addEventListener('click', () => {
        nav.classList.add('active');
    })
}

if (close) {
    close.addEventListener('click', () => {
        nav.classList.remove('active');
    })
}


var allPro = document.getElementsByClassName('pro');

for (i = 0; i < allPro.length; i++) {
    allPro[i].onclick = () => {
        window.location.href = 'sproduct.html';
    }
}

// // // var MainImg = document.getElementById("MainImg");
// // // var smallimg = document.getElementsByClassName("small-img");

// // // // smallimg[0].onclick = function () {
// // // //     MainImg.src = smallimg[0].src;
// // // // }

// // // for (let i = 0; smallimg.length; i++) {
// // //     smallimg[i].onclick = () => {
// // //         MainImg.src = smallimg[i].src;
// // //     }
// // // }