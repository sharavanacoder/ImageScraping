let downloadButton = document.querySelector('#download');
let form = document.querySelector('form');
let close = document.querySelector('.close');
let error=document.querySelector('.error')
let data = '';
form.addEventListener('submit', async function (e){
  e.preventDefault();
  console.log('fsf');
  data = form.children[0].value
  
  if (!data)
  {
    error.classList.add('alert', 'alert-danger', 'alert-dismissible', 'fade','show')
    error.role = 'alert';
    console.log("SUBMIT");
    error.innerHTML=`<strong>Please enter a valid url!!! </strong><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    <strong><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
      </button></strong>`
  }
  else
    downloadButton.style.display = 'block'; 
  
})
downloadButton.addEventListener('click', async function () {
const json={
        data: data
    };
    const options={
        method: "POST",
        body: JSON.stringify(json),
        headers:{
            'Content-Type':'application/json',
        }
    };
  let status = '';
   let rep=document.querySelector('.modal-body')
    fetch('/down',options)
      .then(res => {
        console.log('downloading')
        status = res.status;
          console.log(res.headers)
          return res.blob();
      }).then(blob => {
        if (status != 200) {
          rep.innerText = 'Interrupt Occurred!!!';
          close.style.display = 'block';
        } else {
          download(blob)
          rep.innerText = 'Downloading is finished!!!'
          close.style.display = 'block';
        }
        }).catch(err => {
          rep.innerText = 'Interrupt Occurred!!!';
          close.style.display = 'block';
        });
  downloadButton.style.display = 'none'; 
})